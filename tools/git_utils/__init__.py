'''
git_utils
'''

import subprocess

from git import Repo, Tag

_git_dir = subprocess.getoutput("git rev-parse --show-toplevel")
__git_repo__ = Repo(_git_dir)
__git_submodule_info_cache__ = {m.name: m.hexsha for m in __git_repo__.iter_submodules()}


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

def git_submodule_set_commit(submodule_name, commit):
    '''
    git_submodule_set_commit
    '''
    repo_path = __git_repo__.submodule(submodule_name).abspath
    repo = Repo(repo_path)
    return repo.git.checkout(commit)


def git_submodule_get_commit(submodule_name):
    '''
    git_submodule_get_commit
    '''
    return __git_submodule_info_cache__.get(submodule_name, "")


def git_submodule_list():
    '''
    git_submodule_list
    '''
    return __git_submodule_info_cache__.keys()
