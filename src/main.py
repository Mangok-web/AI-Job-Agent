from agent.data_models import JobDescription
from agent.pipeline import tailor_cover_letter, update_tracking_sheet
from pathlib import Path

def main():
    jd = JobDescription(
        company="AcmeAI",
        role_title="Machine Learning Engineer",
        location="Remote, UK/EU",
        source_link="https://acme.ai/careers/ml-engineer"
    )
    outputs = tailor_cover_letter(jd, Path("outputs"))
    csv_path = update_tracking_sheet(jd, outputs)
    print("Cover letter:", outputs.cover_letter_path)
    print("Checklist:", outputs.checklist_path)
    print("Tracking updated:", csv_path)

if __name__ == "__main__":
    main()
