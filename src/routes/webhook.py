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
    try:
        form_data = await request.form()
        data = chatbot.process_prompt(form_data)

        sender = data["sender"]
        message = data["message"]
        current_state = chatbot.state.get_state(sender)

        logger.info(f"[{sender}] initial state: {chatbot.state.get_all()}")

        # Step 1: Handle reset
        if message == RESET_PHRASE:
            chatbot.state.clear_state(sender)
            intent = "reset"
        else:
            # Step 2: Detect intent from current message
            detected_intent = chatbot.get_intent(message)
            logger.critical({**data, "intent": detected_intent})

            if detected_intent in chatbot.intent_actions:
                intent = detected_intent
                chatbot.state.set_state(sender, {**data, "intent": intent})
            else:
                intent = "unknown"

        # Step 3: Get handler
        handler = chatbot.intent_actions.get(intent, chatbot.intent_actions["unknown"])

        # Step 4: Generate response
        response = handler({**data, "intent": intent})

        # Step 5: Send via Twilio if configured
        if USE_TWILIO and "message" in response:
            twilio_client.send_message(sender, response["message"])

        logger.info(f"[{sender}] final state: {chatbot.state.get_all()}")

        return response

    except Exception as e:
        logger.exception("Webhook processing error")

        fallback_response = {
            "message": "Sorry, something went wrong on our end. Please try again later."
        }

        if USE_TWILIO:
            sender = form_data.get("From")
            if sender:
                twilio_client.send_message(sender, fallback_response["message"])

        return fallback_response

