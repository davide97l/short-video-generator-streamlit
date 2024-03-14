# pip install streamlit langchain lanchain-openai beautifulsoup4 python-dotenv chromadb

import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough


load_dotenv()


def get_vectorstore_from_url(url):
    """Retrieves a vectorstore representation of text content from a given URL.
    Args:
        url: The URL of the website to extract text from.
    Returns:
        A Chroma vectorstore containing embedded text chunks.
    """
    loader = WebBaseLoader(url)  # Load entire text content from the website
    document = loader.load()
    text_splitter = RecursiveCharacterTextSplitter()
    document_chunks = text_splitter.split_documents(document)  # Split text into manageable chunks
    vector_store = Chroma.from_documents(document_chunks, OpenAIEmbeddings())  # Create vectorstore with embedded chunks
    return vector_store


def get_context_retriever_chain(vector_store):
    """Creates a retriever chain that considers conversation history for context.
    Args:
        vector_store: The vectorstore to use for retrieval.

    Returns:
        A LangChain retriever chain with context awareness.
    """
    llm = ChatOpenAI()  # Initialize a language model for query generation
    retriever = vector_store.as_retriever()  # Create retriever from the provided vectorstore
    # Define a prompt template for generating search queries based on conversation history
    prompt = ChatPromptTemplate.from_messages([
        MessagesPlaceholder(variable_name="chat_history"),  # Placeholder for conversation history
        ("user", "{input}"),  # User's current input
        ("user", "Given the above conversation, generate a search query to look up in order to get information relevant to the conversation")
    ])
    # Build a history-aware retriever chain
    retriever_chain = create_history_aware_retriever(llm, retriever, prompt)
    return retriever_chain


def get_conversational_rag_chain(retriever_chain):
    """Creates a conversational RAG chain that combines retrieval and generation abilities.
    Args:
        retriever_chain: The underlying retriever chain to use.

    Returns:
        A LangChain conversational RAG chain.
    """
    llm = ChatOpenAI()  # Initialize a language model for response generation
    # Define a prompt template for guiding response generation based on context and retrieved documents
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Answer the user's questions based on the below context:\n\n{context}"),
        MessagesPlaceholder(variable_name="chat_history"),  # Placeholder for conversation history
        ("user", "{input}"),  # User's current input
    ])
    # Create a chain for combining retrieved documents with the prompt
    stuff_documents_chain = create_stuff_documents_chain(llm, prompt)
    # Build the final conversational RAG chain
    return create_retrieval_chain(retriever_chain, stuff_documents_chain)


def get_event_info(vector_store):

    prompt = hub.pull("rlm/rag-prompt")  # TODO write by myself
    llm = ChatOpenAI(model_name="gpt-3.5-turbo")
    retriever = vector_store.as_retriever()  # Create retriever from the provided vectorstore

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
    )

    questions = [
        '''
        Retrieve the following info. If not provided just say 'not provided':
        
        OUTPUT
        
        Event: (full name event)
        Date: (date of the event in YYYY/MM/DD format)
        Start time: (time the event start in HH:MM am or pm)
        Finish time: (time the event finish in HH:MM am or pm)
        Location: (state, city)
        Address: (detailed address)
        Price: (event price in dollars. Write FREE is you are sure the even is free)
        '''
    ]

    for q in questions:
        o = rag_chain.invoke(q)
        print(o)


def get_response(user_input):
    """Generates a response to a user's input based on the conversation history and retrieved information.

    Args:
        user_input: The user's current input.

    Returns:
        The generated response.
    """

    retriever_chain = get_context_retriever_chain(st.session_state.vector_store)  # Access vectorstore from session state
    conversation_rag_chain = get_conversational_rag_chain(retriever_chain)

    # Invoke the conversational RAG chain with conversation history and user input
    response = conversation_rag_chain.invoke({
        "chat_history": st.session_state.chat_history,  # Access conversation history from session state
        "input": user_input
    })

    return response['answer']  # Extract the generated response


