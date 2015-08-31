# RestfulDNS

RestfulDNS is a rest api and web app wrapper for dnsmasq written in Python using the Flask web framework. It allows for the creation, deletion, and listing of dns records to provide DNS as a service. 
It is useful in an environment such as an internal Openstack where you have a large number of developers wanting to register and remove DNS records, without having to have somebody process each request.


My prefered method of running this is to use the flask built in webserver, and use an nginx ssl proxy to handle SSL offloading. It is much faster and easier to configure, then trying to run SSL in flask.

To run this program you will need to install dnsmasq on your system, and create the file /etc/hosts.txt. You will need to configure dnsmasq to look at the file /etc/hosts.txt file for hosts.

After configuring dnsmasq you will need to run the dbint.py script to intialize the database to store user authentication.

You have two options on how to run this, you can either execute run.py in the root program directory as superuser. Or you can set up a cron job that restarts the dnsmasq server every 5 minutes, or as quickly as you want the refresh to be, and then have the program run, and give that user access to the /etc/hosts.txt file. Security is best if you use the cron job, running as superuser is good for testing.






