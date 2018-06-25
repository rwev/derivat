""" 
Changes:
    * added kill_proc_tree using psutil dependency. Required to kill further processes spawned by command (e.q. PyQt. 
Future changes:
    * ability to ignore / focus on specified subdirectories (or simply working directory)
    * integrate option parser
===================================================

From Eugene Tan (https://gist.github.com/jmingtan/1171288)
    "
    An extension of Steve Krenzel's autoreload script (https://github.com/stevekrenzel/autoreload)
    Changes:
        1. Allow user specified file extension white lists
        2. Check if a process is alive before killing it
    What follows is the original README.md file:
        Autoreload is a simple python script to watch a directory for changed files and restarts a process when the change is detected.
        To use autoreload:
            1. Make sure the script is executable by running chmod +x autoreload
            2. Run ./autoreload <command to run and reload>
            3. For instance, I run ./autoreload python main.py. This first runs python main.py, then watches the current working directory and all subdirectories for changes. If any changes are detected, then the process is killed, and started all over again.
    "
"""

import re
import os
import sys
import subprocess
import time
import psutil

# only allows the use of blacklist OR whitelist (recommend change)
blacklist = ["^\.", "\.swp$"]
whitelist = []

def file_filter(name):
    def run_filters(name, filters):
        for regex in filters:
            if re.search(regex, name):
                return True
        return False
    if len(whitelist) > 0:
        return run_filters(name, whitelist)
    else:
        return not run_filters(name, blacklist)

def file_times(path):
    for root, dirs, files in os.walk(path, topdown = True):
        # print root
        for file_name in filter(file_filter, files):
            yield os.stat(os.path.join(root, file_name)).st_mtime
 
def print_stdout(process):
    stdout = process.stdout
    if stdout != None:
        print stdout

if len(sys.argv) <= 1:
    print "Autoreload - Restarts a process upon file changes."
    print "Usage:"
    print "  %s [-f filter] command" % sys.argv[0]
    print
    print "  -f filter    optional file extension (e.g. *.py)"
    print "               can be repeated multiple times"
    sys.exit(0)

command_index = 1
while sys.argv[command_index] == '-f':
    file_rule = sys.argv[command_index + 1]
    if file_rule.startswith('*'):
        file_rule = file_rule[1:]
    whitelist.append("%s$" %file_rule)
    command_index += 2

# We concatenate all of the arguments together, and treat that as the command to run
command = ' '.join(sys.argv[command_index:])

# The path to watch
path = './components'

# How often we check the filesystem for changes (in seconds)
wait = 1

# The process to autoreload
# set system/version dependent "start_new_session" analogs
def kill_proc_tree(pid, including_parent=True):    
    parent = psutil.Process(pid)
    # recursive option includes child, grandchildren (further generations)
    children = parent.children(recursive=True) 
    for child in children:
        child.kill()
    gone, still_alive = psutil.wait_procs(children, timeout=5)
    if including_parent:
        parent.kill()
        parent.wait(5)

# shell=False => do not spawn shell process first. Results in fewer processes to kill.
process = subprocess.Popen(command, shell=False)  

# The current maximum file modified time under the watched directory
last_mtime = max(file_times(path))

while True:
    max_mtime = max(file_times(path))
    print_stdout(process)
    if max_mtime > last_mtime:
        last_mtime = max_mtime
        try: 
            kill_proc_tree(process.pid)
        except:
            pass
        process = subprocess.Popen(command, shell=False)
    time.sleep(wait)