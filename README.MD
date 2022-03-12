Create Virtual environment in python
python3 -m venv venv
to install all libraries
pip install -r requirements.txt 

pip freeze >requirements.txt
flask db upgrade
flask db migrate -m 'initial migration'