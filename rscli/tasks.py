from sys import exit
from pick import pick
from invoke import task
from invoke.exceptions import Exit
from rscli.version import bump_version, bump_build as _bump_build
from rscli.utils import (
    LANGUAGES, logger, ensure_gitignore, check_command, abcfp)


@task
def init(c):
    '''Inititalize.'''
    title = 'Please pick a language to init'
    language, _ = pick(LANGUAGES, title)
    ensure_gitignore(language)
    c.run('ls -a')


@task
def doctor(c):
    [check_command(command) for command in ['pipenv', 'node', 'yarn', 'git']]


@task
def is_git_dirty(c):
    '''Check if the working dir is clean of not'''
    cmd = c.run('git status', hide='both')
    if cmd.stdout.strip().endswith('working tree clean'):
        print('git dir is clean')
    else:
        raise Exit('git dir is NOT clean', 1)


@task(pre=[is_git_dirty], help={'release': f'Bump one of {abcfp}'})
def bump(c, release='p', force_year_bump=True):
    f'''Bump versions: {abcfp}'''
    if release not in abcfp:
        logger.error(f'Invalid release value: {release}')
        exit(1)
    version = bump_version(release, force_year_bump)
    print(version)
    __import__('ipdb').set_trace()


@task(pre=[is_git_dirty])
def bump_build(c):
    '''Bump build number'''
    version = _bump_build()
    print(version)


@task
def you_dont_say(c):
    '''You don't say?'''
    c.run('echo "We ❤️ Open Source! 😍"')
