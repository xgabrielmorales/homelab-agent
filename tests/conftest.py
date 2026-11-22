import os

os.environ.update(
    {
        "OPENROUTER_API_KEY": "test",
        "FORGEJO_URL": "http://forgejo.test",
        "FORGEJO_TOKEN": "test",
        "GOTIFY_URL": "http://gotify.test",
        "GOTIFY_TOKEN": "test",
        "LOGFIRE_IGNORE_NO_CONFIG": "1",
        "PYDANTIC_AI_NO_BANNER": "1",
    }
)
