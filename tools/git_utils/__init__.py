from git import Repo

from .error import SubmoduleError, TagError

__all__ = ["repo", "RepoManager", "SubmoduleError", "TagError"]


class RepoManager(Repo):

    def __init__(self, path):
        super().__init__(path, search_parent_directories=True)

    def submodule(self, name):
        try:
            sbm = super().submodule(name)
        except ValueError:
            raise SubmoduleError("This git repository doesn't have this submodule")
        return sbm

    @property
    def submodules(self):
        if getattr(self, "_sbms", None):
            return self._sbms
        self._sbms = super().submodules
        if not self._sbms:
            raise SubmoduleError("This git repository doesn't have any submodule")
        return self._sbms

    @property
    def tags(self):
        tags = super().tags
        if not tags:
            raise TagError("This git repository doesn't have any tag")
        return tags

    def get_submodule(self, name):
        repo = RepoManager(self.submodule(name).abspath)
        repo.name = name
        return repo

    def get_all_submodules(self):
        sbms = []
        for sbm in self.submodules:
            repo = RepoManager(sbm.abspath)
            repo.name = sbm.name
            sbms.append(repo)
        return sbms

    @property
    def submodule_list(self):
        return [m.name for m in self.submodules]

    @property
    def latest_commit(self):
        return self.commit().hexsha

    @property
    def latest_origin_commit(self):
        return self.git.log("origin", "-1", "--pretty=oneline").split()[0]

    @property
    def latest_tag(self):
        return max(self.tags, key=lambda t: t.commit.committed_datetime)

    def commit_to_tag(self, commit_hash):
        for tag in self.tags:
            if commit_hash == tag.commit.hexsha:
                return tag
        raise TagError("This commit can't convert into tag")

    def set_commit(self, commit_hash):
        return self.git.checkout(commit_hash)
