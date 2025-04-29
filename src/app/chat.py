from fastapi import HTTPException
import re


class Chat:
    def __init__(self, state=None):
        self.state = state

    @staticmethod
    def get_intent(prompt: str) -> str:
        """
        Determines the appropriate intent based on the prompt using pattern matching.
        """
        prompt = prompt.lower().strip()

        patterns = {
            "greeting": r"\b(hello|hi|hie|hey|good morning|good afternoon|good evening|greetings|howdy)\b",
            "registration": r"\b(register|sign up|join|create account|new user|signup|1)\b",
            "location": r"\b(where|location|branch|directions|find office|nearest|locate|offices|address|2)\b",
            "receipt": r"\b(receipt|confirmation|proof of payment|transaction details|payment proof)\b",
            "complaint": r"\b(complaint|issue|problem|report|bad experience|feedback|issues|4)\b",
            "service_list": r"\b(services|offerings|help|assistance|service|offer|available services|what services|3)\b",
            "faq": r"\b(faq|question|help me with|how do i|can i|what is|why|when|where|who|how)\b",
            "promotion": r"\b(promotions|offers|special rates|exchange rate|discounts|deals)\b",
            "goodbye": r"\b(thank you|thanks|bye|goodbye|i'm good|i'm all set|got it)\b",
        }

        for intent, pattern in patterns.items():
            if re.search(pattern, prompt):
                return intent

        return "unknown"
    
    @staticmethod
    def process_prompt(data: dict) -> dict:
        """
        Processes incoming chat data and validates its structure.
        """
        try:
            platform = data.get("Platform", "whatsapp")
            message = data.get("Body", "").strip().lower()
            sender = data.get("From")

            if not message or not sender:
                return {"error": "Invalid request data, Message or Sender is missing."}

            return {
                "platform": platform,
                "message": message,
                "sender": sender
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Input processing error: {str(e)}")

