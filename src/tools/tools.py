from langchain.tools import tool


@tool
def get_location() -> str:
    """Get the current location"""
    # For the sake of this example, we'll return a dummy location.
    return "Cieszyn, Poland"


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


@tool
def calculate_sum(a: int, b: int) -> int:
    """Calculate the sum of two integers"""
    return a + b


@tool
def reverse_string(s: str) -> str:
    """Reverse the given string"""
    return s[::-1]


@tool
def get_current_time() -> str:
    """Get the current time"""
    from datetime import datetime

    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@tool
def generate_random_number(start: int, end: int) -> int:
    """Generate a random number between start and end"""
    import random

    return random.randint(start, end)


@tool
def translate_text(text: str, target_language: str) -> str:
    """Translate the given text to the target language"""
    # For the sake of this example, we'll return a dummy translation.
    return f"Translated '{text}' to {target_language}"


@tool
def fetch_data_from_api(url: str) -> str:
    """Fetch data from the given API URL"""
    import requests

    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return f"Failed to fetch data from {url}. Status code: {response.status_code}"


@tool
def summarize_text(text: str) -> str:
    """Summarize the given text"""
    # For the sake of this example, we'll return a dummy summary.
    return f"Summary of the text: {text[:50]}..."


@tool
def count_words(text: str) -> int:
    """Count the number of words in the given text"""
    return len(text.split())


@tool
def generate_random_string(length: int) -> str:
    """Generate a random string of the specified length"""
    import random
    import string

    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


@tool
def check_palindrome(s: str) -> bool:
    """Check if the given string is a palindrome"""
    cleaned = "".join(s.lower().split())
    return cleaned == cleaned[::-1]


@tool
def calculate_factorial(n: int) -> int:
    """Calculate the factorial of a given number"""
    if n < 0:
        return "Factorial is not defined for negative numbers."
    elif n == 0 or n == 1:
        return 1
    else:
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result


@tool
def generate_fibonacci(n: int) -> list:
    """Generate the Fibonacci sequence up to the nth number"""
    sequence = []
    a, b = 0, 1
    for _ in range(n):
        sequence.append(a)
        a, b = b, a + b
    return sequence


@tool
def convert_temperature(celsius: float) -> float:
    """Convert Celsius to Fahrenheit"""
    return (celsius * 9 / 5) + 32
