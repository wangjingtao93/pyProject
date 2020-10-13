# -*- coding:utf-8 -*-

import os

def generate_conf(conf):
    with open("template.conf",'r',encoding="utf-8") as f1, open("rsync.conf","w",encoding="utf-8") as f2:
        new_line = []
        for line in f1:
            for k,v in conf_map.items():
                if k in line:
                    line = k+" = "+v + "\n"
            new_line.append(line)
        
        for line in new_line:
            f2.write(line)


if __name__ == "__main__":
    conf_map = {}
    conf_map["hosts allow"] = "192.168.56.173"
    conf_map["path"] = "/rsync-path"
    conf_map["comment"] = "this is a comment"
    generate_conf(conf_map)

    # with open("template.conf",'r',encoding="utf-8") as f1, open("rsync.conf","w",encoding="utf-8") as f2:
    #     new_line = []
    #     for line in f1:
    #         for k,v in conf_map.items():
    #             if k in line:
    #                 line = k+" = "+v + "\n"
    #         new_line.append(line)
        
    #     for line in new_line:
    #         f2.write(line)
