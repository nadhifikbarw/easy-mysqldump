import os


def expand_resolve_path(path):
    return os.path.abspath(os.path.expanduser(path))