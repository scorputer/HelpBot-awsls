# app/utils.py

import os
import json
import logging


def load_prompt_files():
    logger = logging.getLogger(__name__)
    logger.info("Loading prompt files...")

    # Adjust the path to the prompts directory
    prompt_directory = os.path.join(
        os.path.dirname(__file__),
        '..',
        'prompts'
    )
    logger.debug(f"Prompt directory: {prompt_directory}")

    if not os.path.exists(prompt_directory):
        logger.error(f"Prompts directory not found at {prompt_directory}")
        return {}

    prompt_files = [
        f for f in os.listdir(prompt_directory)
        if f.endswith('.json')
    ]
    logger.debug(f"Prompt files found: {prompt_files}")

    prompt_data_cache = {}
    for file_name in prompt_files:
        file_path = os.path.join(prompt_directory, file_name)
        try:
            with open(file_path, 'r') as file:
                prompt_data = json.load(file)
                key = file_name.rsplit('.', 1)[0]
                prompt_data_cache[key] = prompt_data
                logger.debug(f"Loaded prompt for role: {key}")
        except Exception as e:
            logger.exception(f"Failed to load prompt file {file_name}: {e}")

    logger.info("Prompt files loaded successfully.")
    return prompt_data_cache
