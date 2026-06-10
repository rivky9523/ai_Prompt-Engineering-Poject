# Smart CLI Agent

**Objective:** Building an AI-powered (LLM) agent that converts natural language requests into terminal commands, with a strict emphasis on safety, risk management, and sandboxed execution.

**[Experimentation & Metrics Documentation (Google Sheets)](https://docs.google.com/spreadsheets/d/1UqsjkkB372gfAby7IvLB0XIZY-38BRw-PrNTUSfFLmw/edit?gid=0#gid=0)**

---

## Iteration Log (Optimization Process)

### Iteration 1: Minimum Viable Product (MVP)
* **Objective:** Building an initial interface to convert natural language into CLI commands.
* **Findings:** The model provided technically accurate but highly dangerous commands (such as formatting or deleting drives) without any warning. Additionally, typos were discovered (such as `tin` instead of `time`) along with an inconsistent format that included long, redundant explanations that could not be executed.

### Iteration 2: Security & Accuracy Enforcement
* **Objective:** Blocking dangerous commands and improving syntactic accuracy.
* **Prompt Modifications:** Adding strict rules that prohibit redundant explanations (Zero-shot) and block destructive commands with a `BLOCKED` message.
* **Results:** The safety metric rose to 100% and the model stopped producing typos. However, the system became overly rigid, blocking completely legitimate commands as well (such as deleting a single file).

### Iteration 3: Smart Risk Assessment
* **Objective:** Differentiating between completely forbidden commands and commands that require user confirmation.
* **Prompt Modifications:** Categorizing commands into 3 tiers: Safe (direct execution), Sensitive (requires confirmation - `REQUIRES_CONFIRMATION`), and Forbidden (absolute block).
* **Results:** The system demonstrates a perfect balance between high security and operational flexibility.

### Iteration 4 (Bonus): Out-of-Scope Handling & Sandboxed Execution
* **Objective:** Preventing hallucinations in case of conversational input, and executing the actual commands in a secure environment.
* **Prompt & Code Modifications:** 1. Adding an `OUT OF SCOPE` rule – if the user types "How's it going?", the model returns an error message instead of inventing a command.
  2. Transitioning from a Windows prompt to a **Linux Bash** prompt, to enable native and fast execution inside a Docker container (Ubuntu).
* **Results:** The system is immune to requests unrelated to the terminal. Safe commands are automatically sent to an isolated container (Docker Sandbox), executed there, and the output is returned to the user in real-time via a bidirectional Gradio interface.

---

## ⚠️ Key Insights & Interesting Failures

1. **The Encoding Challenge:** Discovered that commands including Hebrew characters are only "partially valid," since classic terminals struggle with Hebrew encoding, which can lead to faulty output.
2. **Permissions:** Certain system commands require administrative privileges (Admin/Sudo). In this project, we created a restricted user (named `runner`) in the Dockerfile to ensure that even if a dangerous command managed to bypass the LLM, it would fail natively at the operating system level.

---

## 🚀 Local Installation & Execution

1. Install the required packages:
```bash
pip install -r requirements.txt
# Or using uv:
uv sync
