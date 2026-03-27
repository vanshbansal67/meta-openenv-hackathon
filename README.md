# 📧 Email Triage & Automation Agent Environment

### **Overview**
Ye ek real-world simulation environment hai jahan ek AI Agent ko "Digital Assistant" ki tarah kaam karna hota hai. Agent ka kaam hai incoming emails ko read karna, unki **Priority** decide karna, aur unhe sahi **Category** mein daalna. 

**Motivation:** Aaj kal LLM agents text toh samajh lete hain, par unhe structured environment chahiye jahan wo "Partial Success" aur "Deterministic Graders" ke saath train ho sakein. Ye environment wahi gap fill karta hai.

---

### **Environment Design**

#### **1. Observation Space**
Agent ko har step par ek `EmailObservation` milti hai:
* `sender`: Email bhejne wale ki identity.
* `subject`: Context aur urgency samajhne ke liye.
* `body`: Detail analysis ke liye poora content.
* `current_queue_size`: Pending tasks ki count.

#### **2. Action Space**
Agent ko `EmailAction` perform karni hoti hai:
* `priority`: High, Medium, ya Low (Crucial for sorting).
* `category`: Support, Billing, ya Spam (Crucial for routing).
* `action_taken`: Agent ki reasoning ka log.

---

### **Task Progression & Difficulty**
Humne isme 3 distinct tasks implement kiye hain jo agent ki reasoning power ko test karte hain:

| Task ID | Level | Description |
| :--- | :--- | :--- |
| `easy` | Beginner | Simple spam filter aur obvious boss emails. |
| `medium` | Intermediate | Billing failures aur policy updates jisme nuance chahiye. |
| `hard` | Advanced | Production-level bug reports jahan priority determine karna mushkil hota hai. |

---

### **Reward Shaping & Grader Logic**
Is environment mein humne **Partial Reward signals** use kiye hain taaki agent jaldi seekh sake:

$$Reward = (0.3 \times \text{Category Match}) + (0.7 \times \text{Priority Match})$$

* **Grader Score:** Har episode ke end mein ek `grader_score` (0.0 to 1.0) generate hota hai jo total accumulated rewards ka average hota hai.

---

### **Setup & Usage Instructions**

**1. Installation**
```bash
pip install uv
uv lock
pip install -r requirements.txt