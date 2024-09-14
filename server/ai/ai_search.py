import os
import json
import logging
import openai
from dotenv import load_dotenv
from server.posts.models import Post
from server import create_app

app = create_app()

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set up OpenAI client with Azure's API
openai.api_type = "azure"
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = os.getenv("OPENAI_API_BASE")  
openai.api_version = "2023-06-01-preview"      

# Define the deployment name (your deployment name in Azure)
deployment_name = os.getenv("OPENAI_DEPLOYMENT_NAME")  

def ai_search(prompt: str):
    try:
        response = openai.ChatCompletion.create(
            engine=deployment_name,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an assistant that extracts apartment search criteria from user queries. "
                        "Extract the following fields from the user's input and output them in JSON format. "
                        "Use null for fields not specified.\n\n"
                        "Fields:\n"
                        "- price (integer): Maximum monthly rent in USD\n"
                        "- roommate_count (integer)\n"
                        "- gender_preferences (list of strings): e.g., ['male', 'female', 'non-binary', 'does not matter']\n"
                        "- walk_time (integer): Maximum minutes to campus by walking\n"
                        "- bike_time (integer): Maximum minutes to campus by biking\n"
                        "- drive_time (integer): Maximum minutes to campus by driving\n"
                        "- pets_allowed (boolean)\n"
                        "- present_pet_types (list of strings): e.g., ['dog', 'cat', etc.]\n"
                        "- furnished (boolean)\n"
                        "- bathroom_count (integer)\n"
                        "- bedroom_count (integer)\n"
                        "- lease_length (string): e.g., '12 months'\n"
                        "- utilities_included (list of strings): e.g., ['water', 'electricity', 'internet']\n"
                        "- ada_accessible (boolean)\n"
                        "- proximity_to_stores (list of strings)\n"
                        "- bus_routes (list of strings)\n"
                        "- nationalities (list of strings)\n"
                        "- deposit_required (integer)\n"
                        "- lease_type (string): e.g., 'Sublease', 'Full Lease'\n"
                        "- square_footage (integer): Minimum square footage\n"
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=250,
            temperature=0,
        )
        criteria_text = response['choices'][0]['message']['content'].strip()
        # Log the AI's response
        logger.info("AI response: %s", criteria_text)

        # Parse the JSON output
        try:
            criteria = json.loads(criteria_text)
        except json.JSONDecodeError as e:
            logger.error("Failed to parse AI response as JSON: %s", e)
            return []

        # Ensure all expected fields are present
        expected_fields = [
            'price', 'roommate_count', 'gender_preferences', 'walk_time', 'bike_time', 'drive_time', 'pets_allowed',
            'present_pet_types', 'furnished', 'bathroom_count', 'bedroom_count', 'lease_length', 'utilities_included', 
            'ada_accessible', 'proximity_to_stores', 'bus_routes', 'nationalities', 'deposit_required', 'lease_type', 
            'square_footage'
        ]

        for field in expected_fields:
            if field not in criteria:
                criteria[field] = None

        return find_matching_listings(criteria)
    except Exception as e:
        logger.error("An error occurred during AI search: %s", e)
        return []


def find_matching_listings(criteria: dict):
    # Start with all posts
   with app.app_context():
    query = Post.query

    # Apply filters based on criteria
    if criteria.get('price') is not None:
        query = query.filter(Post.price <= criteria['price'])

    if criteria.get('roommate_count') is not None:
        query = query.filter(Post.roommate_count == criteria['roommate_count'])

    if criteria.get('gender_preferences') is not None:
        query = query.filter(Post.gender_preferences.contains(criteria['gender_preferences']))

    if criteria.get('walk_time') is not None:
        query = query.filter(Post.walk_time <= criteria['walk_time'])

    if criteria.get('bike_time') is not None:
        query = query.filter(Post.bike_time <= criteria['bike_time'])

    if criteria.get('drive_time') is not None:
        query = query.filter(Post.drive_time <= criteria['drive_time'])

    if criteria.get('pets_allowed') is not None:
        query = query.filter(Post.pets_allowed == criteria['pets_allowed'])

    if criteria.get('furnished') is not None:
        query = query.filter(Post.furnished == criteria['furnished'])

    if criteria.get('bathroom_count') is not None:
        query = query.filter(Post.bathroom_count >= criteria['bathroom_count'])

    if criteria.get('bedroom_count') is not None:
        query = query.filter(Post.bedroom_count >= criteria['bedroom_count'])

    if criteria.get('lease_length') is not None:
        query = query.filter(Post.lease_length == criteria['lease_length'])

    if criteria.get('utilities_included') is not None:
        query = query.filter(Post.utilities_included.contains(criteria['utilities_included']))

    if criteria.get('ada_accessible') is not None:
        query = query.filter(Post.ada_accessible == criteria['ada_accessible'])

    if criteria.get('proximity_to_stores') is not None:
        query = query.filter(Post.proximity_to_stores.contains(criteria['proximity_to_stores']))

    if criteria.get('square_footage') is not None:
        query = query.filter(Post.square_footage >= criteria['square_footage'])

    if criteria.get('present_pet_types') is not None:
        query = query.filter(Post.present_pet_types.contains(criteria['present_pet_types']))

    if criteria.get('bus_routes') is not None:
        query = query.filter(Post.bus_routes.contains(criteria['bus_routes']))

    if criteria.get('nationalities') is not None:
        query = query.filter(Post.nationalities.contains(criteria['nationalities']))

    if criteria.get('deposit_required') is not None:
        query = query.filter(Post.deposit_required <= criteria['deposit_required'])

    if criteria.get('lease_type') is not None:
        query = query.filter(Post.lease_type == criteria['lease_type'])



    # Execute the query
    posts = query.all()

    # Rank the posts based on the number of matching criteria
    ranked_posts = rank_listings(posts, criteria)

    # Convert posts to dictionaries for JSON serialization
    return [post.to_dict() for post in ranked_posts]

def rank_listings(posts, criteria):
    ranked_list = []
    total_criteria = sum(1 for value in criteria.values() if value is not None)

    for post in posts:
        match_count = 0

        # Check each criterion and increment match count
        if criteria.get('price') is not None and post.price <= criteria['price']:
            match_count += 1

        if criteria.get('roommate_count') is not None and post.roommate_count == criteria['roommate_count']:
            match_count += 1

        if criteria.get('gender_preferences') is not None:
            if set(criteria['gender_preferences']).intersection(set(post.gender_preferences or [])):
                match_count += 1

        if criteria.get('walk_time') is not None and post.walk_time <= criteria['walk_time']:
            match_count += 1

        if criteria.get('bike_time') is not None and post.bike_time <= criteria['bike_time']:
            match_count += 1

        if criteria.get('drive_time') is not None and post.drive_time <= criteria['drive_time']:
            match_count += 1

        if criteria.get('pets_allowed') is not None and post.pets_allowed == criteria['pets_allowed']:
            match_count += 1

        if criteria.get('furnished') is not None and post.furnished == criteria['furnished']:
            match_count += 1

        if criteria.get('bathroom_count') is not None and post.bathroom_count >= criteria['bathroom_count']:
            match_count += 1

        if criteria.get('bedroom_count') is not None and post.bedroom_count >= criteria['bedroom_count']:
            match_count += 1

        if criteria.get('lease_length') is not None and post.lease_length == criteria['lease_length']:
            match_count += 1

        if criteria.get('utilities_included') is not None:
            if set(criteria['utilities_included']).issubset(set(post.utilities_included or [])):
                match_count += 1

        if criteria.get('ada_accessible') is not None and post.ada_accessible == criteria['ada_accessible']:
            match_count += 1

        if criteria.get('proximity_to_stores') is not None:
            if set(criteria['proximity_to_stores']).intersection(set(post.proximity_to_stores or [])):
                match_count += 1

        if criteria.get('square_footage') is not None and post.square_footage >= criteria['square_footage']:
            match_count += 1

        if criteria.get('present_pet_types') is not None:
            if set(criteria['present_pet_types']).intersection(set(post.present_pet_types or [])):
                match_count += 1

        if criteria.get('bus_routes') is not None:
            if set(criteria['bus_routes']).intersection(set(post.bus_routes or [])):
                match_count += 1

        if criteria.get('nationalities') is not None:
            if set(criteria['nationalities']).intersection(set(post.nationalities or [])):
                match_count += 1

        if criteria.get('deposit_required') is not None and post.deposit_required <= criteria['deposit_required']:
            match_count += 1

        if criteria.get('lease_type') is not None and post.lease_type == criteria['lease_type']:
            match_count += 1

        # Calculate match score (percentage of criteria matched)
        relevant_criteria_count = sum(1 for field in criteria if criteria[field] is not None)
        match_score = match_count / relevant_criteria_count if relevant_criteria_count > 0 else 0
        ranked_list.append((match_score, post))

    # Sort posts by match score in descending order
    ranked_list.sort(key=lambda x: x[0], reverse=True)

    # Return only the posts, sorted by match score
    return [item[1] for item in ranked_list]

# Optional main block for testing
if __name__ == "__main__":
    app = create_app()  # Create the app before entering context

    with app.app_context():
        prompt = input("Please enter your apartment search query: ")
        results = ai_search(prompt)
        if results:
            print("\nListings Found:")
            for listing in results:
                print(json.dumps(listing, indent=2, default=str))
        else:
            print("No listings found.")
