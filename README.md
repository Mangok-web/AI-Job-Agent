


## 5) Publish to GitHub (permanent access)

1. Create a **new repository** on GitHub (no README, no license).
2. In Terminal, inside this folder, run:
```bash
git init
git add .
git commit -m "Initial commit: AutoApply Pro Extended Starter"
git branch -M main
git remote add origin https://github.com/<YOUR-USERNAME>/<YOUR-REPO>.git
git push -u origin main
```
3. If prompted, use a **GitHub Personal Access Token** (classic, repo scope) as your password.

## 6) Optional: one-command setup
- **macOS / Linux**
```bash
bash setup.sh
```
- **Windows (PowerShell)**
```powershell
./setup.bat
```

