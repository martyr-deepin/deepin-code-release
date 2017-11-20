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
            raise SubmoduleError("This git repository doesn't have this submodule: %s" % (self.name))
        return sbm

    @property
    def submodules(self):
        if getattr(self, "_sbms", None):
            return self._sbms
        self._sbms = super().submodules
        if not self._sbms:
            raise SubmoduleError("This git repository doesn't have any submodule: %s" %s (self.name))
        return self._sbms

    @property
    def tags(self):
        tags = super().tags
        if not tags:
            return None
        return tags

    def get_submodule(self, name):
        sbms = self.get_submodules((name,))
        return sbms[0] if len(sbms) else None


    def get_submodules(self, names):
        sbms = []
        for name in names:
            sbm = self.submodule(name)
            repo = RepoManager(sbm.abspath)
            repo.name = sbm.name
            sbms.append(repo)
        return sbms

    def get_all_submodules(self):
        return self.get_submodules(self.submodule_list)

    @property
    def submodule_list(self):
        return [m.name for m in self.submodules]

    @property
    def latest_commit(self):
        return self.commit().hexsha

    @property
    def latest_origin_commit(self):
        return self.git.log("origin/master", "-1", "--pretty=oneline").split()[0]

    @property
    def latest_tag(self):
        return max(self.tags, key=lambda t: t.commit.committed_datetime) if self.tags else None

    def commit_to_tag(self, commit_hash):
        if self.tags:
            for tag in self.tags:
                if commit_hash == tag.commit.hexsha:
                    return tag
        raise TagError("This commit %s of repo %s can't convert into tag" % (commit_hash, self.name))

    def set_commit(self, commit_hash):
        return self.git.checkout(commit_hash)
