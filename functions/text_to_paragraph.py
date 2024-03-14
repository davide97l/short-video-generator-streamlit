from agents.configs import agent_config
from agents.llm_agent import LLMAgent


def text_to_paragraphs(text: str):
    agent = LLMAgent(agent_config['text_to_paragraphs'])
    user_prompt = text
    result = agent.run(user_prompt, memory=False)
    paragraphs = result['response'].split('\n\n')
    return paragraphs
