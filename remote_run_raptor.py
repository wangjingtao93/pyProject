#!/usr/bin/env python2
# coding: utf-8

import pexpect

if __name__ == '__main__':
    user = 'root'
    ip = '192.168.56.125'
    mypassword = '123456'

    child = pexpect.spawn('ssh %s@%s' % (user,ip))
    child.expect ('password:')
    child.sendline (mypassword)

    child.expect('#')
    child.sendline("run_start_BMs.py -deploy_conf /root/conf-raptor/deploy_conf")
    child.expect ('password:')
    child.sendline (mypassword)

    child.expect('#')
    child.sendline("run_create_meta_table.py -deploy_conf /root/conf-raptor/deploy_conf")
    child.expect ('password:')
    child.sendline (mypassword)