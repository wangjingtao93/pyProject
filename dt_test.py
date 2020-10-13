#!/usr/bin/python
# -*- coding: utf-8 -*-
from os import system
from multiprocessing import Pool

foldercount = 5

def dt_multi_exce(i):
    t = i+1
    cmd = "dt of=/mnt/nas-wjt0-" + str(t) + "/x" + str(t) + " bs=8k limit=50m dispose=keep"
    print cmd
    system(cmd)


if __name__ == "__main__":
    pool = Pool(processes = 5)
    for i in xrange(foldercount):
        '''
        For循环中执行步骤：
        （1）循环遍历，将len(Symphony_py)个子进程添加到进程池（相对父进程会阻塞）
        （2）每次执行10个子进程，等一个子进程执行完后，立马启动新的子进程。（相对父进程不阻塞）

        apply_async为异步进程池写法。
        异步指的是启动子进程的过程，与父进程本身的执行（print）是异步的，而For循环中往进程池添加子进程的过程，与父进程本身的执行却是同步的。
        '''
        print i
        pool.apply_async(dt_multi_exce, args=(i,))
    pool.close()
    pool.join()

    dt_multi_exce(1)
    print "task completed"


