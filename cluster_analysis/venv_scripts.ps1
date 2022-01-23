venv\Scripts\activate
pip list
python.exe -m pip install --upgrade pip
pip install pillow>=9.0.0
pip freeze > requirements.txt
pip list
deactivate
