from flask import Flask, jsonify, request, g, url_for
from flask.ext.restful import Api, Resource, reqparse
from app import app
from flask.ext.httpauth import HTTPBasicAuth
from .auth import User, verify_password, db, auth
import json

app = Flask(__name__)
api = Api(app)
# change domain variable as needed for different domains. Current functionality only works for single domains, unless you removed the domain variable and have the users input the domain.
domain = "example.com"

#DNS record API  address url/api/v1.0/dns
class DNSAPI(Resource):
	#init pulls json arguments from users queries.
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('hostname', type = str, help = 'No hostnames were specified.', location = 'json')
		self.reqparse.add_argument('ipaddress', type = str, help = 'No IP Addresses were specified', location = 'json')
		super(DNSAPI, self).__init__()
	
	# Get request will return list of all records currently in /etc/os_hosts.txt. Requires authenticated credentials to use.
	@auth.login_required
	def get(self):
		lists = {}
		with open('/etc/hosts.txt', 'r+b') as f:
			for line in f:
				k, v = line.split('  ')
				lists[v.strip()] = k.strip()
			return jsonify({'records':lists})
	
	# Post request using hostname and ipaddres json inputs. Writes to /etc/os_hosts.txt in ipaddress hostname format.
	@auth.login_required
	def post(self):
		
		# Opens /etc/os_hosts.txt and inputs entries into dictionary with hostname as key and IP address as value.
		with open('/etc/hosts.txt', 'r+b') as f:
			records = {}
			args = self.reqparse.parse_args()
			host = args['hostname']
			ip = args['ipaddress']
			for line in f:
				k, v = line.strip().split("  ")
				records[v.strip()] = k.strip()
           	
           	# Returns if host is already used in list.
        	if host in records.keys():
        		return jsonify (status_code = '200', success = False, msg = "The hostname %s is already registered to the ip address %s." % (host, records[host]))
        	
        	# writes to /etc/os_hosts.txt if the hostname is not found in file.
        	else:
        		with open('/etc/hosts.txt', 'r+b') as f:
        			records[host] = ip   
        			f.writelines('{}  {}\n'.format(v, k) for k, v in records.items())
        			f.truncate()
                	#restart_service('dnsmasq')
        			return jsonify(status_code = "200", success = True, msg = "The hostname %s has been registered to the ip address %s." %(host, ip), data = args) 				
	
	# Plans to create put to allow changing of hostname or IP address without having to delete record and then entering info again. 
	def put(self):
		pass

	# Delete allows removal of record either via hostname or ipaddress. Does not require both to remove a record
	@auth.login_required
	def delete(self):
		args = self.reqparse.parse_args()
		if args['hostname'] is None:
			host = 'example.com'
		else:
			host = args['hostname'] + domain

		ip = args['ipaddress']
		records = {}
		ipaskey = {}
		#Places records into records dict with hostname as key IP address as value for parsing hostname delete requests.
		with open('/etc/os_hosts.txt', 'r+b') as f:
			for line in f:
				k, v = line.split("  ")
				records[v.strip()] = k.strip()
		#Places records into ipaskey dict with IP address as key, hostname as value, for parsing IP address delete requests.
		with open('./test.txt', 'r+b') as f:
			for line in f:
				k, v = line.split("  ")
				ipaskey[k.strip()] = v.strip()

		#if hostname is not blank it will delete using hostname record in records dict. And will error if hostname is not found in records dict.
		if host != domain:
			try:
				del records[host]
				with open('/etc/hosts.txt', 'r+b') as f:
					f.writelines('{}  {}\n'.format(v, k) for k, v in records.items())
					f.truncate()
					return jsonify(msg = "The record for %s has been removed." % host, status_code = '200', success = True)
			except KeyError:
				return jsonify(msg = "The record for %s was not found." % host, status_code = '200', success = True)
		#if hostname is blank it will query the ipaskey dict and delete record using IP address. Will error if IP address is not found in ipaskey dict.
		else:
			try:
				hostname = ipaskey[ip]
				del ipaskey[ip]
				with open('/etc/hosts.txt', 'r+b') as f:
					f.writelines('{}  {}\n'.format(k, v) for k, v in ipaskey.items())
					f.truncate() 
					return jsonify(msg = "The record for %s registered to %s has  been removed." % (ip, hostname), success = True, status_code = '200')
			except KeyError:
				return jsonify(msg = "The record for %s was not found." % ip, success = False, status_code = '200')
# api.add_resource(DNSAPI, '/api/v1.0/dns', endpoint = 'dns')

# User API for creation of new users. Comment out @auth.login_required to remove reqirement of having existing creds to create users. 
class UserAPI(Resource):

	#@auth.login_required
	def post(self):
		username = request.json.get('username')
		password = request.json.get('password')
		if username is None or password is None:
			return jsonify(msg = "Please enter a valid username or password.", success = False, status_code = '200')    # missing arguments
		if User.query.filter_by(username=username).first() is not None:
			return jsonify(msg = "User already exists", success = False, status_code = '200')    # existing user
		user = User(username=username)
		user.hash_password(password)
		db.session.add(user)
		db.session.commit()
		return jsonify(success = True, status_code = 201, msg = "User %s created" % username)


# Token api call to issue token for authentication verses UN and PW. Timeout is 1 day currently.
class Token(Resource):
	@auth.login_required
	def get(self):
		token = g.user.generate_auth_token(84600)
		return jsonify({'token': token.decode('ascii'), 'duration': 86400})