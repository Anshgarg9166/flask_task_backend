import os

def get_config():
    env = os.getenv("FLASK_ENV", "development")
    if env == "production":
        from .prod import Config
    elif env == "staging":
        from .staging import Config
    else:
        from .dev import Config
    return Config
