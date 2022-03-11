# MdBook with auto index and SUMMARY gen

## Instalation

Install Rust `curl -sSf https://sh.rustup.rs | sh` \

Install MdBook `cargo install mdbook`

## Setup

`cd /var/www/website` \
create `summary_builder.py`
```python
#!/usr/bin/env python3

import os, time, re
from datetime import datetime

#config
ROOT_DIR="/".join(os.path.realpath(__file__).split("/")[:-1])+"/src/"
print(ROOT_DIR)
''' saves/creates File
    :param  path    - full or relative path as string
    :param  str     - string to be saved in file'''
def save_file(path, str):
    with open(path, "w+") as f:
        f.write(str)

''' removes list elements from list when they contain certain strings
    :param  file_list   - list of string/files
    :return file_list   - without index.md and SUMMARY.md string'''
def remove_index_and_summary(file_list):
    regex = re.compile(r'.*index.md$|.*SUMMARY.md$')
    return [i for i in file_list if not regex.match(i)]

''' recursively get markdown from directory tree
    param:  depth       - directory depth for indentation 
    param:  directory   - dir to folder wich is beeing processed
    param:  filename    - either SUMMARY.md or index.me
    param:  index_files - TRUE: index.md files are created, FALSE: they are not created
    return: md          - markdown of folders and ther files'''
def create_md(depth, directory, filename = "index.md", index_files = True):
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
            # remove to-deep indentation (from SUMMARY.d indentation levels)
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
```

create `notify.sh`
```bash
#!/bin/bash

P=/var/www/website/

inotifywait \
    --event create --event delete \
    --event modify --event move \
    --format "%f" \
    --monitor \
    --exclude '.*(.*index.md|.*SUMMARY.md)' \
    --recursive \
    ${P}src/ |
while read CHANGED;
do
	echo "$CHANGED"
	python3 ${P}summary_builder.py
	mdbook build ${P}
done
```
run `mdbook init`

instead of `mdbook watch` run ./notify.sh

## Usage

place `.md` Files in Folders into `src/` \

use samba share or git to sync files \

place images into src/... only
