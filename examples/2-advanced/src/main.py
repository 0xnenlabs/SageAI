from sageai import Message, SageAI

from .customvectordb import CustomVectorDB

# Init on startup
sage = SageAI(
    openai_key="",
    vectordb=CustomVectorDB,
)

# In a CI/CD pipeline or in dev mode on startup/hot reload
sage.index()

# Anywhere in the codebase
message = "What's the weather like in Boston right now?"
print(f"Message: {message}")
response = sage.chat(
    messages=[Message(role="user", content=message)],
    model="gpt-3.5-turbo-0613",
    top_n=5,
)
print(f"Response: {response}")

message = "Give me a number between 1 and 10."
print(f"\nMessage: {message}")
response = sage.chat(
    messages=[Message(role="user", content=message)],
    model="gpt-3.5-turbo-0613",
    top_n=5,
)
print(f"Response: {response}")

message = "What's the weather tomorrow in Toronto?"
print(f"\nMessage: {message}")
response = sage.chat(
    messages=[Message(role="user", content=message)],
    model="gpt-3.5-turbo-0613",
    top_n=5,
)
print(f"Response: {response}")
