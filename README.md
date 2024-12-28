# Physics Chatbot: Offline AI-Powered Learning Assistant

## Project Overview

The **Physics Chatbot** is an offline AI-driven educational tool designed to assist students of grades 9-10 in learning physics. It provides accurate and textbook-aligned answers, conceptual clarity, and interactive explanations based on the *Physics Classes 9-10 (English Version)* by NCTB. By leveraging **Retrieval Augmented Generation (RAG)** and lightweight AI models, this chatbot bridges the digital divide and ensures equitable access to quality education.

## Features

- **Offline Functionality**: Works without internet, reducing reliance on cloud servers.
- **Textbook Alignment**: Retrieves relevant content directly from the NCTB textbook.
- **Interactive Explanations**: Provides clear and concise explanations with inline LaTeX for mathematical equations.
- **Efficient Memory Usage**: Stores conversation summaries using Small Language Models (SLMs) to enhance context retention.
- **Sustainability**: Optimized for minimal resource consumption, ensuring energy efficiency.

## Technologies Used

- **AI Framework**: Retrieval Augmented Generation (RAG)
- **Model Execution**: [Ollama](https://ollama.ai/) for LLM/SLM
- **GPU-Accelerated Computation**: Google Colab
- **Database**: MongoDB for storing chat history
- **Frontend**: Inline LaTeX and Markdown for equations
- **Programming Languages**: Python

## System Architecture

1. **Planning Phase**:
   - Implemented a simple RAG system with chunked textbook data stored in a vector database.
   - Retrieved relevant chunks and utilized prompt engineering with LLM for response generation.

2. **Advanced RAG System**:
   - Generated related questions for enhanced retrieval.
   - Summarized responses using SLM to reduce memory overhead and improve precision.

3. **Frontend Development**:
   - Integrated inline LaTeX for mathematical clarity.
   - Designed a user-friendly interface.

## Dataset

The dataset includes factual, conceptual, explanatory, and math-based problems sourced from:
- **Physics Classes 9-10 (NCTB)**
- **Panjeree Test Paper**
- **Teachingbd24.com**

## Evaluation Metrics

- **BERT Score**
- **BLEU**
- **ROUGE**
- **Cosine Similarity**
- **Online Judge Evaluations**

## Manual Testing Feedback

Feedback from diverse testers, including students and educators, highlighted the following:

- **Strengths**:
  - Clarity of explanations (4.5/5)
  - Helpfulness in understanding concepts (4.4/5)
  - Appropriate language and tone

- **Challenges**:
  - Struggled with out-of-scope questions.
  - Lacked mathematical notation in some responses.
  - Slightly slow response time.

- **Suggestions**:
  - Improve response conciseness.
  - Add features like graph generation and enhanced mathematical notations.

## Installation and Setup

1. Clone the repository:
   ```bash
   git clone [https://github.com/your-username/physics-chatbot.git](https://github.com/tan7vir/Physics-Chatbot-using-Advanced-RAG)
   ```

2. Navigate to the project directory:
   ```bash
   cd physics-chatbot
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the backend:
   ```bash
   cd backend
   python run app.py
   ```
5. Run the Frontend:
   ```bash
   cd ..
   cd Frontend
   streamlit run app.py
   ```

## Future Improvements

- Fine-tuning AI models specifically on the NCTB Physics textbook.
- Incorporating support for multiple sessions and context continuity.
- Enhancing retrieval mechanisms for better accuracy.
- Reducing response time through optimization.
- Integrating graph generation and improved mathematical outputs.

## Contributors

- **Md Tanvirul Islam Niloy** - Lead Developer & Database 
- **Abu Saleh Al Nahian** - Database

---

We welcome contributions! If you’d like to improve this project, please submit a pull request or open an issue.
