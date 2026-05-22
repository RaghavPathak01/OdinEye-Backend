# 👁️ Odin's Eye | AxiomHeimdall Core v3.0

**Track:** Cognify: AI & Automation (InOut Hacks '26)

---

## 🛡️ The Problem

AI models (LLMs) often provide incorrect information with high confidence—a phenomenon known as **Hallucination**. In critical sectors like Healthcare, Law, and Finance, these hallucinations can lead to life-threatening or legal catastrophes.

## 🚀 Solution

**Odin's Eye** is an automated security and verification layer that bridges the gap between AI and User Trust. It intercepts every claim made by an AI and cross-references it against our **Verified Knowledge Vault**. If the AI provides false information, our system "Intercepts" the response, flags the error, and provides the "Healed" ground truth.


## 📊 How it Works (Architecture)

1. **Input:** User asks a fact-based question.
2. **Analysis:** Odin LLM generates a response based on its internal training data.
3. **Verification:** The FastAPI backend extracts the claim and uses **ChromaDB (Vector DB)** to perform a semantic search against our verified vault.
4. **Logic Trace:** - **Similarity Found:** Status is marked as **VERIFIED** (Green Badge).
   - **Conflict Detected:** Status is marked as **FALSE CLAIM** (Red Alert + Corrected Truth).
5. **Output:** The user receives a validated response with a confidence score and a cited source.

---

## 🛠️ Tech Stack

- **Language:** Python
- **Backend:** FastAPI (For high-speed asynchronous processing)
- **Vector Database:** ChromaDB (For semantic indexing & fact-checking)
- **Data Processing:** Pandas
- **Frontend:** HTML5, CSS3 (Cyber-Terminal Theme), JavaScript

---

## 🌟 Key Features

- **100+ Multi-Domain Vault:** Covers Medical (WHO), Legal (Constitution), and Finance (SEBI).
- **Neural Confidence Meter:** Visual feedback on the factual strength of the AI's claim.
- **Evidence Snippet:** Real-time extraction of document proof with a hacker-style typewriter effect.
- **Auto-Healing:** Automatically corrects AI hallucinations before they reach the user.

---

## 🏃 Installation & Setup

1. Install dependencies:  
   `pip install -r requirements.txt`
2. Hydrate the Knowledge Vault:  
   `python db_manager.py`
3. Launch the Application:  
   `uvicorn app:app --reload`
4. Access the Dashboard: `http://127.0.0.1:8000`

---

© 2026 Team Odin's Eye | Built for InOut Hacks, JSS Academy of Technical Education.
