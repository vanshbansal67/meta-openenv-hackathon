# 📧 Meta OpenEnv: Email Triage & Automation Agent Environment

[![OpenEnv](https://img.shields.io/badge/OpenEnv-Spec_Compliant-green)](https://github.com/meta-llama/openenv)
[![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Space-blue)](https://huggingface.co/spaces/Vanshbansal67/meta-pytorch-openenv-triage)

---

### **1. 📝 Overview**
This project introduces a high-fidelity simulation environment for **AI Digital Assistants** focused on automated email management. The agent acts as an automated triage officer, responsible for analyzing incoming corporate communications, determining their business priority, and routing them to the correct internal departments.

**The Problem:** Most LLM agents excel at chat but struggle with structured decision-making in noisy environments. This environment provides a deterministic sandbox with granular reward signals to benchmark an agent's reasoning against real-world corporate scenarios.

---

### **2. 📂 Project Architecture**
The project follows the standard **Meta OpenEnv** specification for seamless integration with automated evaluation pipelines.

```text
.
├── envs/
│   ├── __init__.py
│   ├── models.py       # Pydantic models (Action/Observation)
│   └── simulator.py    # Core logic & Grader system
├── archive/            # Deprecated testing scripts
├── Dockerfile          # Containerization for HF Spaces
├── inference.py        # MANDATORY: Official baseline script
├── openenv.yaml        # Environment metadata
├── requirements.txt    # Dependency list
└── README.md           # Documentation

```
---

### **3. ⚙️ Environment Design**

The agent interacts with the email system through a well-defined interface, ensuring deterministic results and measurable outcomes.

#### **Observation Space (`EmailObservation`)**
The agent receives a structured snapshot of the incoming task:
* **`sender`**: String identifying the source (e.g., `ceo@company.com`, `no-reply@billing.com`).
* **`subject`**: Email subject line providing immediate context.
* **`body`**: Full semantic content for deep triage analysis.
* **`current_queue_size`**: Integer reflecting the workload remaining in the assistant's buffer.

#### **Action Space (`EmailAction`)**
The agent must generate a precise JSON-serializable action:
* **`priority`**: Must be categorized as `High`, `Medium`, or `Low`.
* **`category`**: Must be routed to `Support`, `Billing`, or `Spam`.
* **`action_taken`**: A log of the agent's internal reasoning or the specific handling step executed.

---

### **4. 📊 Task Progression & Graders**

We have implemented three programmatic task levels to evaluate the agent across a gradient of semantic complexity:

| Task ID | Level | Scenario Description | Evaluation Goal |
| :--- | :--- | :--- | :--- |
| **`easy`** | Beginner | Clear-cut marketing spam vs. direct personal boss emails. | High precision in Spam/Priority detection. |
| **`medium`** | Intermediate | Overdue billing notices mixed with general policy updates. | Recognition of financial/administrative urgency. |
| **`hard`** | Advanced | Critical production bug reports vs. complex feature requests. | Nuanced differentiation of technical priority. |

---

### **5. 🏆 Reward Shaping & Evaluation Logic**

To facilitate Reinforcement Learning and fine-grained benchmarking, we use a weighted reward function that rewards partial accuracy:

$$Reward = (0.3 \times \text{Category Match}) + (0.7 \times \text{Priority Match})$$

* **Grader Score:** The final `grader_score` (0.0 to 1.0) is the normalized average of the rewards accumulated over the task trajectory.
* **Success Threshold:** A task is considered successful if the cumulative score exceeds **0.70**.

---

### **6. 🛠️ Setup & Reproducibility**

#### **Local Installation**
We recommend using `uv` for high-speed dependency management:
```bash
pip install uv
uv lock
pip install -r requirements.txt

```
### **8. 👥 Project Contributors & Metadata**
* **`Lead Developer`**: Vanshaj Bansal, Mahima
* **`Institution`**: Vidya College of Engineering, Meerut (UP)
* **`Project Status`**: Production Ready / Meta Spec Compliant
* **`Tech Stack`**: Python 3.11, FastAPI, Pydantic, Docker, OpenAI SDK
* **`OpenEnv Identifier`**: openenv-email-triage-v1
