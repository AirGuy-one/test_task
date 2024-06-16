from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_key: bool = Field(title='API key of exchange money rate website')
    exchange_rate_base_url: str = Field('https://v6.exchangerate-api.com/v6/')

    @property
    def exchange_rate_url(self) -> str:
        return f"{self.exchange_rate_base_url}/{self.api_key}/latest/"

    class Config:
        env_file = ".env"


settings = Settings()
