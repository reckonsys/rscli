import requests
from shutil import which

PYTHON = 'Python'
NODE = 'Node'

LANGUAGES = [PYTHON, NODE]


def ensure_gitignore(language):
    resp = requests.get(
        'https://raw.githubusercontent.com/github/'
        'gitignore/master/%s.gitignore' % language)
    with open('.gitignore', 'w') as f:
        f.write(resp.content.decode())


def check_command(cmd):
    cmd_path = which(cmd)
    if cmd_path is None:
        print("[ERROR] Missing Command: %s" % cmd)
    else:
        print("[INFO] Using command: %s" % cmd_path)
    return cmd_path


class Dict2Obj:
    """Convert a dict of object.

    constraint: kwargs can't contain `keys` and `values`."""

    def __init__(self, **kwargs):
        self.keys = []
        self.values = []
        for key, value in kwargs.items():
            self.keys.append(key)
            self.values.append(key)
            setattr(self, key, value)
        super(Dict2Obj, self).__init__()


RELEASES = Dict2Obj(
    a='alpha', b='beta', c='candidate-release', f='final', p='post'
)
