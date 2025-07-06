
def clean_string(string: str):
    string_return = string.replace("minecraft__", "").replace("fluid__", "").replace("_", " ").replace(".png", "").replace("of ", "")
    return string_return