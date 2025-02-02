LANGUAGE_TEMPLATES = {
    "python": {
        "function": "def {name}({params}):\n    \"\"\"{docstring}\"\"\"\n",
        "class": "class {name}:\n    \"\"\"{docstring}\"\"\"\n"
    },
    "javascript": {
        "function": "function {name}({params}) {\n  // {docstring}\n",
        "class": "class {name} {\n  // {docstring}\n"
    }
}

SUPPORTED_LANGUAGES = ["python", "javascript"]
MAX_CODE_LENGTH = 10000
