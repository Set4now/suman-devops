#!/usr/bin/env python
import subprocess
import os
import sys
import argparse
from subprocess import *


parser=argparse.ArgumentParser(description="Check File system status across CLuster")
parser.add_argument('-f', '--file', metavar='', help="Flat file containg the list of Nagios clients.")
args=parser.parse_args()

failed_cluster_nodes_list=[]

if args.file:
    with open(args.file, 'r') as clustered_nodes:
        for cluster_node in clustered_nodes:
            nrpe_cmd="/Monitoring/nagios/libexec/check_nrpe -H {0} -p 12124".format(cluster_node.strip('\n'))
            nrpe_status = subprocess.Popen(nrpe_cmd, shell=True, stdout=PIPE)
            nrpe_output = nrpe_status.communicate()
            #print nrpe_output
            #print nrpe_output[0].strip('\n').split(' ')[0]
            if nrpe_output[0].strip('\n').split(' ')[0] == "NRPE":
                cmd='/Monitoring/nagios/libexec/check_nrpe -H {0} -p 12124 -t 400 -c check_wm_wrapper -a "-c check_disk -a \\"-e -w 25% -c 10% -E -p /u01/app/ggsuser -p /u01/app/ggtrail \\""'.format(cluster_node.strip('\n'))
                #print cmd
                disk_check=subprocess.Popen(cmd, shell=True, stdout=PIPE)
                disk_output=disk_check.communicate()
                #print disk_output
                #print disk_output[0].strip("\n").split(" ")[1]
                #print cluster_node.strip('\n')
                if disk_output[0].strip("\n").split(" ")[1] == "OK|":
                    print "OK- Current Monitored  Node is {0} - {1}".format(cluster_node.strip('\n'), disk_output[0].strip("\n").split(" ")[2:])
                    status=0
                    #sys.exit(0)
                elif disk_output[0].strip("\n").split(" ")[1] == "WARNING":
                    print "WARNING- Current Monitored  Node is {0} - {1}".format(cluster_node.strip('\n'), disk_output[0].strip("\n").split(" ")[2:])
                    status=1
                    #sys.exit(1)
                elif disk_output[0].strip("\n").split(" ")[1] == "CRITICAL":
                    print "CRITICAL- Current Monitored  Node is {0} - {1}".format(cluster_node.strip('\n'), disk_output[0].strip("\n").split(" ")[2:])
                    status=2
                    #sys.exit(2)
                else:
                    #print "UNKNOWN- THE ENTIRE CLUSTER MAY BE  DOWN"
                    print "UNKNOWN- Check the cluster nodes  manually"
                    status=3
                    #sys.exit(3)
                break
                failed_cluster_nodes_list.append(cluster_node.strip('\n'))
        num_lines=0
        with open(args.file, 'r') as f:
                for line in f:
                   num_lines += 1
        if len(failed_cluster_nodes_list) == num_lines:
            print "CRITICAL- Cluster is DOWN"
            status=2


else:
  sys.tracebacklimit=0
  raise Exception("use the -f option to  provide  the file path containing list of target clustered node")



sys.exit(status)

