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

# Resources
Code labs link: https://codelabs-preview.appspot.com/?file_id=1vRDlDe1wL3BszPOn75w2uF0WKvaB9SjdFROvnrNpknE#0

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


# Team Roles and Responsivilities

* Vemana Anil Kumar:
  * Design and develop Airflow DAGs and Configure Snowflake
  * Work on Nutrition and Drug agents
  * Build LangGraph agent controller (multi-agent logic)
  * Lead project integration and deployment flow

* Madhura Adadhande:
  * Implement FastAPI backend and all route handlers
  * Develop markdown pipeline (S3 → Mistral → Pinecone)
  * Handle OpenAI + Pinecone embeddings
  * Build Streamlit pages for Info and Summary

* Madhura Adadhande:
  * Implement Location Agent using Tavily + Google Maps
  * Handle S3 data versioning + Markdown validation
  * Add Email alerting system with user config
