from sageai.types.function import Function


def func1(param1: str, param2: int):
    return f"param1: {param1} | param2: {param2}"


function = Function(function=func1, description="test function 1")
