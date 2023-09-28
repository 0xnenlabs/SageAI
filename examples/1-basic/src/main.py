from sageai import SageAI

# Init on startup
sage = SageAI(openai_key="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")

# In a CI/CD pipeline or in dev mode on startup/hot reload
sage.index()

# Anywhere in the codebase
message = "What's the weather like in Boston right now?"
response = sage.chat(
    messages=[dict(role="user", content=message)],
    model="gpt-3.5-turbo-0613",
    top_n=5,
)

print(f"Message: {message}")
print(f"Response: {response}")
