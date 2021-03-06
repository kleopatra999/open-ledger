import os
import time

from fabric.api import local, settings, abort, run, cd, env, put, sudo, hosts
from fabric.contrib.console import confirm

timestamp="release-%s" % int(time.time() * 1000)

CODE_DIR = '/home/liza/open-ledger'
CURRENT_BRANCH = 'master'

def deploy():
    with cd(CODE_DIR):
        run('git pull --force origin ' + CURRENT_BRANCH)
        run('./venv/bin/pip install -r requirements.txt')
    restart_host()

def restart_host():
    sudo('service openledger restart', shell=False)
