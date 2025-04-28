from fastapi import HTTPException
import re


class Chat:
    def __init__(self, state):
        self.state = state

    def get_intent(prompt: str) -> str:
        """
        Determines the appropriate endpoint based on keywords or prompt patterns.
        """

        prompt = prompt.lower().strip()

        # Greetings and pleasantries
        if re.search(r"\b(hello|hi|hie|hey|good morning|good afternoon|good evening|greetings|howdy)\b", prompt):
            return "greeting"

        # Registration-related keywords
        if re.search(r"\b(register|sign up|join|create account|new user|signup|1)\b", prompt):
            return "registration"

        # Location inquiries
        if re.search(r"\b(where|location|branch|directions|find office|nearest|find|locate|offices|address|2)\b", prompt):
            return "location"

        # Receipt-related keywords
        if re.search(r"\b(receipt|confirmation|proof of payment|transaction details|payment proof)\b", prompt):
            return "receipt"

        # Complaint-related keywords
        if re.search(r"\b(complaint|issue|problem|report|bad experience|feedback|issues|4)\b", prompt):
            return "complaint"

        # Service-related keywords
        if re.search(r"\b(services|offerings|help|assistance|service|offer|available services|list of services|what services|3)\b", prompt):
            return "service_list"

        # FAQ-related keywords
        if re.search(r"\b(faq|question|help me with|how do i|can i|what is|why|when|where|who|how)\b", prompt):
            return "faq"

        # Marketing/Promotional inquiries
        if re.search(r"\b(promotions|offers|special rates|exchange rate|discounts|deals)\b", prompt):
            return "promotion"

        # Conversation closure cues
        if re.search(r"\b(thank you|thanks|bye|goodbye|i'm good|i'm all set|got it)\b", prompt):
            return "goodbye"

        # Default fallback
        return "unknown"
        


    def process_prompt(data: dict) -> dict:
        """
        Processes incoming messages from WhatsApp or Facebook.
        Extracts message text and sender details.
        """
        try:
            platform = data.get("platform")  # e.g., 'whatsapp' or 'facebook'
            message = data.get("message", "").strip().lower()
            sender = data.get("sender")

            if not message or not sender:
                raise ValueError("Invalid input data")

            return {
                "platform": platform,
                "message": message,
                "sender": sender
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Input processing error: {str(e)}")