from shutil import which

import requests
# from pick import pick
from invoke import task

DJANGO = 'django'
ANGULAR = 'angular'
FRAMEWORKS = [DJANGO, ANGULAR]


def ensure_gitignore(language):
    url = (
        'https://raw.githubusercontent.com/github/'
        'gitignore/master/%s.gitignore' % language)
    resp = requests.get(url)
    with open('.gitignore', 'w') as f:
        f.write(resp.content.decode())


@task
def init_django(c):
    ensure_gitignore('Python')
    c.run('ls')


@task
def init_angular(c):
    ensure_gitignore('Node')


init_map = {}
for framwork in FRAMEWORKS:
    init_map[framwork] = globals()["init_%s" % framwork]


'''
@cli.command()
@click.pass_context
@click.option('--name', prompt='Please enter a name for your project')
@click.option('--description', prompt='Please describe your project')
@click.option('--domain', prompt='Please enter a domain to host in')
def init(ctx, name, description, domain):
    title = 'Please choose the framwork to init'
    framwork, _ = pick(FRAMEWORKS, title)
    ctx.invoke(init_map[framwork])
'''


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
