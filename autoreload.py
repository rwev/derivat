""" 
Changes:
    * added kill_proc_tree using psutil dependency. Required to kill further processes spawned by command (e.q. PyQt. 
    * added proper option parser and extended the ability to specify parameters
    * only find matching files once (added files are not accounted for; script must be restarted )
Future changes:
    * add function commentary
    * remove blacklist functionality, only used whitelist
    * log observed file changed to console w/ timestamp
    * ability to specify regex to match directories
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
from __future__ import print_function

import re
import os, sys, subprocess
import time
import psutil
from optparse import OptionParser

def string_list_callback(option, opt, value, parser):
  setattr(parser.values, option.dest, value.split(','))

parser = OptionParser()

parser.add_option(
    '-w', '--cwd',
    action = 'store_true',
    dest = 'do_observe_current_directory',
    default = False,
    help = 'Observe the current working directory'
)
parser.add_option(
    '-t', '--extensions',
    dest = "regex_file_patterns_to_observe",
    type = 'string',
    default = [],
    action = 'callback',
    callback = string_list_callback,
    help = "Comma-separated, spaceless list of file patterns to be observed"
)
parser.add_option(
    '-d', '--dirs',
    dest = 'additional_subdirectories_to_observe',
    type = 'string',
    default = [],
    action = 'callback',
    callback = string_list_callback,
    help = "Comma-separated, spaceless list of subdirectories (below the working directory) to be observed"
)
parser.add_option(
    '-x', '--command',
    dest = 'command_to_run_str',
    type = 'string',
    default = '',
    help = "Command to run, restart on detected file changes, in single quotes"
)
parser.add_option(
    '-i', '--interval',
    dest = 'file_check_interval_seconds',
    type = 'float',
    default = 1,
    help = "Interval in seconds between checks for file changes."
)
(options, args) = parser.parse_args(sys.argv)

##### ARGUMENT CHECKS #####
# must monitor at least one directory
if ((not options.do_observe_current_directory) and (not len(options.additional_subdirectories_to_observe))):
    print('At least one directory must be observed: use argument(s) \'-w\' and / or \'-d\'.')
    sys.exit(0)
if (not options.command_to_run_str):
    print('Must specify command to execute with \'-x\' argument.')
    sys.exit(0)
if (not len(options.regex_file_patterns_to_observe)):
    print ('Must specify command at least one regex pattern matching files to be watched.')

# only allows the use of blacklist OR whitelist (recommend change)
blacklist = ["^\.", "\.swp$"]
whitelist = []
for regex_rule in options.regex_file_patterns_to_observe:
    if regex_rule.startswith('*'):
        regex_rule = regex_rule[1:]
    whitelist.append("%s$" % regex_rule)

##### DEFINE CORE LOGIC #####
def get_observed_relative_filepaths_for_directory(relative_dir, include_subdirs = False):
    # returns list of relative paths to files to be observed
    relative_filepaths = []
    if include_subdirs:
        for root, dirs, files in os.walk(relative_dir, topdown = True):
            for filename in files:
                if run_filters(filename, whitelist):
                    relative_filepaths.append(os.path.join(root, filename))
    else:
        files = get_files_in_directory(relative_dir)
        for filename in files:
            if run_filters(filename, whitelist):
                relative_filepaths.append(os.path.join(relative_dir, filename))
    return relative_filepaths

def get_files_in_directory(dir): 
    return [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]

def run_filters(name, filters):
    for regex in filters:
        if re.search(regex, name):
            return True
    return False
def file_filter(name):
    if len(whitelist) > 0:
        return run_filters(name, whitelist)
    else:
        return not run_filters(name, blacklist)
def get_file_modification_times(relative_filepaths):
    for filepath in relative_filepaths:
        yield os.stat(filepath).st_mtime

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
def print_stdout(process):
    stdout = process.stdout
    if stdout != None:
        print (stdout)
        
##### PROCESS ARGUMENTS #####
command = options.command_to_run_str
wait = options.file_check_interval_seconds

filepaths_to_watch = []
if (options.do_observe_current_directory):
    filepaths_to_watch.extend(get_observed_relative_filepaths_for_directory('.', include_subdirs=False))
for dir in options.additional_subdirectories_to_observe:
    filepaths_to_watch.extend(get_observed_relative_filepaths_for_directory(dir, include_subdirs=True))

print('Watching files:')
for filepath in filepaths_to_watch:
    print('\t%s' % filepath)

##### SPAWN PROCESS AND OBSERVATION LOOP ##### 
# The current maximum file modified time under the watched directory
last_mtime = max(get_file_modification_times(filepaths_to_watch))
# shell=False => do not spawn shell process first. Results in fewer processes to kill.
process = subprocess.Popen(command, shell=False)

while True:
    max_mtime = max(get_file_modification_times(filepaths_to_watch))
    print_stdout(process)
    if max_mtime > last_mtime:
        last_mtime = max_mtime
        try: 
            kill_proc_tree(process.pid)
        except:
            pass
        process = subprocess.Popen(command, shell=False)
    time.sleep(wait)