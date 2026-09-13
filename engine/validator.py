import ast


FORBIDDEN_IMPORTS = {
    "os",
    "sys",
    "subprocess",
    "socket",
    "requests",
    "urllib",
    "shutil",
    "pathlib",
    "pickle",
    "marshal",
    "ctypes"
}


FORBIDDEN_FUNCTIONS = {
    "eval",
    "exec",
    "compile",
    "__import__"
}


def validate_strategy_code(code):
    """
    Validate AI-generated strategy code before execution.
    """

    try:
        tree = ast.parse(code)
    except SyntaxError as error:
        return False, f"Syntax error: {error}"

    for node in ast.walk(tree):

        # Check imports.
        if isinstance(
            node,
            (ast.Import, ast.ImportFrom)
        ):
            for alias in node.names:

                module = alias.name.split(".")[0]

                if module in FORBIDDEN_IMPORTS:
                    return False, (
                        f"Forbidden import: {module}"
                    )

        # Check dangerous functions.
        if isinstance(node, ast.Call):

            if isinstance(
                node.func,
                ast.Name
            ):
                if node.func.id in FORBIDDEN_FUNCTIONS:
                    return False, (
                        f"Forbidden function: "
                        f"{node.func.id}"
                    )

    # Ensure required function exists.
    functions = [
        node.name
        for node in tree.body
        if isinstance(node, ast.FunctionDef)
    ]

    if "generate_signals" not in functions:
        return False, (
            "generate_signals(df) was not found."
        )

    return True, "Validation passed."
