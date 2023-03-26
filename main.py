from resume_bot import generate_response, preprocess_text
from mongodb_helper import connect_to_mongodb, store_chat

# Read resume text
resume_path = "resume.txt"
with open(resume_path, "r") as f:
    resume_text = f.read()

# Preprocess resume text
resume_text = preprocess_text(resume_text)

# Connect to MongoDB
chat_collection = connect_to_mongodb()

# Chat loop for interacting with the model
print("Chatbot is ready. Type 'exit' to stop chatting.")
while True:
    query = input("You: ")
    if query.lower() == 'exit':
        break
    response = generate_response(query, resume_text)
    store_chat(chat_collection, query, response)
    print("Bot:", response)
