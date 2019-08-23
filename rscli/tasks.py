from sys import exit
from pick import pick
from invoke import task
from rscli.version import compute_version
from rscli.utils import (
    LANGUAGES, logger, ensure_gitignore, check_command, abcfp)


@task()
def init(c):
    title = 'Please pick a language to init'
    language, _ = pick(LANGUAGES, title)
    ensure_gitignore(language)
    c.run('ls -a')


@task
def doctor(c):
    [check_command(command) for command in ['pipenv', 'node', 'yarn', 'git']]


@task(help={'release': f'Bump one of {abcfp}'})
def bump(c, release='p'):
    f'''Bump versions: {abcfp}'''
    if release not in abcfp:
        logger.error(f'Invalid release value: {release}')
        exit(1)
    last_version, next_version = compute_version(release)


@task
def you_dont_say(c):
    '''You don't say?'''
    c.run('echo "We ❤️ Open Source! 😍"')
