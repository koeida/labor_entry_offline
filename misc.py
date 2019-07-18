import os

def get_dirs(path):
    dirs = []
    with os.scandir(path) as it:
        dirs = filter(lambda i: i.is_dir(), it)
        dirs = map(lambda i: i.name, dirs)
        dirs = list(dirs)
    return dirs

def get_most_recent_week(path):
    dirs = []
    with os.scandir(path) as it:
        dirs = filter(lambda i: i.is_dir(), it)
        dirs = map(lambda i: (i.stat().st_ctime, i.name), dirs)
        dirs = list(dirs)
    dirs.sort(key=lambda d: d[0])
    return dirs[-1][1]

def valid_type(type_func, v):
    try:
        type_func(v)
        return True
    except:
        return False
