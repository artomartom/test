#!/bin/python3
try: 
    import git    
except ImportError as e:
    print("import git  failed, pls  install python3-git" )

import argparse
import os 
import datetime
import shutil
import tempfile
import json 



def print_message(message):
    timestamp = datetime.datetime.now().time().strftime("%H:%M:%S")
    print (f"[{timestamp}] {message}")


def main():
    parser =  argparse.ArgumentParser(prog='repo_loader')
    parser.add_argument('reponame') 
    parser.add_argument('sourcepath') 
    parser.add_argument('version') 

    args= parser.parse_args()
    #print(args.reponame, args.sourcepath, args.version)

    print_message("recived arguments: ") 
    print_message(f"reponame: {args.reponame}") 
    print_message(f"path to source code: {args.sourcepath}") 
    print_message(f"build version: {args.version}") 

    reponame=  os.path.split(args.reponame)[-1]
    #print(reponame)
    git_url=args.reponame 
    repo_dir=f"./{reponame}"

    if   os.path.exists(repo_dir) == True:
        print_message (f"  repository  {repo_dir} already exists ")
    else: 
        print_message (f"start cloning {git_url} into   folder {repo_dir} ")
        git.Repo.clone_from(git_url, repo_dir)

    fullsourcepath = f"{repo_dir}/{args.sourcepath}"

    if os.path.exists(fullsourcepath) == False:
        print_message(f"source path {fullsourcepath}  does not exist")
        return 
    
    if os.path.isdir(fullsourcepath) == False: 
        print_message(f"sourcepath {fullsourcepath} have to be a directiory")
        return 

    print_message(f"moving source files from {fullsourcepath} to {repo_dir}")     
    with tempfile.TemporaryDirectory("temp") as tmpdir:
        sourceparentdir=os.path.split(fullsourcepath)[0]
        shutil.move(fullsourcepath,tmpdir)
        shutil.rmtree(f"./{reponame}/")
        #shutil.move(f"{tmpdir}/",repo_dir)
        for   file in os.listdir(tmpdir):
            shutil.move(f"{tmpdir}/{file}",repo_dir)
 

    version_filename= f"{repo_dir}/version.json" 

    print_message (f"writing version {args.version} to {version_filename}  ")
    with open (version_filename,'w') as file:
        listof_files = os.listdir(repo_dir)
        data =  { "name": "hello world ",
              "version": args.version, 
              "files": listof_files }
        json.dump(data,file,indent=4)
    print_message (f" {version_filename} successfully writen ")


    archivename = os.path.split(args.sourcepath)[1]
    today =datetime.date.today().strftime("%d%m%Y")

    print_message (f"creating archive  {archivename}.zip")
    shutil.make_archive ( f"{archivename}{today}","zip", repo_dir)
    print_message("success!") 





if __name__ == "__main__":
    try:
        main()
    except BaseException as e:
        print_message(e)
    


