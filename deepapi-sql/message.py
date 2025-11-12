# messages.py

import random  # To return a random message for variation

# Friendly greetings
def get_greeting_response():
    responses = [
        "Hi there! I'm here to help with coding questions 😊",
        "Hello! Ask me anything related to programming.",
        "Hey! Need help with some code?",
        "Welcome back, developer! Let’s solve a problem.",
        "Yo! Ready to code something cool?"
    ]
    return random.choice(responses)

# Decline messages for non-code prompts
def get_decline_message():
    messages = [
        "I'm a coding assistant, please ask me programming-related questions.",
        "Oops! I only support code and development queries.",
        "I'm trained to assist with software and programming. Try a technical question!",
        "Sorry, I can’t answer that. Please stick to code-related prompts.",
        "I’m designed for developers only – please ask me something about coding."
    ]
    return random.choice(messages)
