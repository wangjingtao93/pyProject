#!/usr/bin/env python2
# coding: utf-8
import paramiko
import os
import pexpect

def run_os_popen():
    f = os.popen('ls -l', 'r')

    # f.read()和f.readlines()不能一块用
    d = f.read()
    #d_list = f.readlines()

    print d
    #print d_list
    f.close()

def run_pexpect():
    user = 'root'
    ip = '192.168.56.125'
    mypassword = '123456'
 
    print user
    child = pexpect.spawn('ssh %s@%s' % (user,ip))
    child.expect ('password:')
    child.sendline (mypassword)
    
    # print child.before
    # child.expect('$')
    # child.sendline('sudo -s')
    # print child.before

    # child.expect (':')
    # child.sendline (mypassword)
    # print child.before

    child.expect('#')
    child.sendline('ls -la')
    print child.before   # Print the result of the ls command.

    child.expect('#')
    child.sendline("echo '112' >> /root/123.txt ")
    print child.before

    child.interact()     # Give control of the child to the user.
 


def remote_execute(hostname, user, pwd, cmd):
    '''
    :param hostname: str
    :param user:     str
    :param pwd:      str
    :param cmd:      str
    :return:    exit_code: ,outputs=list[], errmsgs=list[]
    '''

    sshcli = paramiko.SSHClient()
    sshcli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        sshcli.connect(hostname, username=user, password=pwd, look_for_keys=False, allow_agent=False)
    except paramiko.ssh_exception.AuthenticationException:
        raise AuthenticationFailed('Password error. User {user} on host {hostname}, wrong password: {pwd}'.format(user=user, hostname=hostname, pwd=pwd))

    stdin, stdout, stderr = sshcli.exec_command(cmd)

    exit_code = stdout.channel.recv_exit_status()
    outputs = [line.strip() for line in stdout.readlines()]
    errmsgs = [line.strip() for line in stderr.readlines()]

    return (exit_code, outputs, errmsgs)




if __name__ == '__main__':

    #call remote treminal
    # flag = True
    # exit_code, output, errmsg = remote_execute('192.168.247.156', 'root', '123456', 'mkdir /root/tmp')
    # if exit_code != 0:
    #     flag = False
    #
    # print ' exit_code: {exit_code}, output: {output}, errmsg: {errmsg}'.format(
    #      exit_code=exit_code, output=output, errmsg=errmsg)

    #call local terminal
    #val = os.system("cd /root/pyinstaller-work;  /usr/bin/pyinstaller /root/raptor/raptorstor/output/bin/run_start_BDs.py "
                   # "-p /root/raptor/raptorstor/output/bin/proto/")
    # val = os.system("hostname -i | awk '{print $NF}'")
    # print 'val=', val
    print 'wjt begin'
    #run_os_popen()

    run_pexpect()