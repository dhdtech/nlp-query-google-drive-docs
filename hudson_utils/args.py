from typing import List


def get_from_args(args: List[str], arg_name: str, default_value: str) -> str:
    """
    Get a value from command-line arguments.

    Args:
        args (List[str]): A list of command-line arguments.
        arg_name (str): The name of the argument to find.

    Returns:
        str: The value of the argument.

    Example:
        >>> get_threshold_from_args(["--threshold=0.7", "--other=option"])
        0.7
    """
    for arg in args:
        if arg.startswith(f"--{arg_name}="):
            return arg.split("=")[1]

    return default_value
