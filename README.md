# HelpBot AWS Lightsail Deployment

## Description

HelpBot is a Flask-based chatbot application utilizing OpenAI's GPT models. This project provides a Dockerized version of the application for deployment on AWS Lightsail.

## Installation

```bash
git clone https://github.com/yourusername/HelpBot-awsls.git
cd HelpBot-awsls
docker build -t helpbot .

### Running Tests with Coverage

We use `pytest` along with `pytest-cov` for coverage reporting:

```bash
pytest --cov=app --cov-report=term-missing tests