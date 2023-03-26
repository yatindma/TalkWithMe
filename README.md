# TalkWithME

This project provides a chatbot that can answer questions based on a user's resume. The chatbot is powered by OpenAI's GPT-3.5-turbo model and stores chat history in a MongoDB database. The application is containerized using Docker for easy deployment.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Setup](#setup)
- [Usage](#usage)
- [License](#license)

## Features

- Generate AI-based responses using OpenAI's GPT-3.5-turbo model.
- Preprocess and utilize a given resume as the chatbot's knowledge source.
- Store chat history in a MongoDB database.
- Dockerized application for easy deployment.

## Requirements

- Docker
- An OpenAI API key
- MongoDB database

## Setup

1. Clone the repository:
```
git clone https://github.com/yatindma/TalkWithMe
cd resume-chatbot
```

2. Create a `config.ini` file in the project directory with your OpenAI API key and MongoDB connection details:

```ini
[OpenAI]
api_key = your_openai_api_key

[MongoDB]
connection_string = mongodb://username:password@host:port/db_name
db_name = your_database_name
collection_name = your_collection_name
```
3. Replace the contents of resume.txt with your desired resume text.

4. Build the Docker image:
```
docker build -t personalized-chatbot .
```
## Usage
1. Run the chatbot:
docker run -it resume-chatbot
2. Interact with the chatbot by typing your questions.
3. Type 'exit' to stop chatting.

## License
This project is released under the MIT License



