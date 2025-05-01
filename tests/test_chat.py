import pytest
from fastapi import HTTPException
from src.app.chat import Chat

@pytest.fixture
def chat_instance():
    """Fixture to create a Chat instance."""
    return Chat()

def test_get_intent_greeting(chat_instance):
    """Test the get_intent method for a greeting intent."""
    prompt = "Hello, how are you?"
    intent = chat_instance.get_intent(prompt)
    assert intent == "greeting"

def test_get_intent_goodbye(chat_instance):
    """Test the get_intent method for a goodbye intent."""
    prompt = "Thanks, bye!"
    intent = chat_instance.get_intent(prompt)
    assert intent == "good_bye"

def test_get_intent_unknown(chat_instance):
    """Test the get_intent method for an unknown intent."""
    prompt = "What is the weather today?"
    intent = chat_instance.get_intent(prompt)
    assert intent == "unknown"

def test_process_prompt_valid_data(chat_instance):
    """Test the process_prompt method with valid data."""
    data = {
        "Platform": "whatsapp",
        "Body": "Hello!",
        "From": "+1234567890"
    }
    result = chat_instance.process_prompt(data)
    assert result == {
        "platform": "whatsapp",
        "message": "hello!",
        "sender": "+1234567890"
    }

def test_process_prompt_missing_fields(chat_instance):
    """Test the process_prompt method with missing fields."""
    data = {
        "Body": "Hello!"
    }
    with pytest.raises(HTTPException) as exc_info:
        chat_instance.process_prompt(data)
    assert exc_info.value.status_code == 422
    assert "Missing required fields" in exc_info.value.detail

def test_process_prompt_empty_message(chat_instance):
    """Test the process_prompt method with an empty message."""
    data = {
        "Platform": "whatsapp",
        "Body": "",
        "From": "+1234567890"
    }
    with pytest.raises(HTTPException) as exc_info:
        chat_instance.process_prompt(data)
    assert exc_info.value.status_code == 422
    assert "Missing required fields" in exc_info.value.detail