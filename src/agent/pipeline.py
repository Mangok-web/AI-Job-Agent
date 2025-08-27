from .data_models import JobDescription, TailoredOutputs
from .config import settings
from pathlib import Path
import pandas as pd
import re
from datetime import date

def extract_keywords(text: str):
    words = re.findall(r"[A-Za-z]+", text.lower())
    focus = {"python","pytorch","tensorflow","scikit","sklearn","sql","numpy","pandas","ml","machine","learning","nlp","vision","cnn"}
    found = sorted(set(w for w in words if w in focus))
    return found

def score_match(keywords, required):
    if not required:
        return 0.0
    found = sum(1 for r in required if any(r.lower() in k for k in keywords))
    return round(100.0 * found / len(required), 1)

def bulletize(items):
    return "\n- " + "\n- ".join(items) if items else "\n- (fill after review)"

def generate_submission_checklist(jd: JobDescription, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    fname_base = f"{jd.company.replace(' ','_')}_{jd.role_title.replace(' ','_')}"
    checklist_path = out_dir / f"{fname_base}_submission_checklist.txt"
    checklist = f"""SUBMISSION CHECKLIST
Company: {jd.company}
Role: {jd.role_title}
Location: {jd.location}
Source Link: {jd.source_link or '(add link)'} 

Pre-submit review:
[ ] Verify site ToS (no automation if disallowed)
[ ] CV highlights top 3 JD requirements
[ ] Cover letter cites 2–3 exact JD requirements
[ ] Verify name, phone, email
[ ] Attach CV + paste text if portal requests
[ ] Add portfolio/GitHub if relevant
[ ] Save confirmation/screenshot

Follow-up:
[ ] +7 days
[ ] +14 days
"""
    checklist_path.write_text(checklist, encoding="utf-8")
    return checklist_path

def tailor_cover_letter(jd: JobDescription, out_dir: Path) -> TailoredOutputs:
    template = settings.cover_letter_template_path.read_text(encoding="utf-8")
    jd_keywords = extract_keywords(jd.description + " " + " ".join(jd.requirements))
    match = score_match(jd_keywords, jd.requirements)
    text = template.format(
        role_title=jd.role_title,
        company=jd.company,
        requirements_bulleted=bulletize(jd.requirements),
        skills_matched=", ".join(jd_keywords[:6]) if jd_keywords else "Python, TensorFlow, PyTorch",
        impact_statement="accelerate model development and improve code quality",
        team_or_product="your AI team",
    )
    out_dir.mkdir(parents=True, exist_ok=True)
    fname_base = f"{jd.company.replace(' ','_')}_{jd.role_title.replace(' ','_')}"
    cl_path = out_dir / f"{fname_base}_cover_letter.txt"
    cl_path.write_text(text, encoding="utf-8")
    checklist_path = generate_submission_checklist(jd, out_dir)
    return TailoredOutputs(text, match, jd_keywords, str(cl_path), str(checklist_path))

def update_tracking_sheet(jd: JobDescription, outputs: TailoredOutputs):
    csv_path = settings.tracking_sheet_path
    cols = ["Date Found","Company","Role","Location","Source Link","Match Score","JD Keywords","Notes","CV File","Cover Letter File","Status","Next Action Date","Next Action","Contact Name","Contact Email/URL"]
    if not csv_path.exists():
        pd.DataFrame(columns=cols).to_csv(csv_path, index=False)

    df = pd.read_csv(csv_path)
    new_row = {
        "Date Found": date.today().isoformat(),
        "Company": jd.company,
        "Role": jd.role_title,
        "Location": jd.location,
        "Source Link": jd.source_link,
        "Match Score": f"{outputs.match_score}%",
        "JD Keywords": ", ".join(outputs.jd_keywords),
        "Notes": "Auto-generated; review before submission",
        "CV File": settings.cv_path.name,
        "Cover Letter File": Path(outputs.cover_letter_path).name,
        "Status": "Queued",
        "Next Action Date": "",
        "Next Action": "Review & submit",
        "Contact Name": "",
        "Contact Email/URL": ""
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(csv_path, index=False)
    return csv_path
