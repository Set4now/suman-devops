

import requests
import json
import ast
import os
import argparse
import sys
import re



parser=argparse.ArgumentParser(description="Check Host service status for any UNKNOWN status through NAGIOS API")
parser.add_argument('-s', '--server', type=str, metavar='', required=True, help='This should be the Nagios server FQDN')
parser.add_argument('-f', '--file', metavar='', help="Flat file containg the list of Nagios clients.")
parser.add_argument('-o', '--outputfile', metavar='', help="Output file")
parser.add_argument('-H', '--host', metavar='', help="Single host to scan")
args=parser.parse_args()

#url="http://{}:4567/_status/{}/_services".format(args.server,args.host)
#url="http://{}:4567/_status/{}/_services".format('dfw-mon1.prod.walmart.com', 'dal-sc-vpr2-r1')
""" 
This script with fetch you nodes with disabed notifications or services.
Note:- This is using Nagios API.

Troubleshooting when getting error/exceptions like unable to fetch details from API
1. Check the Nagios server/fqdn ( Tips: use the same Nagios server monitoring GUI fqdn)
2. check the host domain name ( Tips: Same as above)
  
"""

class App:


  def __init__(self, service):
    self.service = service
    a=re.compile(r"\w+:\w+:\w+:(\w+):\w+:\w+:\w+\w+\w+")


  def new_host(self):
    a=re.compile(r"\w+:\w+:\w+:(\w+):\w+:\w+:\w+\w+\w+")
    b=a.search(self.service).group(1)
    new_str="{}{}\n".format(b, "~")
    final=re.sub(b, new_str, self.service)
    return final

def get_status(server, host):
  url="http://{}:4567/_status/{}/_services".format(server, host)
  try:
    data=requests.get(url).json()
    if args.outputfile:
      with open(args.outputfile, 'a') as f:
        #f.write("{}Status of {}{}\n".format(("=" * 10), host, ("=" * 10)))
        for i,j in data.items():
          service=App(i)
          if j["active_checks_enabled"] == "0" or  j["notifications_enabled"] == "0":
             if j["active_checks_enabled"] == "0":
               f.write("{}~Service Disabled~{}\n".format(host, service.new_host()))
             if j["notifications_enabled"] == "0":
               f.write("{}~Notification Disbaled~{}\n".format(host, service.new_host()))
    else:
       #print "{}Status of {}{}\n".format(("=" * 10), host, ("=" * 10))
       for i,j in data.items():
          service=App(i)
          if j["active_checks_enabled"] == "0" or  j["notifications_enabled"] == "0":
             if j["active_checks_enabled"] == "0":
               print "{}~Service Disabled~{}".format(host, service.new_host())
             if j["notifications_enabled"] == "0":
                print "{}~Notification Disabled~{}".format(host, service.new_host())

  except:
    print  "Unable to fetch data from API for {}".format(host)



if args.file and args.host:
  sys.tracebacklimit=0
  raise Exception("Cannot use both parameters for target. Either use -H or -f.")
elif args.file:
 with open(args.file, 'r') as f:
      #url="http://{}:4567/_status/{}/_services".format(args.server,server.strip('\n'))
    for nodes in f:
      get_status(server=args.server, host=nodes.strip('\n'))
elif args.host:
#     url="http://{}:4567/_status/{}/_services".format(args.server,args.host)
     get_status(server=args.server, host=args.host)
else:
  sys.tracebacklimit=0
  raise Exception("Either use -f or -H option to target servers.!!")
