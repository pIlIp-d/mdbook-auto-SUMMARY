#!/usr/bin/env python3

import os, time, re
from datetime import datetime

#config
ROOT_DIR="/".join(os.path.realpath(__file__).split("/")[:-1])+"/src/"
print(ROOT_DIR)

def save_file(path, str):
    with open(path, "w+") as f:
        f.write(str)

def remove_index_and_summary(file_list):
    # removes index.md and SUMMARY.md from file_list
    regex = re.compile(r'.*index.md$|.*SUMMARY.md$')
    return [i for i in file_list if not regex.match(i)]

def create_md(depth, directory, filename = "index.md", index_files = True):
    ''' recursively get markdown from directory tree
    param:  depth       - directory depth for indentation 
    param:  directory   - dir to folder wich is beeing processed
    param:  filename    - either SUMMARY.md or index.md
    param:  index_files - TRUE: index.md files are created, FALSE: they are not created
    return: md          - markdown of folders and their files'''

    #create currently highest level links
    if filename == "SUMMARY.md":
        md = "* [Main Page](./SUMMARY.md)\n"
    elif filename == "index.md":
        rel_dir = directory.replace(ROOT_DIR,"")[:-1]
        md = "* ["+ rel_dir.split("/")[-1] +"]" #Folder Name
        md += "(./" + rel_dir +"/index.md)\n"   #folder Path
    #iterate through directory tree
    for dir in remove_index_and_summary(os.listdir(directory)):
        #if Directory
        if os.path.isdir(directory+dir):
            dir_md = create_md(depth + 1, directory+dir+"/", index_files=index_files)#create markdown recursively
            md += depth*"\t" + dir_md+"\n"#add indentation
            #### index.md ####
            dir_md = dir_md.replace(directory.replace(ROOT_DIR,"")+dir+"/","")
            # remove too-deep indentation (from SUMMARY.d indentation levels)
            row_list = []
            for row in [row for row in dir_md.split("\n") ]:
                row_list.append(row.replace((depth+1)*"\t","\t",1))
            dir_md = "\n".join(row_list)
            #save dir_md into current index.md
            save_file(directory+dir+"/index.md", dir_md)
        #if File
        elif dir[-3:] == ".md":
            md += depth*"\t" + "* ["+ dir.split("/")[-1][:-3] +"](./"+directory.replace(ROOT_DIR,"")+dir+")\n"
    return md

def __main__():
    md = "# Documentation\n"+create_md(0, ROOT_DIR, "SUMMARY.md")
    save_file(ROOT_DIR+ "SUMMARY.md", md)

if __name__ == '__main__':
    __main__()
