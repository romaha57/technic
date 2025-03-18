from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    API_KEY: str

    class Config:
        env_file_encoding = 'utf-8'
        env_file = '../.env'


settings = Settings()
