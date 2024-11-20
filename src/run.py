# run.py

from app import create_app
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--custom-prompt', action='store_true', help="Enable custom prompt feature")
args = parser.parse_args()

app = create_app()
app.config['CUSTOM_PROMPT_ENABLED'] = args.custom_prompt

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
