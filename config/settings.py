"""
Application Configuration Settings
Demonstrates production-ready configuration management
"""
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional
import os


class DatabaseSettings(BaseSettings):
    """Database configuration"""
    host: str = Field(default="localhost", description="Database host")
    port: int = Field(default=5432, description="Database port")
    name: str = Field(default="environmental_monitor", description="Database name")
    user: str = Field(default="postgres", description="Database user")
    password: str = Field(default="password", description="Database password")
    
    @property
    def url(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class RedisSettings(BaseSettings):
    """Redis configuration for caching and task queue"""
    host: str = Field(default="localhost", description="Redis host")
    port: int = Field(default=6379, description="Redis port")
    db: int = Field(default=0, description="Redis database number")
    password: Optional[str] = Field(default=None, description="Redis password")
    
    @property
    def url(self) -> str:
        if self.password:
            return f"redis://:{self.password}@{self.host}:{self.port}/{self.db}"
        return f"redis://{self.host}:{self.port}/{self.db}"


class SensorSettings(BaseSettings):
    """IoT Sensor simulation configuration"""
    sampling_interval: int = Field(default=30, description="Sensor sampling interval in seconds")
    num_sensors: int = Field(default=5, description="Number of simulated sensors")
    failure_rate: float = Field(default=0.01, description="Sensor failure probability")
    noise_level: float = Field(default=0.1, description="Sensor noise level")


class MLSettings(BaseSettings):
    """Machine Learning configuration"""
    model_retrain_interval: int = Field(default=3600, description="Model retraining interval in seconds")
    anomaly_threshold: float = Field(default=0.1, description="Anomaly detection threshold")
    prediction_window: int = Field(default=24, description="Prediction window in hours")
    min_training_samples: int = Field(default=1000, description="Minimum samples for training")


class AlertSettings(BaseSettings):
    """Alert and notification configuration"""
    email_enabled: bool = Field(default=True, description="Enable email alerts")
    sms_enabled: bool = Field(default=False, description="Enable SMS alerts")
    email_smtp_host: str = Field(default="smtp.gmail.com", description="SMTP server")
    email_smtp_port: int = Field(default=587, description="SMTP port")
    email_username: str = Field(default="", description="Email username")
    email_password: str = Field(default="", description="Email password")
    alert_cooldown: int = Field(default=300, description="Alert cooldown in seconds")


class APISettings(BaseSettings):
    """API configuration"""
    title: str = Field(default="Environmental Monitor API", description="API title")
    version: str = Field(default="1.0.0", description="API version")
    host: str = Field(default="0.0.0.0", description="API host")
    port: int = Field(default=8000, description="API port")
    debug: bool = Field(default=False, description="Debug mode")
    cors_origins: list = Field(default=["http://localhost:3000"], description="CORS origins")


class Settings(BaseSettings):
    """Main application settings"""
    # Environment
    environment: str = Field(default="development", description="Environment (development/staging/production)")
    debug: bool = Field(default=True, description="Debug mode")
    
    # Logging
    log_level: str = Field(default="INFO", description="Log level")
    log_format: str = Field(default="json", description="Log format (json/text)")
    
    # Security
    secret_key: str = Field(default="your-secret-key-change-in-production", description="Secret key")
    
    # Component Settings
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    redis: RedisSettings = Field(default_factory=RedisSettings)
    sensors: SensorSettings = Field(default_factory=SensorSettings)
    ml: MLSettings = Field(default_factory=MLSettings)
    alerts: AlertSettings = Field(default_factory=AlertSettings)
    api: APISettings = Field(default_factory=APISettings)
    
    class Config:
        env_file = ".env"
        env_nested_delimiter = "__"


# Global settings instance
settings = Settings()

# Environment-specific configurations
def get_settings() -> Settings:
    """Get settings instance - useful for dependency injection"""
    return settings


def is_development() -> bool:
    """Check if running in development mode"""
    return settings.environment == "development"


def is_production() -> bool:
    """Check if running in production mode"""
    return settings.environment == "production"