import requests
import json
import ast
import os
import argparse
import sys



parser=argparse.ArgumentParser(description="Check Host service status through NAGIOS API")
parser.add_argument('-s', '--server', type=str, metavar='', required=True, help='This should be the Nagios server FQDN')
parser.add_argument('-f', '--file', metavar='', help="Flat file containg the list of Nagios clients.")
parser.add_argument('-H', '--host', metavar='', help="Single host to scan")
args=parser.parse_args()

def get_status(url):
      data=requests.get(url).json()
      for i,j in data.items():
        if j["current_state"] == "3":
          if args.file:
            print "Hostname:- {}".format(server.strip('\n'))
          else:
            print "Hostname:- {}".format(args.host)
          print "Service:- {}".format(j["service_description"])
          if j["notifications_enabled"] == "1":
            print "Notifications has been enabled"
          elif j["notifications_enabled"] == "0":
            print "Notifications has been disabled"
          else:
            print "Notification:- {}".format(j["notifications_enabled"])
          print "Checks enabled:- {}".format(j["active_checks_enabled"])
          print j["plugin_output"] + "\n"


if args.file and args.host:
  sys.tracebacklimit=0
  raise Exception("Cannot use both parameters for target. Either use -H or -f.")
elif args.file:
 with open(args.file, 'r') as f:
  for server in f:
    try:
      url="http://{}:4567/_status/{}/_services".format(args.server,server.strip('\n'))
    except Exception as e:
      print  "Unable to fetch data from API"
    get_status(url)
elif args.host:
   try:
     url="http://{}:4567/_status/{}/_services".format(args.server,args.host)
   except:
     print  "Unable to fetch data from API"
   get_status(url)
else:
  sys.tracebacklimit=0
  raise Exception("Either use -f or -H option to target servers.!!")
