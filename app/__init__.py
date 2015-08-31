from flask import Flask
from flask.ext.restful import Api


app = Flask(__name__)
api = Api(app)
app.config.from_object('config')

from app import main
from app import api


# app.config['LDAP_HOST'] = '172.21.21.50'
# app.config['LDAP_BASE_DN'] = 'OU=Boise, OU=CP Users, DC=CP, DC=local'
# app.config['LDAP_USERNAME'] = 'CN=Dominic Desimini,OU=IT,OU=Boise,OU=CP Users,DC=CP,DC=local'
# app.config['LDAP_PASSWORD'] = 'Rainbow3'