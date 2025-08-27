from agent.data_models import JobDescription
from agent.pipeline import tailor_cover_letter, update_tracking_sheet
from pathlib import Path

def main():
    jd = JobDescription(
        company="DeepMind",
        role_title="AI Engineer",
        location="London, UK",
        description=(Path("samples/jd_ai_engineer.txt").read_text(encoding="utf-8")),
        requirements=[
            "Python",
            "TensorFlow or PyTorch",
            "Experience with ML pipelines",
            "SQL and data manipulation",
        ],
        source_link="https://deepmind.com/careers/ai-engineer",
    )
    outputs = tailor_cover_letter(jd, Path("outputs"))
    csv_path = update_tracking_sheet(jd, outputs)
    print("Cover letter:", outputs.cover_letter_path)
    print("Checklist:", outputs.checklist_path)
    print("Tracking updated:", csv_path)

if __name__ == "__main__":
    main()
