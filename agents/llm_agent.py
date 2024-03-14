from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv
from langchain_community.callbacks import get_openai_callback
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import AIMessage, HumanMessage
from langchain.memory import ChatMessageHistory
from agents.configs import agent_config

load_dotenv()


class LLMAgent:
    """
    This class defines a custom LLM agent that receives a prompt and outputs the result.

    Attributes:
        config: A dictionary containing configuration options, including the LLM model,
                prompt template, and system prompt.
    """

    def __init__(self, config):
        self.config = config
        self.llm = self.get_llm_model(config)
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", "{system_prompt}"),
            MessagesPlaceholder(variable_name="chat_history"),]
         )
        self.system_prompt = config.get("system_prompt", "")
        self.chat_history = ChatMessageHistory()

    @staticmethod
    def get_llm_model(config):
        """
        Loads the LLM model based on the configuration.

        Args:
            config: The configuration dictionary.

        Returns:
            The loaded LLM model instance.
        """
        # Replace this logic with your actual LLM provider's model loading method
        llm_model_name = config.get("llm_model")
        if llm_model_name == "chat_openai":  # Example for ChatOpenAI
            from langchain_openai import ChatOpenAI
            return ChatOpenAI(model_name=config.get("llm_model_name", {}), temperature=config.get("temperature", 0))
        else:
            raise ValueError(f"Unsupported LLM model: {llm_model_name}")

    def run(self, prompt, memory=False):

        self.chat_history.add_user_message(prompt)

        full_prompt = self.prompt_template.format(
            system_prompt=self.system_prompt,
            chat_history=self.chat_history.messages if memory else [HumanMessage(content=prompt)]
        )
        with get_openai_callback() as cb:
            response = self.llm.invoke(full_prompt)

        self.chat_history.add_ai_message(message=response.content)

        return {
            "response": response.content,
            "total_tokens": cb.total_tokens,
            "prompt_tokens": cb.prompt_tokens,
            "completion_tokens": cb.completion_tokens,
            "total_cost": cb.total_cost,
        }


if __name__ == '__main__':
    agent = LLMAgent(agent_config['chatgpt'])
    user_prompt = "I ate an apple"
    result = agent.run(user_prompt, memory=False)
    print(result)
    user_prompt = "what did I eat"
    result = agent.run(user_prompt, memory=True)
    print(result)
