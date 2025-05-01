
# Deterministic Chatbot

A conversational assistant designed to streamline remittance-related inquiries, providing users with accurate and timely information through natural language interactions.

## Features

- **Intent Recognition**: Utilizes pattern matching to discern user intents from messages.
- **State Management**: Maintains conversational context for seamless interactions.
- **Extensible Intent Handlers**: Easily add or modify functionalities by updating intent actions.
- **Twilio Integration**: Supports WhatsApp messaging via Twilio API.
- **Error Handling**: Gracefully manages unexpected inputs and system errors. 

## Folder Structure


```bash
remittance-chatbot/
├── .github/workflows/        # GitHub Actions workflows for CI/CD
├── .vscode/                  # VSCode-specific settings
├── src/                      # Core application source code
│   ├── app/
│   │   ├── __init__.py
│   │   ├── chatbot.py        # Chat class handling intents and state
│   │   ├── intent_actions.py # Functions mapping intents to responses
│   │   ├── state.py          # State management utilities
│   │   ├── model.py          # Model file for the table schema
│   │   └── twilio.py         # Twilio client setup
├── tests/                    # Unit and integration tests
│   └── test_main.py
├── .gitignore
├── LICENSE
├── README.md
├── main.py                   # FastAPI application entry point
├── env_example               # Sample environment variables file
├── requirements.txt          # Python dependencies
└── main.py                   # Application runner
```


## Getting Started

### Prerequisites

- Python 3.13 or higher
- Twilio account (for WhatsApp integration)

### Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/nyashaChiza/remittance-chatbot.git
   cd remittance-chatbot
   ```


2. **Create and activate a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```


3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```


4. **Configure environment variables**:

   - Rename `env_example` to `.env`.
   - Update the `.env` file with your Twilio credentials and desired settings.

### Running the Application


```bash
uvicorn src.main:app --reload
```


The application will be accessible at `http://127.0.0.1:8000`.

## Usage

- Send a POST request to the `/webhook/` endpoint with form data containing:
  - `From`: Sender's identifier (e.g., WhatsApp number).
  - `Body`: Message content.

- The chatbot will process the message, determine the intent, and respond accordingly.

## Testing


```bash
pytest
```


This will execute the test suite located in the `tests/` directory.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the [GPL-3.0 License](LICENSE).

## Acknowledgments

Developed by [Nyasha Chizampeni](https://github.com/nyashaChiza) 

---

Feel free to customize this `README.md` further to match any additional specifics or preferences you have for your project. 
