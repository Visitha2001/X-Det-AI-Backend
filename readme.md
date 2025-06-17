
---

### 🧹 Clear pip cache

```bash
pip cache purge
```

---

### 🚀 Run Backend Server

```bash
uvicorn main:app --reload
# or
uvicorn main:app --reload --port 8002
```

---

### ⚙️ Backend Setup

**(Make sure to use Python 3.10.11)**

```bash
python -m venv tf_env_stable
python --version
.\tf_env_stable\Scripts\activate

pip install "fastapi[all]" "motor[srv]" beanie aiostream numpy matplotlib pillow uvicorn tensorflow python-jose passlib[bcrypt] google.generativeai python-multipart cloudinary pydantic-settings sentence-transformers scikit-learn numpy
```

---

### 📦 Generate Requirements File

```bash
pip freeze > requirements.txt
```

---

### 🧠 Gemini Setup

```bash
pip install google-generativeai
```

---

### ▶️ Run the Project

```bash
.\tf_env_stable\Scripts\activate
python --version
cd src
uvicorn main:app --reload --port 8002
```

---
