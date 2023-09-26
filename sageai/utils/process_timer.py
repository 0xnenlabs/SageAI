import time
from typing import Callable, Any, Tuple, get_type_hints


def process_timer(func: Callable[..., Any]) -> Callable[..., Any]:
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        duration = round(end_time - start_time, 1)

        # Check return type hint
        return_type_hint = get_type_hints(func).get("return")
        if return_type_hint == Tuple:
            # If the function was expected to return a tuple, add the duration to the tuple
            return (*result, duration)
        else:
            # Otherwise, return as a tuple (result, duration)
            return result, duration

    return wrapper
