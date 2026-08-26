import pytest
from fastapi import HTTPException

from src.app.chat import Chat
from src.app.state import MemoryState


@pytest.mark.parametrize(
    "message,expected_intent",
    [
        ("hello there", "greeting"),
        ("Hi!", "greeting"),
        ("Good morning", "greeting"),
        ("thanks a lot", "good_bye"),
        ("bye", "good_bye"),
        ("got it", "good_bye"),
        ("what time is it", "unknown"),
    ],
)
def test_get_intent(message, expected_intent):
    assert Chat.get_intent(message) == expected_intent


def test_process_prompt_returns_normalized_fields():
    chat = Chat(state=MemoryState())
    result = chat.process_prompt({"From": "+15550000000", "Body": "  Hello There  "})
    assert result == {
        "platform": "whatsapp",
        "message": "hello there",
        "sender": "+15550000000",
    }


def test_process_prompt_respects_explicit_platform():
    chat = Chat(state=MemoryState())
    result = chat.process_prompt({"From": "+15550000000", "Body": "hi", "Platform": "sms"})
    assert result["platform"] == "sms"


def test_process_prompt_missing_sender_raises_http_exception():
    chat = Chat(state=MemoryState())
    with pytest.raises(HTTPException) as exc_info:
        chat.process_prompt({"Body": "hello"})
    assert exc_info.value.status_code == 400


def test_process_prompt_missing_message_raises_http_exception():
    chat = Chat(state=MemoryState())
    with pytest.raises(HTTPException) as exc_info:
        chat.process_prompt({"From": "+15550000000"})
    assert exc_info.value.status_code == 400
