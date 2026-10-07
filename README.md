# [Log Analyzer - notepad++]

> Python Script project aiming to bring the analysis/Debugging at 1 click using notepad++.

---

## 1. Problem at Hand

* **Core Issue:** Operational overhead of analysing and opening all log files captured from a client, 40-50 different log files to faster diagnose the root cause of the issues in production systems. Aim to give a report of all these issues in files as 1 report, for maximum token ROI when checking with AI-Chat agents.
* **Impact:** from 20-30 minutes of manual log checking reduced to under 10 seconds and unified report of this check. 
* **Target Outcome:** Faster report, Maxium verbosity on error details, Best optimized for AI-token economy.

---

## 2. Languages & Tools Used

| Category | Technology / Stack | Role / Purpose |
| :--- | :--- | :--- |
| **Language(s)** | Python script (2.1.0)/ Notepad++/ Pythonscript-plugin on Notepad++. | Unified-Tool

---

## 3. Actions & Thought Process

### Architectural Decisions
* **Why this approach?** Lightweight plugin to unify process in one tool(notepad++).
* **Constraints handled:** Limited tokens, AI-agent processing & Parsing time, Limited access over corporate network.

### Execution & Implementation
> Exporation and step by step inclusion of newer features or optimisations.

---

## Quickstart

```bash
# Clone the repository
git clone "https://github.com/rahulv-security/LogAnalyzer"
cd [LogAnalyzer]

# Run setup / execution
Start Notepad++ and open all log files for multi-file processing.
Click on Plugins
Dropdown select Python Script and hover over scripts option
click on LogAnalyzer --> Execution proceeds to output as new file (Consolidated Report)
