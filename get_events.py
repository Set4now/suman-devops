import json
import subprocess
import os
import select
import sys

token_directory="/var/run/secrets/kubernetes.io/serviceaccount/token"
with open('/var/run/secrets/kubernetes.io/serviceaccount/token', 'r') as f:
    token=f.read()
#print token
ca_cert="/var/run/secrets/kubernetes.io/serviceaccount/ca.crt"
kube_api_server="https://kubernetes.svc.local"
kube_api_port="443"

args='curl --cacert /var/run/secrets/kubernetes.io/serviceaccount/ca.crt -H "Authorization: Bearer {}" https://kubernetes.default.svc/api/v1/watch/events -k'.format(token)
#print args


process=subprocess.Popen(args, shell=True, stdout=subprocess.PIPE, bufsize=1)
out=select.poll()
out.register(process.stdout)

while True:
    if out.poll(1):
        print process.stdout.readline().strip("\n")

