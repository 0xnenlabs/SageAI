from sageai import SageAI

# Init on startup
sageai = SageAI(
    openai_key="",
    functions_directory="functions",
    log_level="WARNING",
)

# In a CI/CD pipeline or in dev mode on startup/hot reload
sageai.index()

# Anywhere in the codebase
message = "What's the weather like in Boston right now?"
response = sageai.chat(message=message)

print(message)
print(response)
