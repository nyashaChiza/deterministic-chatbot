from fastapi import APIRouter, Depends, Request
from loguru import logger
from decouple import config
from src.app import setup_twilio, Chat, State

router = APIRouter(prefix="/webhook", tags=["Webhook"])
state = State()  # Initialize the state management
chatbot = Chat(state)

USE_TWILIO = config('USE_TWILIO', cast=bool)  # Set to True to use Twilio for messaging
TWILIO_ACCOUNT_SID = config('TWILIO_ACCOUNT_SID', 'default')  # Your Twilio account SID
TWILIO_AUTH_TOKEN = config('TWILIO_AUTH_TOKEN', 'default')  # Your Twilio auth token
TWILIO_PHONE_NUMBER = config('TWILIO_PHONE_NUMBER', 'default')  # Your Twilio phone number
RESET_PHRASE = config('RESET_PHRASE', 'default')  # The phrase to reset the conversation

# Set up Twilio client via the wrapper
twilio_client = setup_twilio(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER)

@router.post("/")
async def webhook(request: Request):
    form_data = await request.form()
    data = chatbot.process_prompt(form_data)

    # Exact match for reset
    if data.get('message') == RESET_PHRASE:
        chatbot.state.clear_state(data.get('sender'))