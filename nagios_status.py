import requests
import json
import ast
import os
import argparse



parser=argparse.ArgumentParser(description="Check Host service status through NAGIOS API")
parser.add_argument('-s', '--server', type=str, metavar='', required=True, help='This should be the Nagios server FQDN')
parser.add_argument('-f', '--file', metavar='', help="Flat file containg the list of Nagios clients.")
parser.add_argument('-H', '--host', metavar='', help="Single host to scan")
args=parser.parse_args()

if args.file:
 with open(args.file, 'r') as f:
  for server in f:
    try:
      url="http://{}:4567/_status/{}/_services".format(args.server,server.strip('\n'))
      data=requests.get(url).json()
      for i,j in data.items():
        if j["current_state"] == "3":
          print "Hostname:- {}".format(server.strip('\n'))
          print "Service:- {}".format(j["service_description"])
          if j["notifications_enabled"] == "1":
            print "Notifications has been enabled"
          elif j["notifications_enabled"] == "0":
            print "Notifications has been disabled"
          else:
            print "Notification:- {}".format(j["notifications_enabled"])
          print "Checks enabled:- {}".format(j["active_checks_enabled"])
          print j["plugin_output"] + "\n"
    except Exception as e:
      print  "Unable to fetch data from API"
