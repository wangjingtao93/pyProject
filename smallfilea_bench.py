#!/usr/bin/python
# -*- coding: utf-8 -*-

filecount = 30
filesize = 1024

import random, time
from os import system

if __name__ == "__main__":
    flush = "sudo su -c 'sync; echo 3> /proc/sys/vm/drop_caches'"  # 看不懂干啥

    randfile = open("/dev/urandom", "r")  # 只读方式打开，这个是外设啥啥文件

    print "\ncreate test folder"
    startime = time.time()
    system("rm -rf test && mkdir test")
    print time.time() - startime
    system(flush)

    print "\ncreate files"
    startime = time.time()
    for i in xrange(int(filecount / 10)):
        rand = randfile.read(int(filesize * 0.5 + filesize * random.random()))
        outfile = open("test/" + unicode(i), "w")
        outfile.write(rand)
    print time.time() - startime

    print "\nrewrite files:"
    startime = time.time()
    for i in xrange(int(filecount / 10)):
        rand = randfile.read(int(filesize * 0.5 + filesize * random.random()))
        outfile = open("test/" + unicode(int(random.random()*filecount)), "w")
        outfile.write(rand)
    print time.time() - startime


    print "\nread linear:"
    startime = time.time()
    for i in xrange(int(filecount / 10)):
        infile = open("test/" + unicode(i), "r")
        outfile.write(infile.read());
    print time.time()
    system(flush)
