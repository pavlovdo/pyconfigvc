#!/usr/bin/env python3


class NetworkDevice:
    """ base class for network devices """

    def __init__(self, hostname, ip, slack_hook, login=None, password=None,
                 enablepw=None):

        self.hostname = hostname
        self.ip = ip
        self.login = login
        self.password = password
        self.enablepw = enablepw
        self.slack_hook = slack_hook


class CiscoDevice(NetworkDevice):
    """ base class for cisco devices """

    def getConfig(self, printing=False):

        import paramiko
        from pyslack import slack_post
        import sys

        conflist = []
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            client.connect(self.ip.rstrip(), username=self.login,
                           password=self.password, timeout=10,
                           allow_agent=False, look_for_keys=False)

            stdin, stdout, stderr = client.exec_command('show run')
            confbinary = stdout.read() + stderr.read()

            conftext = confbinary.decode("utf-8")
            conflist = conftext.split("\n")[4:]

            if printing:
                for confline in conflist:
                    print(confline)

            client.close()

        except:
            slack_post(self.slack_hook, 'Unexpected exception in ' +
                       str(self.__class__) + '.'
                       + str(sys.exc_info()),
                       self.hostname, self.ip)

        return conflist

    def saveConfig(self, conflist, savedir):

        fh = open(savedir + '/' + self.hostname, 'w')
        for confline in conflist:
            fh.write(confline + '\n')
        fh.close()


class CiscoASA(CiscoDevice):
    """ class for cisco asa """

    def getConfig(self, endstring=': end', printing=False):

        import paramiko

        conffull = ''
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(self.ip.rstrip(), username=self.login,
                       password=self.password, timeout=10,
                       allow_agent=False, look_for_keys=False)

        channel = client.invoke_shell()
        channel.send('enable\n')
        channel.send(self.enablepw + '\n')

        while True:
            channel.send('show run\n')
            confbinary = channel.recv(4096)
            conftext = confbinary.decode("utf-8")
            if endstring in conftext:
                endindex = conftext.find(endstring)
                conffull += conftext[:endindex]
                break
            conffull += conftext

        conflist = conffull.split("\n")[4:]

        if printing:
            for confline in conflist:
                print(confline)

        channel.close()
        client.close()

        return conflist


class CiscoNexus(CiscoDevice):
    """ class for cisco nexuses """
    pass


class CiscoRouter(CiscoDevice):
    """ class for cisco routers """
    pass


class CiscoSwitch(CiscoDevice):
    """ class for cisco switches """
    pass


class LinuxServer(NetworkDevice):
    """ class for linux servers """

    def getConfig(self, remotepath, tempdir='./tmp/',
                  use_key_pairs=True, printing=False):

        import os
        import paramiko

        self.tempdir = tempdir

        client = paramiko.SSHClient()
        client.load_system_host_keys()

        if use_key_pairs:
            client.connect(self.hostname)
        else:
            client.connect(self.hostname, username=self.login,
                           password=self.password)

        temppath = tempdir + os.path.basename(remotepath)
        sftp = client.open_sftp()
        sftp.get(remotepath, temppath)

        if printing:
            fhand = open(temppath, 'r')
            for line in fhand:
                print(line)

    def saveConfig(self, filename, savedir='./data', overwrite=True, vc=True):

        import os

        if not os.path.exists(savedir + '/' + self.hostname):
            os.mkdir(savedir + '/' + self.hostname)

        dstpath = savedir + '/' + self.hostname + '/' + filename
        if not os.path.isfile(dstpath) or overwrite:
            os.rename(self.tempdir + filename, dstpath)
        else:
            print('File ' + dstpath + ' is already exist, keep the old file')
