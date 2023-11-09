import openai
from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()

# Set the API key from the OPENAI_API_KEY environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

# Ensure the API key is present
if not openai.api_key:
    raise ValueError("The OPENAI_API_KEY environment variable is not set.")

# The prompt for the test
prompt_text = "Translate the following English text to French: 'Hello, how are you?'"

# Call the OpenAI API
try:
    response = openai.Completion.create(
        engine="text-davinci-003",  # Or "gpt-3.5-turbo" depending on your plan
        prompt=prompt_text,
        max_tokens=60
    )
    # Print the response
    print(response.choices[0].text.strip())
except Exception as e:
    print(f"An error occurred: {e}")
