from dataclasses import dataclass
from typing import List

@dataclass
class JobDescription:
    company: str
    role_title: str
    location: str
    description: str
    requirements: List[str]
    source_link: str = ""

@dataclass
class TailoredOutputs:
    cover_letter_text: str
    match_score: float
    jd_keywords: List[str]
    cover_letter_path: str
    checklist_path: str
