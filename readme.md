pip cache purge

to run backend
uvicorn main:app --reload
uvicorn main:app --reload --port 8002

setup backend
(must use python 3.10.11)
python -m venv tf_env_stable
python --version
.\tf_env_stable\Scripts\activate
pip install "fastapi[all]" "motor[srv]" beanie aiostream numpy matplotlib pillow uvicorn tensorflow python-jose passlib[bcrypt] google.generativeai python-multipart cloudinary pydantic-settings

generate requirements files
pip freeze > requirements.txt

gemini setup
pip install google-generativeai

to run
.\tf_env_stable\Scripts\activate
uvicorn main:app --reload --port 8002