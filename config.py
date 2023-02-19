from pydantic import BaseSettings


class Settings(BaseSettings):
    database_hostname: str = 'localhost'
    database_port: str = 3306
    database_password: str = 1234
    database_name: str = 'fastapi'
    database_username: str = 'root'
    secret_key: str = "VHKJFABNVIJFEBVHLEFBAIVFEAOVI"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60


settings = Settings()