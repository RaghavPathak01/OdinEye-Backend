# 🛠️ Odin's Eye | Technical Specifications & System Design

**Project Architect:** Virat Sirohi  
**Track:** Cognify: AI & Automation

---

## 🏗️ 1. System Architecture

Odin's Eye follows a **Modular RAG (Retrieval-Augmented Generation)** architecture. Unlike standard chatbots, we use a "Middle-Man" interception pattern.

### **Components:**

1. **The Ingestion Layer (`db_manager.py`):** - Uses **Pandas** to sanitize raw CSV data.
   - Vectors are generated and stored in **ChromaDB** using persistent storage.
2. **The Interception Engine (`verify_engine.py`):**
   - Extracts semantic claims from LLM outputs.
   - Performs a **K-Nearest Neighbors (KNN)** search in the vector space to find ground truth.
3. **The API Layer (`app.py`):**
   - Built on **FastAPI** for asynchronous, non-blocking I/O operations, ensuring sub-20ms latency.

---

## 🔒 2. Security Protocols (Heimdall Logic)

To ensure AI safety, we implemented three specific security guardrails:

- **Threshold-Based Validation:** We set a similarity threshold (0.75). Any AI claim falling below this is flagged as a high-risk hallucination.
- **Metadata Grounding:** Every fact is tethered to a `Source` and `Domain` tag. If the AI cannot provide a source that matches our vault, it is marked as `UNVERIFIED`.
- **The "Kill-Switch" Mechanism:** For high-stakes domains (like Medical), the system is hard-coded to prioritize the Vault over the LLM's generative output.

---

## 📊 3. Data Insights (The Vault)

Curated by our Data Architect (Raghav), the vault consists of:

- **Total Records:** 100+ High-Fidelity Facts.
- **Domains Covered:** Medical, Legal, Financial, Technology, and General Science.
- **Storage:** Persistent Vector Collections (`knowledge_vault`).

---

## ⚡ 4. API Endpoints

### **POST `/verify`**

**Request Body:**

```json
{
  "text": "The maximum dose of paracetamol is 6000mg."
}
```
