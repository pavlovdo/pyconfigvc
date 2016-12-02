#!/usr/bin/env python3

from configread import configread
from datetime import datetime
import os
from pygit2 import Repository, Signature, init_repository
from pynetdevices import CiscoASA, CiscoNexus, CiscoRouter, CiscoSwitch

git_init = False

conf_file = '/etc/orbit/' + os.path.basename(__file__).split('.')[0] + '.conf'

# Read the configuration file with parameters,
# location of configuration file - as in production system
asa_parameters = configread(conf_file, 'CiscoASA', 'enablepw')

git_parameters = configread(conf_file, 'GIT', 'author_name', 'committer_name',
                            'author_email', 'committer_email')

nd_parameters = configread(conf_file, 'NetworkDevice', 'login', 'password',
                           'slack_hook', 'device_file', 'savedir')

if not os.path.isdir(nd_parameters['savedir']):
    os.makedirs(nd_parameters['savedir'])

# Try to create object repository if repository is already exist
try:
    repo = Repository(nd_parameters['savedir'])
except KeyError:
    repo = init_repository(nd_parameters['savedir'])
    git_init = True

# Build the index of repository
index = repo.index

device_list_file = open(nd_parameters['device_file'])

# Parse the device file
for device_line in device_list_file:
    device_params = device_line.split(':')
    device_type = device_params[0]
    device_name = device_params[1]
    device_ip = device_params[2]

    if device_type == 'ciscoasa':
        device = CiscoASA(device_name, device_ip, nd_parameters['slack_hook'],
                          nd_parameters['login'],
                          nd_parameters['password'],
                          asa_parameters['enablepw'])

    if device_type == 'cisconexus':
        device = CiscoNexus(device_name, device_ip,
                            nd_parameters['slack_hook'],
                            nd_parameters['login'],
                            nd_parameters['password'])

    if device_type == 'ciscorouter':
        device = CiscoRouter(device_name, device_ip,
                             nd_parameters['slack_hook'],
                             nd_parameters['login'],
                             nd_parameters['password'])

    if device_type == 'ciscoswitch':
        device = CiscoSwitch(device_name, device_ip,
                             nd_parameters['slack_hook'],
                             nd_parameters['login'],
                             nd_parameters['password'])

#   Get and save configuration of each network device
    device_config = device.getConfig()
    device.saveConfig(device_config, nd_parameters['savedir'])
    diff = index.diff_to_workdir()
    if diff.patch:
        print (diff.patch + '\n')
#   Add configuration of network device to index cache
    index.add(device_name)

# Prepare to commit
author = Signature(git_parameters['author_name'],
                   git_parameters['author_email'])
committer = Signature(git_parameters['committer_name'],
                      git_parameters['committer_email'])
# reference = 'refs/HEAD'
reference = 'refs/heads/master'

# Build the message
year = datetime.now().strftime('%Y')
month = datetime.now().strftime('%m')
day = datetime.now().strftime('%d')
hour = datetime.now().strftime('%H')
message = 'Commit repository changes at ' + year + month + day + hour

# Save the new index of repository (git add)
index.write()

tree_oid = index.write_tree()
# tree_oid = repo.TreeBuilder().write()
if not git_init:
    # Get previous commit (parent)
    parent_commit = repo.revparse_single('HEAD')
    commit_oid = repo.create_commit(reference, author, committer, message,
                                    tree_oid, [parent_commit.oid])
else:
    commit_oid = repo.create_commit(reference, author, committer, message,
                                    tree_oid, [])
