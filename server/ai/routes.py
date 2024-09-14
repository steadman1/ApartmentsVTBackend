from flask import Blueprint, request, jsonify, abort
from .ai_search import ai_search

# Define the AI blueprint
ai_bp = Blueprint('ai', __name__)

@ai_bp.route('/search/ai', methods=['POST'])
def search_with_ai():
    data = request.get_json()
    if not data or 'prompt' not in data:
        abort(400, description="Request must contain 'prompt' field.")
    prompt = data.get('prompt')
    if not prompt or not isinstance(prompt, str):
        abort(400, description="Invalid 'prompt' provided. It must be a non-empty string.")
    results = ai_search(prompt)
    if results:
        return jsonify({"success": True, "listings": results}), 200
    else:
        return jsonify({"success": False, "error": "No listings found."}), 404
