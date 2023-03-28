import openai
import re


def preprocess_text(text):
    """
    Preprocesses the given text by removing extra spaces and leading/trailing spaces.
    """
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text
