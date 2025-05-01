# intent_actions.py
from src.app.state import get_state_instance


def handle_greeting(data=None):
    state = get_state_instance()
    # state.set_state(data.get('sender'), data)  # Set the state for the sender
    return {"message": "Hello! How can I assist you today?"}

def handle_goodbye(data=None):
    state = get_state_instance()
    state.clear_state(data.get('sender'))  # Clear the state for the sender
    return {"message": "Goodbye! If you have any more questions, I'm just a message away. Stay safe!"}

def handle_unknown(data=None):
    state = get_state_instance()
    return {"message": "I'm sorry, I didn't understand that. Can you rephrase?"}

def handle_reset(data=None):
    state = get_state_instance()
    return {"message": "Your conversation has been reset. How can I assist you today?"}

# Intent to action mapping
INTENT_ACTIONS = {
    "greeting": handle_greeting,
    "good_bye": handle_goodbye,
    "unknown": handle_unknown,
    "reset": handle_reset,
}
