from fastapi import APIRouter, Request, HTTPException
from loguru import logger
from decouple import config
from src.app import setup_twilio, get_chatbot_instance

router = APIRouter(prefix="/webhook", tags=["Webhook"])
chatbot = get_chatbot_instance()

# Config
USE_TWILIO = config('USE_TWILIO', cast=bool)
TWILIO_ACCOUNT_SID = config('TWILIO_ACCOUNT_SID', default='default')
TWILIO_AUTH_TOKEN = config('TWILIO_AUTH_TOKEN', default='default')
TWILIO_PHONE_NUMBER = config('TWILIO_PHONE_NUMBER', default='default')
RESET_PHRASE = config('RESET_PHRASE', default='reset').lower()

# Twilio client (optional)
twilio_client = setup_twilio(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER)


@router.post("/")
async def webhook(request: Request):
    """
    Handles incoming webhook POST requests from Twilio.
    """
    form_data = await request.form()
    
    try:
        data = chatbot.process_prompt(form_data)
    except HTTPException as e:
        logger.error(f"Validation failed: {e.detail}")
        raise

    sender = data["sender"]
    message = data["message"]

    logger.info(f"[{sender}] initial state: {chatbot.state._state}")

    # Check for reset phrase
    if message == RESET_PHRASE:
        chatbot.state.clear_state(sender)
        response = chatbot.intent_actions.get("reset")()
    else:
        # Stateful interaction
        current_state = chatbot.state.get_state(sender)
        if current_state:
            intent = current_state.get("intent")
            response = chatbot.intent_actions.get(intent)(data)
        else:
            # New interaction
            intent = chatbot.get_intent(message)
            logger.critical({**data, "intent": intent})
            chatbot.state.set_state(sender, {**data, "intent": intent})
            response = chatbot.intent_actions.get(intent)(data)

    # Send response via Twilio (if enabled)
    if USE_TWILIO and "message" in response:
        twilio_client.send_message(sender, response["message"])

    logger.info(f"[{sender}] final state: {chatbot.state._state}")

    return response
