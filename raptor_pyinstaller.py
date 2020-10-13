#!/usr/bin/env python2
# coding: utf-8
import paramiko
import os
import re
import unittest
from multiprocessing import Pool

pyinstaller_workpath = './pyinstaller-work'  # pyinstaller工作目录
def pyinstaler_exec(i):
    cmd_create_workpath =  'mkdir -p ' + pyinstaller_workpath
    val = os.system(cmd_create_workpath)

    py_path = '/root/raptor/raptorstor/output/bin'
    exec_str = "/usr/bin/pyinstaller -y ";

    path_str = py_path + '/'+ Symphony_py[i] + " -p "+ py_path + '/proto' + ' --distpath=' + \
               pyinstaller_workpath + ' --workpath=' + pyinstaller_workpath + "/build" + ' --specpath=' + pyinstaller_workpath

    cmd = exec_str + path_str
    val = os.system(cmd)


def remove_index(endpoint):
    '''
    usage:   格式化，根据逗号拆分，变成list格式，并删掉index
    入参：   endpoint={str}'127.0.0.1:20000:0, 127.0.0.1:20101:0, 127.0.0.1:20202:0
    return:  endpoint= <type 'list'>: ['127.0.0.1:20202', '127.0.0.1:20101', '127.0.0.1:20000']
    '''
    #判断类型是否是list
    if type(endpoint) == type([]):
        if endpoint[0][-2:] == ':0':
            return [t[:-2] for t in endpoint]
        else:
            return endpoint

    tmp = re.split(r'[ .]', endpoint) #根据逗号拆分，存储到tmp=<type 'list'>: ['127.0.0.1:20000:0', '127.0.0.1:20101:0', '127.0.0.1:20202:0']
    endpoint = [t for t in tmp if t != '']
    if endpoint[0][-2:] == ':0':
        endpoint = [e[:-2] for e in endpoint]

    return endpoint

def raptor_union(i):
    pyinstaller_raptor_outpath = './pyinstaller-raptor'#取并集的结果存放路径
    cmd_create_path = 'mkdir -p ' + pyinstaller_raptor_outpath
    val = os.system(cmd_create_path)

    tmppath = remove_index(Symphony_py[i])
    cmd = 'cp -rn ' + pyinstaller_workpath + '/' + tmppath[0]+ '/*' + ' ' + pyinstaller_raptor_outpath
    val = os.system(cmd)


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)

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
            raise AuthenticationFailed(
                'Password error. User {user} on host {hostname}, wrong password: {pwd}'.format(user=user,
                                                                                               hostname=hostname,
                                                                                               pwd=pwd))

        stdin, stdout, stderr = sshcli.exec_command(cmd)

        exit_code = stdout.channel.recv_exit_status()
        outputs = [line.strip() for line in stdout.readlines()]
        errmsgs = [line.strip() for line in stderr.readlines()]

        return (exit_code, outputs, errmsgs)



Symphony_py = ["run_start_BMs.py", "run_add_BDs.py", "run_clean_pool.py","run_create_pool.py", "run_start_BNs.py",
               "run_create_meta_tables.py", "run_deploy.py", "run_rebalance_leaders.py", "run_generate_move_tasks.py",
               "run_check_leader_distribution.py", "run_do_move_tasks.py", "run_move_tables.py",
               "run_start_BDs.py", "raptor.py"]

if __name__ == '__main__':
    #unittest.main()

    pool = Pool(processes=10)
    for i in xrange(len(Symphony_py)):
        '''
        For循环中执行步骤：
        （1）循环遍历，将len(Symphony_py)个子进程添加到进程池（相对父进程会阻塞）
        （2）每次执行10个子进程，等一个子进程执行完后，立马启动新的子进程。（相对父进程不阻塞）

        apply_async为异步进程池写法。
        异步指的是启动子进程的过程，与父进程本身的执行（print）是异步的，而For循环中往进程池添加子进程的过程，与父进程本身的执行却是同步的。
        '''
        pool.apply_async(pyinstaler_exec, args=(i,))  # 维持执py行的进程总数为10，当一个进程执行完后启动一个新进程.
    pool.close()
    pool.join()

    for i in xrange(len(Symphony_py)):
        raptor_union(i)



    #print remove_index('wangjingtao:hello:world')


