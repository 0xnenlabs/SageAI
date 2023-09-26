from sageai import SageAI

# Init once on their app starting up
SageAI.init(functions_directory=".gitignore", openai_key="123")

# Anywhere in their codebase
file = SageAI.ask("hello mate")
