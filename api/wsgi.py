from flask_cors import CORS
from api.classrank_rest import *

if __name__ == "__main__":
    CORS(app)
    app.run()