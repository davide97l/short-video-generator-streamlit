agent_config = {
    "chatgpt": {
        "llm_provider": "chat_openai",  # Replace with your actual provider's model name
        "llm_model_name": "gpt-3.5-turbo",  # Replace with your provider's specific params
        "system_prompt": "You are a helpful assistant. Answer all questions to the best of your ability.",
        "temperature": 0.7,  # Optional temperature setting
    },
    "g4f": {
        "llm_provider": "g4f",  # Replace with your actual provider's model name
        "llm_model_name": "gpt-3.5-turbo",  # Replace with your provider's specific params
        "system_prompt": "You are a helpful assistant. Answer all questions to the best of your ability.",
        "temperature": 0.7,  # Optional temperature setting
    },
    "text_to_paragraphs": {
        "llm_provider": "chat_openai",
        "llm_model_name": "gpt-3.5-turbo",
        "system_prompt": """
        Split the text into meaningful paragraphs. A paragraph should represent a distinct topic.
        Score each paragraph according to:
        - how it is understandable without further context
        - its ability to tell a story itself
        - how interesting is its context
        Return each paragraph and score from 0 to 10 along with its reason。
        The output should have the following json format.
        
        OUTPUT
        
        [
            {
            "score": (int),
            "reason": (str),
            "paragraph": (str)
            }
        ]
        """,
        "temperature": 0.,  # Optional temperature setting
    },
}
