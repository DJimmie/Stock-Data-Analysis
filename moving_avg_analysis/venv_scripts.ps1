venv\Scripts\activate
pip list
python.exe -m pip install --upgrade pip
pip install ipython>=7.31.1
pip install pillow>=9.0.0
pip install lxml>=4.6.5
pip freeze > requirements.txt
pip list
deactivate
