# House Price Prediction System

An end-to-end Machine Learning web application designed to predict residential property prices. The system is built using a modern decoupled architecture:

* **Backend Framework:** FastAPI (RESTful API, Data Validation via Pydantic).
* **Frontend Framework:** Streamlit (Interactive Data Web Interface).
* **Machine Learning Model:** Trained pipeline integrated using `joblib` / `scikit-learn`.

---

## 📸 Project Live Preview

### Web Application Interface
![Streamlit App Interface](./app1.png.jpeg)
---

## 🚀 How to Run Locally

### Prerequisites
Make sure you have Python installed and your virtual environment activated.

### 1. Start Backend Server (FastAPI)
```bash
cd backend
uvicorn main:app --reload
cd frontend
streamlit run app.py
