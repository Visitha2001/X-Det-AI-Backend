pip cache purge

to run backend
uvicorn main:app --reload
uvicorn main:app --reload --port 8002

setup backend
(must use python 3.11 or 3.12)
python -m venv tf_env
python --version
.\tf_env\Scripts\activate
pip install "fastapi[all]" "motor[srv]" beanie aiostream numpy matplotlib pillow uvicorn tensorflow python-jose passlib[bcrypt] google.generativeai

generate requirements files
pip freeze > requirements.txt

gemini setup
pip install google-generativeai