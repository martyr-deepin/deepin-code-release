'''
git_utils
'''

import os
import subprocess
from functools import update_wrapper

from git import Repo, Tag, Submodule

__git_repo__ = None
__git_submodule_info_cache__ = {}

def check_repo():
    '''
    check_repo
    '''
    global __git_repo__

    if not __git_repo__:
        git_dir = subprocess.getoutput("git rev-parse --show-toplevel")
        __git_repo__ = Repo(git_dir)

def ensure_repo(func):
    '''
    ensure_repo
    '''
    def ret(*args, **kwrds):
        '''
        wrapper
        '''
        check_repo()
        return func(*args, **kwrds)
    update_wrapper(ret, func)
    return ret

def ensure_submodule_info_cache(func):
    '''
    ensure_submodule_info_cache
    '''
    check_repo()
    repo = __git_repo__

    def ret(*args, **kwrds):
        '''
        wrapper
        '''
        if len(__git_submodule_info_cache__) == 0:
            mods = Submodule.iter_items(repo)
            for mod in mods:
                __git_submodule_info_cache__[mod.name] = mod.hexsha

        return func(*args, **kwrds)

    update_wrapper(ret, func)
    return ret

def git_commit_to_tag(repo_dir, commit_name):
    '''
    git_commit_to_tag
    '''
    repo = Repo(repo_dir)
    tags = Tag.list_items(repo)
    for tag in tags:
        if tag.commit.hexsha == commit_name:
            return tag.name
    return ""

def git_origin_commit(repo_dir):
    '''
    git_origin_commit
    '''
    repo = Repo(repo_dir)
    git = repo.git
    return git.log("origin", "-1", "--pretty=oneline").split()[0]

def git_origin_tag(repo_dir):
    '''
    git_origin_tag
    '''
    repo = Repo(repo_dir)
    tags = repo.tags.copy()
    tags.sort(key=lambda x: x.commit.committed_datetime)
    return tags[-1].name if len(repo.tags) else ""

def git_submodule_commit_to_tag(submodule_name, commit_name):
    '''
    git_submodule_commit_to_tag
    '''
    repo_path = __git_repo__.submodule(submodule_name).abspath
    return git_commit_to_tag(repo_path, commit_name)

def git_submodule_latest_commit(submodule_name):
    '''
    git_submodule_latest_commit
    '''
    repo_path = __git_repo__.submodule(submodule_name).abspath
    return git_origin_commit(repo_path)

def git_submodule_latest_tag(submodule_name):
    '''
    git_submodule_latest_tag
    '''
    repo_path = __git_repo__.submodule(submodule_name).abspath
    return git_origin_tag(repo_path)

@ensure_submodule_info_cache
def git_submodule_get_commit(submodule_name):
    '''
    git_submodule_get_commit
    '''
    return __git_submodule_info_cache__.get(submodule_name, "")

@ensure_submodule_info_cache
def git_submodule_list():
    '''
    git_submodule_list
    '''
    return __git_submodule_info_cache__.keys()
