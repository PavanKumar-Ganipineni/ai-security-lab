# Exercise 01 — Environment Setup & Repository Initialisation

**Module:** M01 — LLM Threat Modelling  
**Day:** 1  
**Estimated time:** 3 hours  
**Difficulty:** Beginner  

---

## Objective

Set up the complete local lab environment on your Mac Mini M1, initialise the GitHub repository, and verify all core tools are working before any security exercises begin. A clean, verified environment on Day 1 prevents wasted time debugging tooling issues during later exercises.

---

## Prerequisites

- Mac Mini M1 with macOS Sonoma or later
- GitHub account with SSH key configured
- VS Code installed
- Homebrew installed (`/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`)

---

## Part 1 — GitHub Repository Setup (30 min)

### Step 1.1 — Create the repository on GitHub

1. Go to [github.com/new](https://github.com/new)
2. Repository name: `ai-security-lab`
3. Description: `Hands-on AI Security research lab — LLM threat modelling, adversarial ML, secure AI pipelines, SOC integration, agentic security, and AI governance. CAISP certified practitioner.`
4. Visibility: **Public** (this is your portfolio — it must be visible)
5. Do NOT initialise with README (you already have one)
6. Click **Create repository**

### Step 1.2 — Clone and push the scaffold

```bash
# Navigate to your preferred working directory
cd ~/Documents

# Clone the empty repo
git clone git@github.com:YOUR_GITHUB_USERNAME/ai-security-lab.git
cd ai-security-lab

# Copy all scaffold files you downloaded from this lab into here
# (or initialise from scratch using the commands below)

# Stage everything
git add .
git commit -m "feat: initial lab scaffold — all 7 modules, templates, and docs"
git push origin main
```

### Step 1.3 — Verify on GitHub

Open `https://github.com/YOUR_GITHUB_USERNAME/ai-security-lab` in your browser.  
You should see the master README rendered with the module table.

**Evidence to capture:** Screenshot of the GitHub repository landing page.  
Save as: `module-01-llm-threat-modelling/evidence/ex-01-github-repo.png`

---

## Part 2 — Python Environment (45 min)

### Step 2.1 — Check Python version

```bash
python3 --version
# Expected: Python 3.11.x or 3.12.x
```

If below 3.11:
```bash
brew install python@3.11
echo 'export PATH="/opt/homebrew/opt/python@3.11/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### Step 2.2 — Create a virtual environment for Module 1

```bash
cd ~/Documents/ai-security-lab/module-01-llm-threat-modelling
python3 -m venv .venv
source .venv/bin/activate

# Verify
which python
# Should show: .../module-01-llm-threat-modelling/.venv/bin/python
```

### Step 2.3 — Install Module 1 dependencies

```bash
pip install --upgrade pip
pip install flask requests python-dotenv openai langchain langchain-community
pip install garak  # LLM vulnerability scanner — core tool for M1 and M2

# Verify Garak installed correctly
garak --version
```

### Step 2.4 — Create requirements.txt

```bash
pip freeze > requirements.txt
git add requirements.txt
git commit -m "feat(m01): add Python dependencies for Module 1"
git push
```

---

## Part 3 — Ollama Setup (45 min)

Ollama runs local LLMs on Apple Silicon using MPS acceleration. This is your local LLM inference engine for all modules.

### Step 3.1 — Install Ollama

```bash
# Download from ollama.ai or via Homebrew
brew install ollama

# Start the Ollama service
ollama serve &

# Verify it is running
curl http://localhost:11434/api/tags
```

### Step 3.2 — Pull the models you will use throughout the lab

```bash
# Primary model — general purpose, fast on M1
ollama pull llama3

# Smaller model — useful for rapid iteration
ollama pull phi3

# Verify both are available
ollama list
```

Expected output:
```
NAME            ID              SIZE    MODIFIED
llama3:latest   365c0bd3c000    4.7 GB  X seconds ago
phi3:latest     4f2222927938    2.3 GB  X seconds ago
```

### Step 3.3 — Test inference

```bash
# Quick sanity check
ollama run llama3 "What are the OWASP Top 10 risks for LLMs? Give a one-line answer."
```

**Evidence to capture:** Terminal screenshot showing `ollama list` output and a successful inference response.  
Save as: `evidence/ex-01-ollama-running.png`

---

## Part 4 — Docker Desktop Setup (30 min)

Docker is needed for Wazuh (M4), DefectDojo (M3), and isolated attack environments.

### Step 4.1 — Verify Docker is running

```bash
docker --version
docker ps
```

If not installed, download Docker Desktop for Apple Silicon from [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop/).

### Step 4.2 — Test a container

```bash
# Pull and run a quick test container
docker run hello-world
```

**Evidence to capture:** Screenshot of `docker run hello-world` success output.  
Save as: `evidence/ex-01-docker-running.png`

---

## Part 5 — VS Code Extensions (15 min)

Install these extensions — they will be used throughout the lab:

```
# Open VS Code and install via Extensions panel (Cmd+Shift+X):

Python                    (Microsoft)
Pylance                   (Microsoft)
GitLens                   (GitKraken)
Docker                    (Microsoft)
Markdown All in One       (Yu Zhang)
YAML                      (Red Hat)
REST Client               (Huachao Mao)  ← for testing LLM APIs
Bandit                    (optional, for inline SAST feedback)
```

---

## Part 6 — Create Your Lab Journal (15 min)

Your lab journal is a running personal log — different from the formal lab reports. It captures raw thoughts, mistakes, surprises, and questions as you work.

```bash
cat > ~/Documents/ai-security-lab/docs/LAB-JOURNAL.md << 'EOF'
# Lab Journal — AI Security Lab

> Personal running log. Raw observations, mistakes, surprises, and questions.
> Not for publication — for learning.

---

## Day 1 — [DATE]

### What I set up today
-

### What worked first time
-

### What didn't work and how I fixed it
-

### Things I want to understand better
-

### Questions for further research
-

---
EOF
```

```bash
git add docs/LAB-JOURNAL.md
git commit -m "docs: add personal lab journal"
git push
```

---

## Verification Checklist

Before moving to Exercise 02, confirm all of the following:

- [ ] GitHub repo live at `github.com/YOUR_GITHUB_USERNAME/ai-security-lab`
- [ ] Master README visible and rendering correctly
- [ ] Python 3.11+ confirmed: `python3 --version`
- [ ] Virtual environment activates: `source .venv/bin/activate`
- [ ] Garak installed: `garak --version`
- [ ] Ollama running: `ollama list` shows llama3 and phi3
- [ ] Docker running: `docker ps` returns without error
- [ ] VS Code extensions installed
- [ ] Lab journal created and committed
- [ ] All evidence screenshots saved to `evidence/` folder
- [ ] All changes committed and pushed to GitHub

---

## Troubleshooting

**Ollama not starting:**
```bash
# Kill any existing process and restart
pkill ollama
ollama serve &
sleep 2
curl http://localhost:11434/api/tags
```

**Garak install fails:**
```bash
# Try with explicit pip version
pip install --upgrade pip setuptools wheel
pip install garak
```

**Docker out of memory on M1 with 8GB:**  
Open Docker Desktop → Settings → Resources → set Memory to 4GB maximum. The M1 shares unified memory between CPU and GPU — be conservative.

---

## Time Log

| Part | Estimated | Actual | Notes |
|---|---|---|---|
| Part 1 — GitHub setup | 30 min | | |
| Part 2 — Python env | 45 min | | |
| Part 3 — Ollama | 45 min | | |
| Part 4 — Docker | 30 min | | |
| Part 5 — VS Code | 15 min | | |
| Part 6 — Lab journal | 15 min | | |
| **Total** | **3 hrs** | | |

---

## Next Exercise

→ [Exercise 02 — OWASP LLM Top 10 Deep Dive](./EX-02-owasp-llm-top10.md)

---

*Exercise 01 · Module 01 · ai-security-lab*
