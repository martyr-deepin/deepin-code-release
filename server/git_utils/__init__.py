'''
git_utils
'''

import subprocess

from git import Repo, Tag

from errors import GitException

_git_dir = subprocess.getoutput("git rev-parse --show-toplevel")
__git_repo__ = Repo(_git_dir)
__git_submodule_info_cache__ = {m.name: m.hexsha for m in __git_repo__.iter_submodules()}


def git_checkout_branch(branch_name):
    '''
    checkout branch
    '''
    repo = __git_repo__
    if branch_name not in repo.branches:
        raise GitException("branch doesn't exist")
    cmd = repo.git
    try:
        cmd.checkout(branch_name)
    except:
        raise

def git_prepare_submodules():
    '''
    git_prepare_submodules
    '''
    repo = __git_repo__

    cmd = repo.git
    cmd.submodule("update", "--init")
    cmd.pull("--recurse-submodules")

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
    repo = Repo(repo_path)
    tags = repo.tags
    tags.sort(key=lambda x: x.commit.committed_datetime)
    return tags[-1].name if len(repo.tags) else ""

def git_submodule_commit_minus_tag(submodule_name, commit, tag):
    '''
    git_submodule_latest_tag
    '''
    repo_path = __git_repo__.submodule(submodule_name).abspath
    cmd = Repo(repo_path).git
    lines = cmd.log("--pretty=oneline", "%s..%s" % (tag, commit)).splitlines()
    return len(lines)

def git_submodule_get_commit(submodule_name):
    '''
    git_submodule_get_commit
    '''
    return __git_submodule_info_cache__.get(submodule_name, "")

def git_submodule_set_commit(submodule_name, commit):
    '''
    git_submodule_set_commit
    '''
    repo_path = __git_repo__.submodule(submodule_name).abspath
    cmd = Repo(repo_path).git
    cmd.checkout(commit)

def git_submodule_list():
    '''
    git_submodule_list
    '''
    return __git_submodule_info_cache__.keys()

def git_create_update_changelines(submodule_name, commit):
    '''
    git_create_update_changelines
    '''
    repo = __git_repo__
    cmd = repo.git
    cmd.checkout("-b", "update_%s_to_%s" % (submodule_name, commit))
    git_submodule_set_commit(submodule_name, commit)
    cmd.add("--all")
    cmd.commit("-m", "update %s release version to %s" % (submodule_name, commit))
    cmd.review("panda/current")
