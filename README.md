# Big_Data_Final_Project

# Introduction
Chronic health conditions such as Type 2 Diabetes, Hypertension, High Cholesterol, and Heart Disease etc are on the rise globally, significantly impacting quality of life and healthcare systems. Managing these conditions requires consistent monitoring of diet, medication, and access to real-time medical updates.

ChronicCare.AI is an AI-powered, patient-centric health management system that empowers individuals with chronic conditions to take control of their health. By integrating structured nutrition and medication data, unstructured health literature (PDFs, articles), location-based services, and AI-driven insights from large language models, the platform offers a unified experience for dietary guidance, medication adherence, and real-time medication updates.

# Objective:
The goal of ChronicCare.AI is to design an intelligent assistant that supports end-to-end chronic disease management, leveraging structured data, unstructured documents, and AI agents.
Key Objectives:
* To build a nutritionist module that provides daily caloric needs and food recommendations based on chronic conditions, with alerting systems for threshold violations through email.
* To develop a knowledge base powered by vector search Pinecone for patient-facing FAQs from research papers, PDFs, and government health guidelines.
* To integrate with location-aware web agents for discovering hospitals, clinics, and support groups nearby.
* To manage medication adherence and provide drug-specific guidance using OpenFDA and RxNorm.
* To support mental health journaling and insights.
* To deliver real-time news, discoveries, and research updates for each condition via web search and summarization.

Live Links:
airflow: http://206.81.3.50:8082
fastapi: http://206.81.3.50:8000/docs
streamlit: http://206.81.3.50:8501

# Resources
Code labs link: [CodeLabs]https://codelabs-preview.appspot.com/?file_id=1vRDlDe1wL3BszPOn75w2uF0WKvaB9SjdFROvnrNpknE#0

# Architecture Diagram

<img width="1307" alt="image" src="https://github.com/user-attachments/assets/74f4be24-4253-404f-b3f9-7c3f6e678a9d" />

# Tools and Technologies

* Frontend: Streamlit
* Backend: FastAPI
* Agent Framework: LangGraph
* MCP Server: Model Context Protocol for multi-agent context sharing
* Orchestration: Apache Airflow
* Vector Database: Pinecone
* Storage: Snowflake, AWS S3
* PDF Parser: Mistral AI
* LLM Integration: OpenAI GPT-4
* Chunking Strategy: Recursive
* Embeddings: OpenAI text-embedding-3-small
* Web Search: Tavily API/ Serp API
* Containerization: Docker
* Deployment: Digital Ocean/ GCP

![ChatGPT Image Apr 18, 2025, 10_03_02 AM](https://github.com/user-attachments/assets/392b5ec5-c557-4599-acc9-cff15f7e5f3f)



# Team Roles and Responsibilities

* Vemana Anil Kumar:
  * Design and develop Airflow DAGs and Configure Snowflake
  * Work on Nutrition and Drug agents
  * Build LangGraph agent controller (multi-agent logic)
  * Lead project integration and deployment flow

* AshwinB adamikar:
  * Implement FastAPI backend and all route handlers
  * Develop markdown pipeline (S3 → Mistral → Pinecone)
  * Handle OpenAI + Pinecone embeddings
  * Build Streamlit pages for Info and Summary

* Madhura Adadhande:
  * Implement Location Agent using Tavily + Google Maps
  * Handle S3 data versioning + Markdown validation
  * Add Email alerting system with user config
 
## 🔍 PROJECT OVERVIEW

### Scope
- Development of a data ingestion system to collect structured data (e.g., user inputs, food logs) and unstructured data (e.g., health articles, PDFs, web pages)
- Creation of an ETL pipeline using Apache Airflow to process nutrition data, medical knowledge bases, and live web content
- Implementation of four AI-powered agents:
  - **Nutrition Agent** – provides dietary advice based on user inputs and chronic condition guidelines
  - **Knowledge-Based Agent** – answers questions using curated healthcare documents and research
  - **Location Web Agent** – finds nearby facilities like clinics, pharmacies, and support groups using Google Maps API
  - **Live Summary Agent** – summarizes real-time web content for chronic health updates and trends
- Integration with OpenAI and LangGraph for agent orchestration and intelligent LLM responses
- Design and development of a Streamlit-based user interface for query input, visualization, and agent interaction
- Deployment of a FastAPI backend to coordinate agent tasks, manage state, and support scalable API access

### Stakeholders
- **End Users**: Individuals managing chronic conditions seeking personalized dietary, lifestyle, and location-based healthcare support  
- **Healthcare Providers**: Indirect beneficiaries who can integrate AI-driven insights into patient care plans  
- **Health Data Platforms**: Sources of medical research, condition guidelines, and nutrition databases powering the knowledge-based agent  
- **Local Health Services**: Clinics, pharmacies, and support groups that are surfaced through the Location Web Agent

---

## 🚧 PROBLEM STATEMENT
Managing chronic illnesses is a complex and often overwhelming task. Patients must juggle multiple variables such as diet restrictions, medication schedules, etc.

Despite the abundance of medical knowledge and digital health tools, there is no centralized system that:
- Provides personalized nutrition, medication, and lifestyle guidance based on the user's condition
- Integrates real-time health insights with condition-specific recommendations
- Supports proactive alerts, and community/hospital discovery

The lack of personalization, integration, and proactive support leads to non-adherence, misinformation, and worsening health outcomes.

---

## 🎯 OBJECTIVE
The goal of ChronicCare.AI is to design an intelligent assistant that supports end-to-end chronic disease management, leveraging structured data, unstructured documents, and AI agents.

### Key Objectives
- Build a nutritionist module that provides daily caloric needs and food recommendations based on chronic conditions, with alerting systems for threshold violations through email
- Develop a knowledge base powered by vector search Pinecone for patient-facing FAQs from research papers, PDFs, and government health guidelines
- Integrate with location services for discovering hospitals, clinics, and support groups nearby
- Deliver real-time news, discoveries, and research updates for each condition via web search and summarization

---

## 🧱 SYSTEM ARCHITECTURE
ChronicCare.AI is an AI-powered assistant that integrates structured and unstructured data sources, LLM-powered agents, and a modular orchestration architecture using Airflow and LangGraph.

### Frontend (Streamlit UI)
- User Input: Chronic condition + location
- Tabs:
  - Nutrition Tracker: Recommends and monitors daily intake
  - Condition KB: QA on uploaded PDFs about the condition
  - Nearby Clinics & Support: Based on user location
  - Health Summary: Personalized recommendations and alerts
- Output:
  - Daily nutrient recommendations with intake tracking
  - Top 5 nearby clinics, pharmacies, and support groups
  - Summary with alert flags (limit crossed)
  - Email-based reminders and risk alerts

### Backend (FastAPI)
- Receives query, chronic condition, and location from UI
- Routes via LangGraph controller to appropriate agent:
  - Nutrition Agent
  - Knowledge Base QA Agent
  - Location Web Agent
  - Summary & Alert Agent

### Agents (LangGraph)
- **Nutrition Agent**: Uses Snowflake data ingested from Edamam API to suggest caloric & nutrient intake
- **Knowledge Base QA Agent**: Answers questions using PDFs via Mistral, OpenAI, Pinecone (RAG pipeline)
- **Location Web Agent**: Uses Google Maps API and OpenAI API to fetch nearby healthcare services
- **Summary Agent**: Aggregates user data and sends health summaries and alerts

### Pipeline Orchestration: Apache Airflow
- **Structured Data**:
  - Ingested from Edamam API
  - Stored in Snowflake
- **Unstructured Data**:
  - PDFs uploaded to S3 → Converted via MistralAI → Embedded and stored in Pinecone
- **Live Data**:
  - Tavily API for real-time web search (news, clinic data)

### Datasets Used
- Structured: EDAMAM (via ETL, Snowflake)
- Unstructured: PDFs
- Live: Tavily API (for web results)

---

## 🧪 PROOF OF CONCEPT
1. Using Edamam API for recipe and nutrient data  
2. Recipe pipeline integration and validation  
3. PostgreSQL DB for initial prototyping  
4. Google Maps API tested for real-time clinic search  

---

## 🗺️ ARCHITECTURE DIAGRAM
*(Insert architecture diagram image or link here)*

---

## 👣 APPLICATION WALKTHROUGH
- **Home Page**: Login and registration for new users
- **Nutrition**: Input meals and view nutrient insights with recommendations
- **Condition KB**: Ask questions related to chronic conditions based on uploaded documents
- **Nearby Clinics**: Auto-fetch nearby support centers based on location
- **Summary Tab**: Get personalized recommendations and health alerts

---

## ⚙️ INSTALLATION

### 1. Clone the Repository
```bash
git clone https://github.com/Vemana-Northeastern/Big_Data_Final_Project.git
cd ChronicCareAI
```

### 2. Create and Activate a Virtual Environment
```bash
python -m venv venv
# On Windows: venv\Scriptsctivate
# On MAC: source venv/bin/activate  
```

### 3. Install Required Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a `.env` file in the `Streamlit/` directory with the following:
```env
OPENAI_API_KEY=your_openai_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENVIRONMENT=us-east-1
```

### 5. Run the Application
```bash
cd Streamlit
streamlit run main.py
```

---

## ⚠️ RISKS AND MITIGATION STRATEGIES
- **API Rate Limits**
  - *Risk*: Hitting usage limits
  - *Mitigation*: Cache frequent queries, rotate keys, monitor usage

- **Agent Orchestration Failures**
  - *Risk*: Communication issues between agents
  - *Mitigation*: Isolated agent testing, retries, modular design

- **Unstructured Data Inaccuracy**
  - *Risk*: Incomplete or outdated info from PDFs or web
  - *Mitigation*: Use verified sources and summarization confidence filters

- **Location Mismatches**
  - *Risk*: Inaccurate map data for remote areas
  - *Mitigation*: Allow pin code input, filter results by relevance

---

## 📈 EXPECTED OUTCOMES AND BENEFITS

### Measurable Goals
- Achieve ≥ 90% accuracy in recommendation relevance
- Return at least 5 accurate facility suggestions per query
- Process 50+ chronic condition documents and 10+ real-time health updates

### Benefits
- **Personalized Support**: Tailored nutrition and health insights
- **Smarter Search**: Summarized results from trusted health sources
- **Better Access to Care**: Discover nearby support instantly
- **Scalable**: Easily extensible to other conditions and agents

---

## 📚 REFERENCES
*(See full list of tool documentation and healthcare sources in your original reference section — included as-is in this README)*

---

## 🧾 DISCLOSURES
**Contributions**  
Vemana Anil Kumar - 33%  
Ashwin Badamikar - 33%  
Madhura Adadande - 33%

**AI Usage Disclosure**  
We used AI tools (ChatGPT, DeepSeek, Claude) to assist with coding, debugging, documentation, and technical explanation. All final implementations and decisions were made by the project team.

---

## ✅ CONCLUSION
ChronicCare.AI brings a fresh perspective to how individuals manage long-term health conditions. It combines the power of AI, real-time data, and user-centric design to create a platform that is not only intelligent but genuinely helpful. 

- **Personalized Health Support**: Users receive recommendations based on their condition and lifestyle via AI-powered agents.
- **Location Awareness**: Quickly discover relevant healthcare facilities nearby.
- **Real-Time Insights**: Stay informed with live updates from trusted sources.
- **Seamless Experience**: A clean, responsive frontend with modular backend APIs.
- **Scalable Framework**: Easily extendable to cover more health domains.
- **Real-World Impact**: Designed for meaningful change in patient independence and chronic care support.

With continued development and integrations, ChronicCare.AI has the potential to become a reliable daily companion for individuals managing chronic health conditions.

