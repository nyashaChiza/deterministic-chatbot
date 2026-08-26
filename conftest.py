import os

# Test-only defaults so importing the app (which reads required settings at
# module load time, e.g. src/routes/webhook.py) works without a real .env
# file or Twilio credentials. Real values from the environment always win.
os.environ.setdefault("USE_TWILIO", "0")
os.environ.setdefault("TWILIO_ACCOUNT_SID", "test_account_sid")
os.environ.setdefault("TWILIO_AUTH_TOKEN", "test_auth_token")
os.environ.setdefault("TWILIO_PHONE_NUMBER", "+15550000000")
os.environ.setdefault("RESET_PHRASE", "reset")
os.environ.setdefault("STATE_BACKEND", "memory")
os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")
os.environ.setdefault("BASE_URL", "http://localhost:8000")
