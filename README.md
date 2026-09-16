# 🏥 MediTrace

## AI-Powered Emergency Health Passport with Verifiable Medical History

MediTrace is a secure digital health-passport platform designed to help doctors **quickly access, understand, retrieve, and verify relevant patient medical history**, especially during emergency situations.

Medical information is often spread across prescriptions, reports, hospital records, and scanned documents. MediTrace brings these sources together and uses **OCR, Medical NLU, RAG, and LLM-assisted analysis** to make historical information easier to retrieve and understand.

For critical medical events, MediTrace also provides **blockchain-backed integrity verification**, allowing the system to detect if an important historical record has been modified or is missing.

> **MediTrace assists the doctor; it does not replace the doctor.**

---

# 🎯 Problem

In emergency situations, doctors may need important historical information within seconds.

However:

- Medical records may be scattered across different documents and hospitals.
- Old prescriptions and reports can be difficult to search manually.
- Critical information such as allergies, previous surgeries, chronic conditions, and major medical events may be buried inside documents.
- There may be a need to verify whether important historical information has been modified.
- Emergency access must remain controlled and traceable.

MediTrace addresses these problems by combining **secure medical data management, AI-assisted retrieval, and integrity verification**.

---

# 💡 Our Solution

MediTrace provides a digital emergency health passport where authorized doctors can access relevant patient information through a secure interface.

The system combines:

- 🔐 Authentication and role-based access
- 👤 Patient and doctor management
- 📄 Medical document processing
- 🔎 OCR-based text extraction
- 🧠 Medical Natural Language Understanding
- 🗂️ Structured medical information
- 🔍 Patient-scoped RAG retrieval
- 🤖 Gemini LLM-assisted responses
- 🔗 SHA-256 + blockchain-backed integrity verification
- 🚨 Controlled Break-Glass emergency access
- 📋 Complete audit logging

---

# 🔄 Complete Working Flow

```text
                         ┌─────────────────────┐
                         │   Patient / Doctor  │
                         │      Login          │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ Authentication &    │
                         │ Authorization       │
                         └──────────┬──────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
                    ▼                               ▼
           ┌────────────────┐              ┌────────────────┐
           │  Normal Access │              │  Break-Glass   │
           │                │              │   Emergency    │
           └───────┬────────┘              └───────┬────────┘
                   │                               │
                   └───────────────┬───────────────┘
                                   ▼
                         ┌─────────────────────┐
                         │ Patient Medical     │
                         │ Records/Documents   │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ OCR / Text          │
                         │ Extraction          │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ Medical NLU         │
                         │                     │
                         │ Conditions          │
                         │ Allergies           │
                         │ Medications         │
                         │ Procedures / Events │
                         └──────────┬──────────┘
                                    │
                       ┌────────────┴────────────┐
                       ▼                         ▼
              ┌────────────────┐        ┌────────────────┐
              │ Structured     │        │ Historical     │
              │ Medical Data   │        │ Documents      │
              └───────┬────────┘        └───────┬────────┘
                      │                          │
                      ▼                          ▼
              ┌────────────────┐        ┌────────────────┐
              │ Supabase /     │        │ Chunking +     │
              │ PostgreSQL     │        │ Embeddings     │
              └────────────────┘        └───────┬────────┘
                                                 │
                                                 ▼
                                        ┌────────────────┐
                                        │ Patient-Scoped │
                                        │ RAG Retrieval  │
                                        └───────┬────────┘
                                                │
                                                ▼
                                        ┌────────────────┐
                                        │ Gemini LLM     │
                                        │ Grounded       │
                                        │ Response       │
                                        └───────┬────────┘
                                                │
                                                ▼
                                        ┌────────────────┐
                                        │ Doctor Review  │
                                        │ & Decision     │
                                        └────────────────┘
