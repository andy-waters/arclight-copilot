# arclight/config.py
import os
from dataclasses import dataclass

from dotenv import load_dotenv

# Ensure .env is loaded as soon as this module is imported
load_dotenv()


@dataclass
class Settings:
    aoai_endpoint: str | None = os.getenv("AZURE_OPENAI_ENDPOINT")
    aoai_key: str | None = os.getenv("AZURE_OPENAI_API_KEY") or os.getenv(
        "AZURE_OPENAI_KEY"
    )
    aoai_deployment: str | None = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    aoai_api_version: str | None = os.getenv("AZURE_OPENAI_API_VERSION", "2024-06-01")

    # Azure AI Search (optional)
    search_endpoint: str | None = os.getenv("AZURE_SEARCH_ENDPOINT")
    search_key: str | None = os.getenv("AZURE_SEARCH_KEY")
    search_index: str | None = os.getenv("AZURE_SEARCH_INDEX")

    @property
    def demo_mode(self) -> bool:
        return not (self.aoai_endpoint and self.aoai_key and self.aoai_deployment)


SETTINGS = Settings()
