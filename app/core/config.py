from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str = "postgresql://postgres:mysecretpassword@db:5432/postgres"
    MQTT_BROKER_URL: str = "217.120.251.115"
    MQTT_BROKER_PORT: int = 5683
    MQTT_USERNAME: str = "lyvmqttuser"
    MQTT_PASSWORD: str = "lyvmqttuser"


settings = Settings()
