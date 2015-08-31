from flask import render_template, flash, redirect, request, jsonify
from app import app
from .forms import RegisterForm
from .forms import DeleteForm
from .api import DNSAPI, UserAPI, Token
from flask.ext.restful import Api, Resource, reqparse
import json
api = Api(app)
domain = '.example.com'

#main route that redirects to registration web app.
@app.route('/')
def index():
    return redirect('/register')
@app.route('/register', methods=['GET', 'POST'])

# Registration web form that is at url/register
def register():
    form = RegisterForm()
    if request.method == 'POST':
        host = form.hostname.data + domain
        ip = form.ipaddress.data
        records = {}
        #Opens file and inputs into records dict with hostname as key and IP address as value. 
        with open('/etc/hosts.txt', 'r+b') as f:
            for line in f:
                k, v = line.strip().split("  ")
                records[v.strip()] = k.strip()
           
        if host in records.keys():
            flash("The hostname %s is already registered to the ip address %s." % (host, records[host]))
        
        else:
            #Inputs records dict, with new recorded added into /etc/os_hosts.txt in format ip address, hostname. 
            with open('/etc/host.txt', 'r+b') as f:
                records[host] = ip
                f.writelines('{}  {}\n'.format(v, k) for k, v in records.items())
                f.truncate()
                #restart_service('dnsmasq')
                flash("The hostname %s has been registered to the ip address %s." %(host, ip)) 	
    return render_template('register.html', title='Register', form=form)

@app.route('/delete', methods=['GET', 'POST'])

def delete():
    form = DeleteForm()
    if request.method == 'POST':
        host = form.hostname.data + domain
        ip = form.ipaddress.data
        records = {}
        ipaskey = {}
        with open('/etc/hosts.txt', 'r+b') as f:
            for line in f:
                k, v = line.split("  ")
                records[v.strip()] = k.strip()
        with open('/etc/hosts.txt', 'r+b') as f:
            for line in f:
                k, v = line.split("  ")
                ipaskey[k.strip()] = v.strip()
         
        if host != domain:
            try:
                del records[host]
                with open('/etc/hosts.txt', 'r+b') as f:
                    f.writelines('{}  {}\n'.format(v, k) for k, v in records.items())
                    f.truncate() 
                    flash("The record for %s has been removed." % host)

            except KeyError:
                flash("The record for %s was not found." % host)

        
        else:
            try:
                hostname = ipaskey[ip]
                del ipaskey[ip]
                with open('/etc/hosts.txt', 'r+b') as f:
                    f.writelines('{}  {}\n'.format(k, v) for k, v in ipaskey.items())
                    f.truncate() 
                    flash("The record for %s registered to %s has  been removed." % (ip, hostname))

            except KeyError:
                flash("The record for %s was not found." % ip)


    return render_template('delete.html', title='Delete', form=form)

@app.route('/test', methods=['GET'])
def test():
    pass


api.add_resource(DNSAPI, '/api/v1.0/dns', endpoint = 'dns')
api.add_resource(UserAPI, '/api/v1.0/users', endpoint = 'users')
api.add_resource(Token, '/api/v1.0/token', endpoint = 'token')

def restart_service(name):
    command = ['/usr/bin/service', name, 'restart'];
    subprocess.call(command, shell=False)
