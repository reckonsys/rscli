from shutil import which

import click
import requests
from pick import pick

DJANGO = 'django'
ANGULAR = 'angular'
FRAMEWORKS = [DJANGO, ANGULAR]


@click.group()
@click.pass_context
def cli(ctx):
    '''
    Reckonsys CLI Toolchain
    '''
    ctx.ensure_object(dict)


def ensure_gitignore(language):
    url = (
        'https://raw.githubusercontent.com/github/'
        'gitignore/master/%s.gitignore' % language)
    resp = requests.get(url)
    with open('.gitignore', 'w') as f:
        f.write(resp.content.decode())


@cli.command()
def init_django():
    ensure_gitignore('Python')


@cli.command()
def init_angular():
    ensure_gitignore('Node')


init_map = {}
for framwork in FRAMEWORKS:
    init_map[framwork] = globals()["init_%s" % framwork]


@cli.command()
@click.pass_context
@click.option('--name', prompt='Please enter a name for your project')
@click.option('--description', prompt='Please describe your project')
@click.option('--domain', prompt='Please enter a domain to host in')
def init(ctx, name, description, domain):
    '''
    Init
    '''
    title = 'Please choose the framwork to init'
    framwork, _ = pick(FRAMEWORKS, title)
    ctx.invoke(init_map[framwork])


def check_command(cmd):
    cmd_path = which(cmd)
    if cmd_path is None:
        print("[ERROR] Missing Command: %s" % cmd)
    else:
        print("[INFO] Using command: %s" % cmd_path)
    return cmd_path


@cli.command()
@click.pass_context
def doctor(ctx):
    [check_command(command) for command in [
        'pipenv', 'django-admin', 'node', 'yarn']]
