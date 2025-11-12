def is_greeting(prompt):
    greetings = ["hi", "hello", "hey", "good morning", "good evening", "good afternoon"]
    return any(prompt.lower().strip().startswith(greet) for greet in greetings)