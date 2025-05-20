# all imports needed are listed below
import argparse # for parsing arguments taken from the command line input by the user
import configparser  # for configuration file format
from datetime import datetime #we will use some date and time features to make some git features
import grp, pwd # for detection of the group and user , to know whom a particular file belongs to ? 
from fnmatch import fnmatch   # to support .gitignore we need to match filenames against pattterns such as *.txt ,, etc .
import hashlib   # git uses sha-1 function quite extensively , so we will do it in python using this library
from math import ceil # this ceil function is used to ceil the values to the integer just greater than the provided decimal like if given a random input x , the output would be ([x] + 1 ) , where [.] represents G.I.F or greatest integer function 
import os # for using some os capabilities , maybe like ls, cd, etc
import re   # just  a bit of regular expressions
import sys  # we need sys to access command line arguments 
import zlib   # git compresses everything using zlib , so we will copy the same  , thanks to the developers of microsoft.


argparser = argparse.ArgumentParser(description='The Stupidest content tracker ever.')   #creating a argument parser using a python library 
argsubparsers = argparser.add_subparsers(title='Commands', dest='command')   # adding subparsers to our argument parser
argsubparsers.required = True   # statignt that the argument and subargument are necessary for this program to work 

#Next is the function in which we just match which function is being called

def main(argv=sys.argv[1:]):
    args = argparser.parse_args(argv)
    match args.command:
        case "add"          : cmd_add(args)
        case "cat-file"     : cmd_cat_file(args)
        case "check-ignore" : cmd_check_ignore(args)
        case "checkout"     : cmd_checkout(args)
        case "commit"       : cmd_commit(args)
        case "hash-object"  : cmd_hash_object(args)
        case "init"         : cmd_init(args)
        case "log"          : cmd_log(args)
        case "ls-files"     : cmd_ls_files(args)
        case "ls-tree"      : cmd_ls_tree(args)
        case "rev-parse"    : cmd_rev_parse(args)
        case "rm"           : cmd_rm(args)
        case "show-ref"     : cmd_show_ref(args)
        case "status"       : cmd_status(args)
        case "tag"          : cmd_tag(args)
        case _              : print("Bad command.")


# creating classes for adding features into our wyag , so let us start with init , which will create a repository for us .
class GitRepository(object) : 
    '''A git Repo'''
    worktree = None
    gitdir = None
    conf = None
    
    def __init__(self, path , force=False):
        self.worktree = path
        self.gitdir = os.path.join(path, ".git")
        
        if not (force or os.path.isdir(self.gitdir)):
            raise Exception(f'Not a Git Repository {path}')
        
        # read configuration file in .git/config 
        self.config = configparser.ConfigParser()
        cf = repo_file(self, "config")
        if cf and os.path.exists(cf):
            self.conf.read([cf])
        elif not force:
            raise Exception("Configuration file is missing.")
        
        if not force:
            vers = int(self.conf.get("core","repositoryformatversion"))
            if vers != 0 :
                raise Exception("Unsupported repositoryformatversion : {vers}")

