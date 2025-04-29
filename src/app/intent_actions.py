# intent_actions.py

def handle_greeting(data=None):
    return {"message": "Hello! How can I assist you today?"}

def handle_goodbye(data=None):
    return {"message": "Goodbye! If you have any more questions, I'm just a message away. Stay safe!"}

def handle_unknown(data=None):
    return {"message": "I'm sorry, I didn't understand that. Can you rephrase?"}

# Intent to action mapping
INTENT_ACTIONS = {
    "greeting": handle_greeting,
    "registration": handle_goodbye,
    "unknown": handle_unknown,
}
