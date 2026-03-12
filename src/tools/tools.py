from langchain.tools import tool


@tool
def get_current_weather(location: str) -> str:
    """Get the current weather in a given location"""
    # For the sake of this example, we'll return a dummy weather report.
    return f"The current weather in {location} is sunny with a temperature of 25°C."


@tool
def save_to_file(filename: str, content: str) -> str:
    """Save the given content to a file with the specified filename"""
    with open(filename, "w") as f:
        f.write(content)
    return f"Content saved to {filename}"
