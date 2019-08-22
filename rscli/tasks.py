from shutil import which

import requests
from pick import pick
from invoke import task, Config

PYTHON = 'Python'
NODE = 'Node'
LANGUAGES = [PYTHON, NODE]


class TesterConfig(Config):
    prefix = 'rscli'


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


def ensure_gitignore(language):
    url = (
        'https://raw.githubusercontent.com/github/'
        'gitignore/master/%s.gitignore' % language)
    resp = requests.get(url)
    with open('.gitignore', 'w') as f:
        f.write(resp.content.decode())


@task()
def init(c):
    title = 'Please choose the framwork to init'
    language, _ = pick(LANGUAGES, title)
    ensure_gitignore(language)
    c.run('ls')


def check_command(cmd):
    cmd_path = which(cmd)
    if cmd_path is None:
        print("[ERROR] Missing Command: %s" % cmd)
    else:
        print("[INFO] Using command: %s" % cmd_path)
    return cmd_path


@task
def doctor(c):
    [check_command(command) for command in [
        'pipenv', 'django-admin', 'node', 'yarn']]


@task(help={'release': f'One of: {"/".join(RELEASES.keys)}'})
def bump(c, release=RELEASES.a):
    pass


@task
def you_dont_say(c):
    '''You don't say?'''
    c.run('echo "We ❤️ Open Source! 😍"')
