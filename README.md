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
* To deliver real-time news, discoveries, and research updates for each condition via web search and summarization.

## Live Links

- [Apache Airflow](http://157.245.251.74:8082)
- [FastAPI](http://157.245.251.74:8000/docs)
- [Streamlit](http://157.245.251.74:8501)
- [CodeLabs](https://codelabs-preview.appspot.com/?file_id=1vRDlDe1wL3BszPOn75w2uF0WKvaB9SjdFROvnrNpknE#0)
- [DemoLink](https://drive.google.com/drive/folders/1ZsTAWwdGBpguvkAeMRJh24xeFvWyDgYY)

# Architecture Diagram

## Airflow Pipeline

![Diagram_Nutrition_RAG_Project](https://github.com/user-attachments/assets/3b989289-f436-4dfd-86e5-d373ce67238d)


![mermaid-diagram-2025-04-18-152843](https://github.com/user-attachments/assets/aa0bb440-ca03-49fe-94df-b6ee15a14d4a)

# Tools and Technologies

* Frontend: Streamlit
* Backend: FastAPI
* Agent Framework: LangGraph
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
# On Windows: venv\Scripts\activate
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
## Data Sources

1. **[Edamam API](https://developer.edamam.com/edamam-nutrition-api)**
   - Provides nutrition data for recipes and ingredients.

2. **[CDC (Centers for Disease Control and Prevention)](https://www.cdc.gov/)**
   - Provides health data and statistics on various diseases and conditions.

## Tools & Services

### Apache Airflow
- **[Official Documentation](https://airflow.apache.org/docs/)**
  - A platform to programmatically author, schedule, and monitor workflows.
- **[Snowflake Operator for Airflow](https://airflow.apache.org/docs/apache-airflow-providers-snowflake/)**
  - Allows you to interact with Snowflake from Airflow tasks.

### Snowflake
- **[Getting Started with Snowflake](https://quickstarts.snowflake.com/guide/getting_started_with_snowflake/index.html#0)**
  - An introduction to setting up Snowflake data warehouses and working with Snowflake data.
- **[Python Connector Documentation](https://docs.snowflake.com/en/user-guide/python-connectoN)**
  - Learn how to use Python to interact with Snowflake databases.

### DBT (Data Build Tool)
- **[Official Documentation](https://docs.getdbt.com/)**
  - A powerful tool for transforming raw data into a meaningful form using SQL.

### FastAPI
- **[Official Documentation](https://fastapi.tiangolo.com/)**
  - A modern framework for building APIs with Python.
- **[SQLAlchemy Integration](https://fastapi.tiangolo.com/tutorial/sql-databases/)**
  - Learn how to connect FastAPI to relational databases using SQLAlchemy.

### AWS S3
- **[Python SDK (Boto3)](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)**
  - Amazon Web Services' SDK for Python to interact with S3 and other AWS services.

### Streamlit
- **[Official Documentation](https://docs.streamlit.io/)**
  - A tool to easily create beautiful data apps with Python.

### OpenAI API
- **[Official Documentation](https://platform.openai.com/docs)**
  - API for integrating OpenAI's GPT models into your applications.

### LangChain
- **[Official Documentation](https://docs.langchain.com)**
  - A framework for building applications that leverage large language models (LLMs).

### Google Developers
- **[Google Maps Platform Documentation](https://developers.google.com/maps/documentation)**
  - APIs to integrate mapping, location, and geospatial data into your applications.

---

## 🧾 DISCLOSURES
**Contributions**  
Vemana Anil Kumar - 33.3%  
Ashwin Badamikar - 33.3%  
Madhura Adadande - 33.3%

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

