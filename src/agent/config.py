from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

@dataclass
class Settings:
    env: str = os.getenv("ENV", "dev")
    cv_path: Path = Path(os.getenv("CV_PATH", "assets/Khalil_Mabok_ATS_CV.docx"))
    cover_letter_template_path: Path = Path(os.getenv("COVER_LETTER_TEMPLATE_PATH", "templates/cover_letter_template.txt"))
    tracking_sheet_path: Path = Path(os.getenv("TRACKING_SHEET_PATH", "assets/Job_Applications_Tracking_Sheet.csv"))

settings = Settings()
