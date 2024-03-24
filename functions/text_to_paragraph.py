from agents.configs import agent_config
from agents.llm_agent import LLMAgent
from functions.is_valid_json import is_valid_json


def text_to_paragraph(text: str, threshold=None):
    agent = LLMAgent(agent_config['text_to_paragraphs'])
    user_prompt = text
    result = agent.run(user_prompt, memory=False)
    is_valid, paragraphs = is_valid_json(result['response'])
    if not is_valid:
        raise Exception('Invalid JSON')
        # maybe can call again the agent and change temperature or seed

    # Create an empty list to store paragraph dictionaries
    paragraph_list = []

    # Iterate through each paragraph in the response
    for entry in paragraphs:
        if threshold and entry["score"] < threshold:
            continue
        # Create a dictionary for the current paragraph and score
        paragraph_dict = {"paragraph": entry["paragraph"], "score": entry["score"], "reason": entry["reason"]}
        # Append the dictionary to the list
        paragraph_list.append(paragraph_dict)

    # Return the list of dictionaries
    return paragraph_list


if __name__ == '__main__':
    text = """One so child came to visit his grandfather during his summer holidays. He used to play with his grandpa all the time. One day he said to his grandpa, When I grow up, I want to become a successful man. Can you tell me some ways to be successful? Grandfather nodded. Yes. And took the boy with him to a nearby nursery. From nursery, his grandpa bought two small plants and came back home. Then he planted one plant in a pot and kept it inside the house and planted another one outside the house. What do you think? Which of these two plants will grow better in future? Grandfather asked the boy. Boy, kept thinking for some time and then said, The plant inside the house will grow better because it is safe from every danger while the plant outside is at risk of many things like strong sunlight, storms, animals, etc. Grandfather smiled and said, Let's see what happens in future. After that boy left with his parents. After four years, Boy came to visit his grandfather again when the boy saw his grandfather. """
    print(text_to_paragraph(text))
