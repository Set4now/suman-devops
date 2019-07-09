from subprocess import Popen, PIPE
import subprocess
import sys
import logging
import json

from subprocess import Popen, PIPE

token_directory="/var/run/secrets/kubernetes.io/serviceaccount/token"
with open('/var/run/secrets/kubernetes.io/serviceaccount/token', 'r') as f:
    token=f.read()
#print token
ca_cert="/var/run/secrets/kubernetes.io/serviceaccount/ca.crt"
kube_api_server="https://kubernetes.svc.local"
kube_api_port="443"

args='curl -s --cacert /var/run/secrets/kubernetes.io/serviceaccount/ca.crt -H "Authorization: Bearer {}" https://kubernetes.default.svc/api/v1/watch/events'.format(token)

#output=""
logging.basicConfig(format='%(asctime)s   %(process)d %(processName)s %(message)s', level=logging.INFO)



def run(command):
    #global output
    process = Popen(command, stdout=PIPE, stderr=subprocess.STDOUT, shell=True)
    while True:
          output=""
          line = process.stdout.readline().replace("null", '"Nothing"')
          #line = line.decode()
          if (line == ""): break
          output += line
          logging.info(output.rstrip())

if __name__ == "__main__":
    for path in run(args):
      print path
