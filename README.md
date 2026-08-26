
# Deterministic Chatbot

A conversational assistant designed to streamline inquiries, providing users with accurate and timely information through natural language interactions.

## Features

- **Intent Recognition**: Utilizes pattern matching to discern user intents from messages.
- **State Management**: Maintains conversational context for seamless interactions.
- **Extensible Intent Handlers**: Easily add or modify functionalities by updating intent actions.
- **Twilio Integration**: Supports WhatsApp messaging via Twilio API.
- **Error Handling**: Gracefully manages unexpected inputs and system errors.

## Folder Structure


```bash
Deterministic-chatbot/
├── .github/
│   ├── workflows/             # GitHub Actions CI workflow
│   └── dependabot.yml         # Automated dependency update PRs
├── .vscode/                   # VSCode-specific settings
├── src/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── chat.py            # Chat class handling intents and prompt processing
│   │   ├── intent_actions.py  # Functions mapping intents to responses
│   │   ├── state.py           # State management (in-memory or SQLite)
│   │   ├── model.py           # SQLAlchemy table schema
│   │   └── twilio.py          # Twilio client setup
│   └── routes/
│       ├── __init__.py
│       ├── webhook.py         # POST /webhook/ - main chat endpoint
│       └── callback.py        # POST /status-callback/ - Twilio status callback
├── tests/                     # Unit and integration tests
│   ├── test_main.py
│   ├── test_state.py
│   ├── test_chat.py
│   └── test_webhook.py
├── conftest.py                # Shared pytest env-var setup
├── .env.example                # Sample environment variables file
├── .flake8                    # Lint configuration
├── Dockerfile
├── .gitignore
├── LICENSE
├── README.md
├── main.py                    # FastAPI application entry point
├── requirements.in            # Direct runtime dependencies (source)
├── requirements.txt           # Fully pinned runtime dependencies (lock)
├── requirements-dev.in        # Direct dev/test dependencies (source)
└── requirements-dev.txt       # Fully pinned dev/test dependencies (lock)
```


## Getting Started

### Prerequisites

- Python 3.13 or higher
- Twilio account (for WhatsApp integration)

### Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/nyashaChiza/deterministic-chatbot.git
   cd deterministic-chatbot
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

   For local development (tests, linting), also install the dev dependencies:

   ```bash
   pip install -r requirements-dev.txt
   ```


4. **Configure environment variables**:

   - Copy `.env.example` to `.env`.
   - Update the `.env` file with your Twilio credentials and desired settings.

### Running the Application


```bash
uvicorn main:app --reload
```


The application will be accessible at `http://127.0.0.1:8000`.

### Running with Docker

```bash
docker build -t deterministic-chatbot .
docker run --env-file .env -p 8000:8000 deterministic-chatbot
```

## Usage

- Send a POST request to the `/webhook/` endpoint with form data containing:
  - `From`: Sender's identifier (e.g., WhatsApp number).
  - `Body`: Message content.

- The chatbot will process the message, determine the intent, and respond accordingly.

## Testing


```bash
pip install -r requirements-dev.txt
pytest
```


This will execute the full test suite located in the `tests/` directory (intent detection, prompt validation, state backends, and the `/webhook/` endpoint).

## Linting

```bash
flake8 .
```

CI runs this on every push/PR and fails the build on style or complexity violations.

## Dependency updates

`requirements.txt` and `requirements-dev.txt` are the pinned, installable lockfiles. `requirements.in` and `requirements-dev.in` list the direct dependencies they were compiled from (via [pip-tools](https://pypi.org/project/pip-tools/)):

```bash
pip install pip-tools
pip-compile requirements.in
pip-compile requirements-dev.in
```

[Dependabot](.github/dependabot.yml) opens a weekly PR for outdated pip and GitHub Actions dependencies.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the [GPL-3.0 License](LICENSE).

## Acknowledgments

Developed by [Nyasha Chizampeni](https://github.com/nyashaChiza) 

---


