from os import environ as env
import logging


class Config:
    DEBUG = bool(env.get("APP_CLIENT_DEBUG", False))
    APP_PORT = env.get("APP_CLIENT_PORT", 80)
    APP_DATABASE = env.get("APP_DATABASE", "sqlite+aiosqlite:///clients.db")
    APP_HOST = env.get("APP_HOST","0.0.0.0")


logging.basicConfig(
    level=Config.DEBUG,
    format="%(levelname)s: %(asctime)s - %(name)s - %(funcName)s - %(message)s",
    handlers=[
        logging.FileHandler("client_service.log"),
        logging.StreamHandler()
    ]
)
