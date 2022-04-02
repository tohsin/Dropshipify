from re import T
from webapp import create_app
from webapp import db
from webapp.models import User, Store,Product
from werkzeug.utils import secure_filename
import uuid as uuid
from werkzeug.security import generate_password_hash, check_password_hash
from webapp.dummy_data import create_dummydata
app = create_app()

@app.cli.command()
def test():
    create_dummydata()
       
if __name__ == '__main__':
    app.run(debug=True)
