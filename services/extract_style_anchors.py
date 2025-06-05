from utils.prompt_loader import load_prompt
from utils.llm import call_openAI

import json


"""
Extracts style anchros from a given text.
"""

#Function that extracts style anchors from multiple texts
def extract_style_anchors_from_texts(texts: list, min_sentences: int = 3, max_sentences: int = 5, model: str = "gpt-4.1-nano") -> list:
    """
    Extracts style anchors from a list of texts.

    Args:
        texts (list): A list of input texts from which to extract style anchors.

    Returns:
        list: A list of extracted style anchors.
    """
    all_anchors = []
    for text in texts:
        anchors = extract_style_anchors(text, min_sentences, max_sentences, model)
        all_anchors.append(anchors)
    return all_anchors

def extract_style_anchors(text: str, min_sentences: int = 3, max_sentences: int = 5, model: str = "gpt-4.1-nano") -> list:
    """
    Extracts style anchors from a given text.

    Args:
        text (str): The input text from which to extract style anchors.

    Returns:
        list: A list of extracted style anchors.
    """
    #1. Load prompt

    replacements = {
        "[MIN-SENT]": min_sentences,
        "[MAX-SENT]": max_sentences,
    }

    prompt = load_prompt(
        folder_path="prompts/extract_style_anchors",
        replacements = replacements
        )

    #2 Call OpenAI API

    response = call_openAI(
        instructions=prompt,
        input=text,
        model=model
    )

    #3 Parse response
    response = json.loads(response)
    response = response["sentences"]

    return response