from sageai import SageAI, set_config

set_config(functions_directory=".gitignore", openai_key="123")
file = SageAI.ask("hello mate")
# print(file)
