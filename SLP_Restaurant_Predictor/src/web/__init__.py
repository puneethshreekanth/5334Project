from flask import Flask

web = Flask(__name__)

#Adding an import end of the file avoids circular import
from web import views