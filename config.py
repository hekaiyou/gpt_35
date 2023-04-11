from pydantic import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str = ''


settings_describe = {
    'openai_api_key': 'OpenAI API key',
}
