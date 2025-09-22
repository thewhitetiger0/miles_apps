from pydantic_settings import BaseSettings, SettingsConfigDict


class _Config(BaseSettings):
    # tell Pydantic to auto-load from .env
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # discord bots
    notifymorales_bot_discord_token: str
    automations_bot_discord_token: str
    tester_bot_discord_token: str


config = _Config()
