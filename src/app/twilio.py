from loguru import logger
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client



class TwilioService:
    def __init__(self, account_sid: str, auth_token: str, from_number: str):
        """
        Initialize Twilio client with the provided credentials.

        :param account_sid: Twilio Account SID
        :param auth_token: Twilio Auth Token
        :param from_number: Twilio WhatsApp-enabled phone number
        """
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.from_number = from_number
        self.client = Client(account_sid, auth_token)

    def send_message(self, to: str, body: str) -> dict:
        """
        Send a WhatsApp message using the Twilio API.

        :param to: Recipient's phone number in WhatsApp format (e.g., '1234567890')
        :param body: The message to be sent
        :return: The response from Twilio API, or an error message in case of failure
        """
        try:
            # Ensure that both 'from_' and 'to' numbers are in WhatsApp format
            from_ = f"whatsapp:{self.from_number}"  # Twilio WhatsApp number
            to_ = f"{to}"  # Recipient's phone number in WhatsApp format

            # Attempt to send the message using the Twilio client
            message = self.client.messages.create(
                body=body,
                from_=from_,
                to=to_
            )
            return {"sid": message.sid}  # Return the message SID as a response
        except TwilioRestException as e:
            # Handle Twilio-specific exceptions
            error_message = f"Twilio error: {e.msg}"
            # Optionally log the error for debugging or monitoring purposes
            logger.error(error_message)
            return {"error": error_message}
        except Exception as e:
            # Catch any other general exceptions
            error_message = f"An error occurred: {str(e)}"
            # Optionally log the error for debugging or monitoring purposes
            logger.error(error_message)
            return {"error": error_message}

    def send_media_message(self, to: str, body: str, media_url: str) -> dict:
        """
        Send a WhatsApp media message using Twilio API.

        :param to: Recipient's phone number in WhatsApp format (e.g., '1234567890')
        :param body: The message to be sent
        :param media_url: The URL of the media to send (e.g., image or PDF)
        :return: The response from Twilio API, or an error message in case of failure
        """
        try:
            # Ensure that both 'from_' and 'to' numbers are in WhatsApp format
            from_ = f"whatsapp:{self.from_number}"  # Twilio WhatsApp number
            to_ = f"{to}"  # Recipient's phone number in WhatsApp format

            # Attempt to send the media message using the Twilio client
            message = self.client.messages.create(
                body=body,
                from_=from_,
                to=to_,
                media_url=[media_url]  # Attach the media URL
            )
            return {"sid": message.sid}  # Return the message SID as a response
        except TwilioRestException as e:
            # Handle Twilio-specific exceptions
            error_message = f"Twilio error: {e.msg}"
            # Optionally log the error for debugging or monitoring purposes
            logger.critical(f"from:{self.from_number} to:{to_} body:{body} media_url:{media_url}")
            logger.error(error_message)
            return {"error": error_message}
        except Exception as e:
            # Catch any other general exceptions
            error_message = f"An error occurred: {str(e)}"
            # Optionally log the error for debugging or monitoring purposes
            logger.error(error_message)
            return {"error": error_message}


# Create a function to initialize and send messages
def setup_twilio(account_sid: str, auth_token: str, from_number: str) -> TwilioService:
    """
    Set up and return a TwilioService instance.

    :param account_sid: Twilio Account SID
    :param auth_token: Twilio Auth Token
    :param from_number: Twilio WhatsApp-enabled phone number
    :return: TwilioService instance
    """
    return TwilioService(account_sid, auth_token, from_number)