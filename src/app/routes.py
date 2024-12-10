# app/routes.py

from flask import Blueprint, request, jsonify, render_template, current_app
import os
import openai
from .utils import load_prompt_files


main = Blueprint('main', __name__)

# Load prompts
prompt_data_cache = load_prompt_files()

# Initialize OpenAI client
openai.api_key = os.getenv('OPENAI_API_KEY')
if not openai.api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")


@main.route('/')
def home():
    current_app.logger.debug("Rendering home page.")
    custom_prompt_enabled = current_app.config.get(
        'CUSTOM_PROMPT_ENABLED',
        False
    )
    return render_template(
        'index.html',
        custom_prompt_enabled=custom_prompt_enabled
    )


@main.route('/ask', methods=['POST'])
def ask():
    current_app.logger.debug("Processing /ask request.")
    user_input = request.json.get('input')
    role = request.json.get('role', 'general')
    conversation_history = request.json.get('history', [])

    current_app.logger.debug(f"User input: {user_input}")
    current_app.logger.debug(f"Role: {role}")
    current_app.logger.debug(f"Conversation history: {conversation_history}")

    model = "gpt-3.5-turbo"
    prompt_data = prompt_data_cache.get(
        role,
        {
            "bot_description": "You are a helpful assistant.",
            "guidelines": {"initial_prompt": "How can I assist you?"}
        }
    )

    messages = []
    # Add system message with bot description
    messages.append(
        {"role": "system", "content": prompt_data['bot_description']}
    )

    # Add conversation history
    for message in conversation_history:
        messages.append(
            {"role": message['role'], "content": message['content']}
        )
        current_app.logger.debug(f"Added to messages: {message}")

    # Add the latest user input
    messages.append({"role": "user", "content": user_input})
    current_app.logger.debug(
        "Final messages sent to OpenAI: {}".format(messages)
    )

    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages
        )
        bot_response = response.choices[0].message['content'].strip()
        current_app.logger.debug(f"OpenAI response: {bot_response}")
    except Exception:
        current_app.logger.exception("Failed to get response from OpenAI.")
        bot_response = "I'm sorry, I'm having trouble processing your request."

    # Update conversation history
    conversation_history.extend([
        {"role": "user", "content": user_input},
        {"role": "assistant", "content": bot_response}
    ])

    return jsonify(
        {"response": bot_response, "history": conversation_history}
    )


@main.route('/roles', methods=['GET'])
def get_roles():
    current_app.logger.debug("Fetching available roles.")
    roles = [{"name": "General Use", "value": "general"}]
    for key, value in prompt_data_cache.items():
        if 'name' in value:
            roles.append({"name": value['name'], "value": key})
    current_app.logger.debug(f"Available roles: {roles}")
    return jsonify(roles)


@main.route('/prompt/<role>', methods=['GET'])
def get_initial_prompt(role):
    current_app.logger.debug(f"Fetching initial prompt for role: {role}")
    try:
        prompt = prompt_data_cache.get(
            role,
            {"guidelines": {"initial_prompt": "How can I assist you?"}}
        )
        initial_prompt = prompt['guidelines']['initial_prompt']
        current_app.logger.debug(f"Initial prompt: {initial_prompt}")
        return jsonify({"initial_prompt": initial_prompt})
    except Exception as e:
        current_app.logger.exception("Failed to fetch initial prompt.")
        return jsonify({"error": str(e)}), 500


@main.route('/custom_prompt', methods=['POST'])
def custom_prompt():
    current_app.logger.debug("Processing /custom_prompt request.")
    if not current_app.config.get('CUSTOM_PROMPT_ENABLED', False):
        current_app.logger.warning("Custom prompt feature is disabled.")
        return jsonify({"error": "Custom prompt feature is disabled."}), 403

    custom_input = request.json.get('input')
    conversation_history = request.json.get('history', [])

    current_app.logger.debug(f"Custom input: {custom_input}")
    current_app.logger.debug(
        f"Conversation history: {conversation_history}"
    )

    model = "gpt-3.5-turbo"

    messages = []
    # Add system message with the custom prompt
    messages.append({"role": "system", "content": custom_input})

    # Add conversation history
    for message in conversation_history:
        messages.append(
            {"role": message['role'], "content": message['content']}
        )
        current_app.logger.debug(f"Added to messages: {message}")

    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages
        )
        bot_response = response.choices[0].message['content'].strip()
        current_app.logger.debug(f"OpenAI response: {bot_response}")
    except Exception:
        current_app.logger.exception("Failed to process custom prompt.")
        bot_response = "I'm sorry, I'm having trouble processing your request."

    # Update conversation history
    conversation_history.extend([
        {"role": "user", "content": custom_input},
        {"role": "assistant", "content": bot_response}
    ])

    return jsonify(
        {"response": bot_response, "history": conversation_history}
    )
