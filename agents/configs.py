agent_config = {
    "chatgpt": {
        "llm_model": "chat_openai",  # Replace with your actual provider's model name
        "llm_model_name": "gpt-3.5-turbo",  # Replace with your provider's specific params
        "system_prompt": "You are a helpful assistant. Answer all questions to the best of your ability.",
        "temperature": 0.7,  # Optional temperature setting
    },
    "text_to_paragraphs": {
        "llm_model": "chat_openai",  # Replace with your actual provider's model name
        "llm_model_name": "gpt-3.5-turbo",  # Replace with your provider's specific params
        "system_prompt": "Split the text into meaningful paragraphs. A paragraph should represent a distinct topic. Use \n\n to split paragraphs",
        "temperature": 0.,  # Optional temperature setting
    },
}