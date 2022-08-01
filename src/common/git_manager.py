# Standard Library Imports
import logging

# Third Party Library Imports
import git

# Local Library Imports

# Configure Logging
log = logging.getLogger('log')


def get_git_atts(repo_path: str) -> None:
    repo = git.Repo(repo_path)

    branch = repo.active_branch
    print(branch.name)
    origin = repo.remotes[0]
    print(type(origin))

    # method_list = [attribute for attribute in dir(repo) if callable(getattr(repo, attribute)) and attribute.startswith('__') is False]
    method_list = dir(origin)
    # You can pull from remote so lets give that a try

    for method in method_list:
        print(method)
        pass
