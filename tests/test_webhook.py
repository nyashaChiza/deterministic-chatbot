from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_webhook_greeting():
    response = client.post(
        "/webhook/", data={"From": "whatsapp:+10000000001", "Body": "Hello"}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Hello! How can I assist you today?"}


def test_webhook_goodbye():
    response = client.post(
        "/webhook/", data={"From": "whatsapp:+10000000002", "Body": "thanks"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "Goodbye! If you have any more questions, I'm just a message away. Stay safe!"
    }


def test_webhook_reset():
    response = client.post(
        "/webhook/", data={"From": "whatsapp:+10000000003", "Body": "reset"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "Your conversation has been reset. How can I assist you today?"
    }


def test_webhook_unknown_intent():
    response = client.post(
        "/webhook/", data={"From": "whatsapp:+10000000004", "Body": "asdkjalksdj"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "I'm sorry, I didn't understand that. Can you rephrase?"
    }


def test_webhook_missing_body_returns_fallback_message():
    response = client.post("/webhook/", data={"From": "whatsapp:+10000000005"})
    assert response.status_code == 200
    assert response.json() == {
        "message": "Sorry, something went wrong on our end. Please try again later."
    }


def test_webhook_form_parsing_failure_returns_fallback_without_crashing():
    # Regression test: the except block used to reference `form_data` even
    # though it was only ever assigned *inside* the try - if awaiting
    # request.form() itself is what raised, that branch raised a fresh
    # NameError instead of returning the fallback response.
    with patch("starlette.requests.Request.form", new=AsyncMock(side_effect=Exception("boom"))):
        response = client.post("/webhook/", data={"From": "whatsapp:+10000000006", "Body": "hi"})

    assert response.status_code == 200
    assert response.json() == {
        "message": "Sorry, something went wrong on our end. Please try again later."
    }
