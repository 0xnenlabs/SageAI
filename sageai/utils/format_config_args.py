import inspect
import os


def get_user_package_path():
    caller_frame = inspect.stack()[4]
    caller_module = inspect.getmodule(caller_frame[0])

    if caller_module is None or not hasattr(caller_module, "__file__"):
        raise ValueError("Cannot determine the path of the caller's module")

    module_path = os.path.abspath(caller_module.__file__)
    return os.path.dirname(module_path)


def format_config_args(**kwargs):
    if "functions_directory" not in kwargs:
        kwargs["functions_directory"] = "functions"
    if not os.path.isabs(kwargs["functions_directory"]) and not kwargs[
        "functions_directory"
    ].startswith("./"):
        base_path = get_user_package_path()
        kwargs["functions_directory"] = os.path.join(
            base_path, kwargs["functions_directory"]
        )
    elif kwargs["functions_directory"].startswith("./"):
        base_path = get_user_package_path()
        # Strip './' from the beginning and then join with the base path
        relative_path = kwargs["functions_directory"][2:]
        kwargs["functions_directory"] = os.path.join(base_path, relative_path)
    return kwargs
