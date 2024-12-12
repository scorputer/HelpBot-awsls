# routes.py
from flask import Blueprint, request, jsonify, render_template, current_app
import openai
from src.app.utils import load_prompt_files

main = Blueprint('main', __name__)

prompt_data_cache = load_prompt_files()
openai.api_key = openai.api_key = openai.api_key = openai.api_key = openai.api_key = openai.api_key = openai.api_key = openai.api_key = openai.api_key

@main.route('/')
def home():
    custom_prompt_enabled = current_app.config.get('CUSTOM_PROMPT_ENABLED', False)
    return render_template('index.html', custom_prompt_enabled=custom_prompt_enabled)

@main.route('/ask', methods=['POST'])
def ask():
    current_app.logger.debug("Processing /ask request.")
    user_input = request.json.get('input')
    role = request.json.get('role', 'general')
    conversation_history = request.json.get('history', [])

    current_app.logger.debug(f"User input: {user_input}, Role: {role}, History: {conversation_history}")

    model = "gpt-3.5-turbo"  # or whichever model you use

    prompt_data = prompt_data_cache.get(role, {
        "system_message": "You are a helpful assistant.",
        "initial_prompt": "How can I assist you?"
    })

    system_message = prompt_data.get('system_message', "You are a helpful assistant.")
    messages = []

    # Add system message
    messages.append({"role": "system", "content": system_message})

    # Add conversation history
    for message in conversation_history:
        # Ensure roles are one of user/assistant
        if message['role'] == 'bot':
            # Convert old 'bot' role to 'assistant'
            message['role'] = 'assistant'
        messages.append(message)

    # Add the user's new input
    messages.append({"role": "user", "content": user_input})

    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages
        )
        bot_response = response.choices[0].message['content'].strip()
        current_app.logger.debug(f"OpenAI response: {bot_response}")
    except Exception as e:
        current_app.logger.exception("Failed to get response from OpenAI.")
        bot_response = "I'm sorry, I'm having trouble processing your request."

    # Update conversation history
    conversation_history.extend([
        {"role": "user", "content": user_input},
        {"role": "assistant", "content": bot_response}
    ])

    return jsonify({"response": bot_response, "history": conversation_history})

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
        prompt = prompt_data_cache.get(role, {
            "system_message": "You are a helpful assistant.",
            "initial_prompt": "How can I assist you?"
        })
        initial_prompt = prompt.get('initial_prompt', "How can I assist you?")
        return jsonify({"initial_prompt": initial_prompt})
    except Exception as e:
        current_app.logger.exception("Failed to fetch initial prompt.")
        return jsonify({"error": str(e)}), 500
