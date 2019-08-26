from sys import exit
from pick import pick
from invoke import task
from rscli.version import bump_version, bump_build as _bump_build
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
    version = bump_version(release)
    print(version)
    __import__('ipdb').set_trace()


@task
def bump_build(c):
    '''Bump build number'''
    version = _bump_build()
    print(version)


@task
def you_dont_say(c):
    '''You don't say?'''
    c.run('echo "We ❤️ Open Source! 😍"')
