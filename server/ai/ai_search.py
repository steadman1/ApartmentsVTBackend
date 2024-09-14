import os
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up OpenAI client with Azure's API
openai.api_type = "azure"
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = os.getenv("OPENAI_API_BASE")  # e.g., 'https://vthacks2024.openai.azure.com/'
openai.api_version = "2023-06-01-preview"  # Update to the correct API version if needed


def ai_search(prompt: str):
    try:
        response = openai.ChatCompletion.create(
            engine=os.getenv("OPENAI_DEPLOYMENT_NAME"),  # e.g., 'VTHacks24'
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful assistant that extracts concise, relevant keywords from user queries "
                        "to aid in apartment searches. Only provide the keywords separated by commas without additional text."
                    ),
                },
                {
                    "role": "user",
                    "content": f"Extract the main keywords from the following search query, separated by commas:\n\n{prompt}",
                },
            ],
            max_tokens=50,
            temperature=0.5,
        )
        keywords_text = response['choices'][0]['message']['content'].strip()
        keywords = [kw.strip() for kw in keywords_text.split(',') if kw.strip()]
        return find_matching_listings(keywords)
    except openai.error.OpenAIError as e:
        print(f"OpenAI API error: {e}")
        return []

def find_matching_listings(keywords: list):
    # Import your database model
    from your_app.models import Listing  # Adjust the import path as necessary

    # Build a query to search for listings that match the keywords
    query = Listing.query
    for keyword in keywords:
        keyword = keyword.lower()
        query = query.filter(
            Listing.title.ilike(f"%{keyword}%") |
            Listing.summary.ilike(f"%{keyword}%") |
            Listing.propertyType.ilike(f"%{keyword}%") |
            Listing.proximityToStores.any(keyword)  # Adjust if using an array field
            # Add other fields as necessary
        )
    results = query.all()
    # Convert listings to dictionaries for JSON serialization
    return [listing.to_dict() for listing in results]
