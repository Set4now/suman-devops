from subprocess import Popen, PIPE
import subprocess
import sys
import logging
import json

from subprocess import Popen, PIPE

#output=""
logging.basicConfig(format='%(asctime)s-%(message)s', level=logging.INFO)



def run(command):
    #global output
    process = Popen(command, stdout=PIPE, stderr=subprocess.STDOUT, shell=True)
    while True:
          output=""
          line = process.stdout.readline()
          line = line.decode()
          if (line == ""): break
          output += line
          logging.info(output.rstrip())

if __name__ == "__main__":
    for path in run("echo suman"):
      print path
