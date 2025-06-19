from pydantic import Field
from pydantic_settings import BaseSettings

from dotenv import load_dotenv
load_dotenv(".env")  # ✅ 무조건 Settings보다 먼저

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "원 마 솔 Assistant"
    DB_URL: str = Field(..., env="DB_URL")
    SECRET_KEY: str = Field(..., env="SECRET_KEY")  # ← 여기에 추가!
    GOOGLE_CLIENT_ID: str = Field(..., env="GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET: str = Field(..., env="GOOGLE_CLIENT_SECRET")
    CLOVA_OCR_APIGW_URL: str = Field(..., env="CLOVA_OCR_APIGW_URL")
    CLOVA_OCR_SECRET_KEY: str = Field(..., env="CLOVA_OCR_SECRET_KEY")
##    MODEL_ENDPOINT: str = Field(..., env="MODEL_ENDPOINT")
##    OCR_ENDPOINT: str   = Field(..., env="OCR_ENDPOINT")

    # JWT Settings
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60  # 60분
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7일

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
