import openai
import re


def preprocess_text(text):
    """
    Preprocesses the given text by removing extra spaces and leading/trailing spaces.
    """
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text


def generate_response(query, resume_text, max_length=100):
    """
    Generates a response based on the input query using the OpenAI API.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are a helpful AI trained on the following resume: {resume_text}"},
                {"role": "user", "content": query}
            ],
            max_tokens=max_length,
            n=1,
            temperature=0.7,
            top_p=0.9,
        )

        response_text = response.choices[0].message.content
        return response_text
    except Exception as e:
        print(f"Error generating response: {e}")
        return "I'm sorry, I couldn't generate a response."
