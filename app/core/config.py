from pydantic_settings import BaseSettings

class Settings(BaseSettings):

	PROJECT_NAME: str = "MedVoice"
	ENV: str = "development"
	OPENAI_API_KEY: str | None = None
	DATABASE_URL: str

	class Config:
		env_file = ".env"



settings = Settings()
