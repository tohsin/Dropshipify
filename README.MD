Create Virtual environment in python
python3 -m venv venv
to install all libraries
pip install -r requirements.txt 

pip freeze >requirements.txt

Windows
$ py -3 -m venv venv

Activate virtual environment:
venv\Scripts\activate

tell flask whicj app to use
export FLASK_APP=main.py

then create dummy data with command
flask test


### TO DO
* Add function to add to wishlist
- [ ] Add toast to signify adding to wish list
- [x] Add function to add to wishlist
- [ ] Come up with proper data structure for order -items
- [ ] 
