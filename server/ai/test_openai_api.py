import os
import openai
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Set up OpenAI client with Azure's API
openai.api_type = "azure"
openai.api_base = os.getenv("OPENAI_API_BASE")  # e.g., 'https://vthacks24.openai.azure.com'
openai.api_version = "2023-06-01-preview"       # Update to the correct API version if needed
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define the deployment name (your deployment name in Azure)
deployment_name = os.getenv("OPENAI_DEPLOYMENT_NAME")  # e.g., 'VTHacks24'

def test_openai_api():
    try:
        # Prompt the user for a question
        question = input("Please enter your question: ")

        response = openai.ChatCompletion.create(
            engine=deployment_name,
            messages=[
                {"role": "user", "content": question}
            ],
            max_tokens=500,
            temperature=0.5,
        )
        message = response['choices'][0]['message']['content'].strip()
        print("\nResponse from OpenAI:")
        print(message)
    except Exception as e:
        print("An error occurred:")
        print(e)

if __name__ == "__main__":
    test_openai_api()
