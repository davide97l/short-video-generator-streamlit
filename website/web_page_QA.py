import bs4
from langchain import hub
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from dotenv import load_dotenv


# https://python.langchain.com/docs/use_cases/question_answering/quickstart


load_dotenv()
openai_api_key = os.environ.get("OPENAI_API_KEY")
link = "https://lilianweng.github.io/posts/2023-06-23-agent/"
link = 'https://padovamarathon.com/en/marathon/'


# Load, chunk and index the contents of the blog.
loader = WebBaseLoader(
    web_paths=(link,),
    #bs_kwargs=dict(
    #    parse_only=bs4.SoupStrainer(
    #        class_=("post-content", "post-title", "post-header")
    #    )
    #),
)
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)
vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())

# Retrieve and generate using the relevant snippets of the blog.
retriever = vectorstore.as_retriever()
prompt = hub.pull("rlm/rag-prompt")
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, openai_api_key=openai_api_key)


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
)

questions = [
    "What is the date of the event?",
    "Where is the event located? Reply with Country, Region, City, and address if provided",
    "What time do the event start?",
    '''
    Get the following info:
    Event: (name event)
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

# cleanup
vectorstore.delete_collection()