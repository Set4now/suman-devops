import requests
import os
import subprocess
import json



#dfw_url_data=requests.get(dfw_url).json()
#dal_url_data=requests.get(dal_url)

with open("hostfile", 'r') as f:
    host_all=f.readlines()

for host in host_all:
    dfw_url = "http://{0}:4567/_status/{1}/_services".format("", host.strip("\n"))
    dfw_url_data=requests.get(dfw_url).json()
    
    for dfw_service,dfw_status in dfw_url_data.items():
        if "active_checks_enabled" in dfw_status.keys():
          if dfw_status["active_checks_enabled"] == "0":
             cmd="ng_disable_check -H {0} -s {1} -a s0d011k -c test".format(host.strip("\n"), dfw_service)
             subprocess.call(cmd, shell=True)
          if dfw_status["active_checks_enabled"] == "1":
            cmd="ng_enable_check -H {0} -s {1} -a s0d011k -c test".format(host.strip("\n"), dfw_service)
            subprocess.call(cmd, shell=True)
        else:
          cmd="ng_disable_notification -H {0} -a s0d011k -c STRTPL-1632 -y".format(host.strip("\n"))
          subprocess.call(cmd, shell=True)
          with open('status.txt', 'a') as f:
             report="Issue found:- {0}\n".format(host.strip("\n"))
             f.write(report)
        if "notifications_enabled" in dfw_status.keys():
          if dfw_status["notifications_enabled"] == "0":
            cmd="ng_disable_notification -H {0} -s {1} -a s0d011k -c test".format(host.strip("\n"), dfw_service)
            subprocess.call(cmd, shell=True)
          if dfw_status["notifications_enabled"] == "1":
            cmd="ng_enable_notification -H {0} -s {1} -a s0d011k -c test".format(host.strip("\n"), dfw_service)
            subprocess.call(cmd, shell=True)
#        else:
#          cmd="ng_disable_notification -H {0} -a s0d011k -c STRTPL-1632 -y".format(host.strip("\n"))
#          subprocess.call(cmd, shell=True)
#          with open('status.txt', 'a+') as f:
#             report="Issue found:- {0}\n".format(host.strip("\n"))
#             content=f.readlines()
#             if report not in content:
#               f.write(report)
