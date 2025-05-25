# ✨ AI-Powered Dynamic Ad Generation Agent ✨

## Project Overview

This project showcases a sophisticated **AI-Powered Dynamic Ad Generation Agent** for real-time, context-aware advertising. Leveraging cutting-edge Generative AI and Agentic AI, it aims to revolutionize ad content creation from static campaigns to personalized user experiences.

Built with a Django backend and a React frontend, this application integrates Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), advanced vector databases (FAISS), and intelligent reranking using Cross-Encoders.

## 🚀 What This AI Agent Can Do for Clients

For businesses and advertising platforms, this AI agent offers significant advantages:

* **Real-time Personalization:** Generates highly relevant ad copy based on user context and inferred interests, moving beyond generic ads.

* **Enhanced Ad Performance:** Improves factual accuracy and appeal by grounding LLM generations in up-to-date external knowledge, potentially boosting CTR and conversion rates.

* **Operational Efficiency:** Automates ad copy creation, freeing marketing teams for strategy.

* **Scalable Content Generation:** Rapidly produces unique ad variations for diverse segments, products, or triggers.

* **Data-Driven Insights:** Logs ad generation requests, providing a foundation for analytics and performance linking.

* **Future-Proofing Advertising:** Positions clients at the forefront of AI-driven marketing.

### **Real Estate Industry Applications**

This agent is particularly impactful for real estate, enabling highly personalized property advertising:

* **Hyper-Personalized Listings:** Creates ads tailored to user search history, property views, or inferred lifestyle needs (e.g., "3-bedroom homes near good schools").

* **Contextual Property Highlights:** Dynamically generates ads emphasizing features relevant to user browsing context (e.g., "low down payment options" for first-time homebuyer tips).

* **Neighborhood-Specific Messaging:** Pulls local amenity data via RAG to highlight unique benefits of properties in specific areas.

* **Dynamic Open House Promotions:** Generates real-time ads for open houses based on user location and preferences, with direct scheduling links.

* **Agent-Specific Branding:** Can be fine-tuned to incorporate individual real estate agent branding.

* **Targeted Investment Opportunities:** Generates ads for properties with investment potential (e.g., "high rental yield") using market data.

By leveraging RAG with property databases and user behavior, this agent transforms real estate advertising from broad outreach to precise, high-conversion engagements.

## 🌟 Key Features

* **Dynamic Ad Copy Generation:** Creates engaging, relevant ad copy using LLMs.

* **Contextual Retrieval (RAG):** Integrates external knowledge (product/blog data) for LLM context.

* **Semantic Search with FAISS:** Uses FAISS for efficient, meaning-based content retrieval.

* **Intelligent Reranking:** Employs a Cross-Encoder (`cross-encoder/ms-marco-MiniLM-L-6-v2`) to prioritize retrieved documents.

* **Modular Architecture:** Separates Django backend (data, retrieval) and React frontend (UI, LLM orchestration).

* **Ad Generation Logging:** Records requests for analytics and auditing.

* **Scalable Data Ingestion:** Includes a Django command for offline embedding generation and FAISS index building.

## 🏗️ Technical Architecture

This project is a client-server application:

### **1. Django Backend**

* **Role:** Manages data, performs context retrieval and reranking, exposes API endpoints.

* **Components:**

    * `models.py`: Defines Django models for `UserProfile`, `AdCampaign`, `AdGenerationLog`.

    * `utils/embedding_utils.py`: Uses `SentenceTransformer('all-MiniLM-L6-v2')` for embeddings; manages FAISS index creation/loading.

    * `utils/rag_core.py`: Orchestrates FAISS queries and integrates `CrossEncoder` for reranking.

    * `management/commands/load_data.py`: Custom command to pre-process data and build persistent FAISS indexes.

    * `views.py`: Exposes `/api/get_ad_context/` (retrieves/reranks context) and `/api/generate_final_ad/` (placeholder for server-side LLM call/logging).

* **Core Libraries:** `Django`, `sentence-transformers`, `faiss-cpu`, `cross-encoder`.

### **2. React Frontend**

* **Role:** Provides UI, orchestrates interaction, directly invokes LLM.

* **Workflow:** User query $\rightarrow$ Django backend for context $\rightarrow$ React constructs prompt with context $\rightarrow$ Gemini API (`gemini-2.0-flash`) for ad generation $\rightarrow$ Display ad.

* **Key Features:** Responsive design (Tailwind CSS), loading indicators, error handling.

* **Core Libraries:** `React`, `Tailwind CSS`.

## 🛠️ Getting Started

### **Prerequisites**

* Python 3.8+

* Git

### **Setup Instructions**

1.  **Clone Repo:** `git clone [YOUR_REPO_URL_HERE]` then `cd ad_generator_project_v2`.

2.  **Virtual Environment:** `python -m venv venv`; `source venv/bin/activate` (Linux/macOS) or `venv\Scripts\activate` (Windows).

3.  **Install Dependencies:** `pip install -r requirements.txt`.

4.  **Run Migrations:** `python manage.py makemigrations ad_generator_app`; `python manage.py migrate`.

5.  **Load Data/Build Indexes:** `python manage.py load_data` (downloads models, builds FAISS).

6.  **Create Superuser (Optional):** `python manage.py createsuperuser`.

7.  **Start Server:** `python manage.py runserver`.

8.  **Access App:** Open `http://127.0.0.1:8000/` in your browser.

## 📈 Future Enhancements

* **Full Backend LLM Integration:** Centralize LLM calls (e.g., Gemini API) in Django for complex prompt orchestration via LangChain.

* **Advanced Prompt Engineering:** Implement dynamic prompts with few-shot examples and agentic reasoning.

* **Multi-Modal RAG:** Incorporate image/video embeddings.

* **A/B Testing:** Integrate tools for ad copy/strategy testing.

* **User-Specific Context:** Personalize ads using `UserProfile` data.

* **Real-time Analytics:** Build dashboards for logs and performance.

* **Deployment:** Containerize (Docker, Kubernetes) for cloud platforms.

* **Evaluation Frameworks:** Integrate automated tools (Evals) for continuous quality monitoring.

## 🤝 Collaboration & Contact

I'm passionate about Generative AI and Agentic AI, open to discussing ideas, collaborations, or opportunities.

Reach out on LinkedIn: https://www.linkedin.com/in/kapil-chaudhari-445130171/