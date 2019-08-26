from pick import pick
from invoke import task
from invoke.exceptions import Exit
from rscli.version import bump_version
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
    '''Check if the working dir is clean or not.'''
    cmd = c.run('git status', hide='both')
    if cmd.stdout.strip().endswith('working tree clean'):
        logger.info('git dir is clean')
    # else:
    #     raise Exit('git dir is NOT clean', 1)


@task(pre=[is_git_dirty], help={'release': f'Bump one of {abcfp}'})
def bump(c, release='p', force_year_bump=True):
    f'''Bump versions: {abcfp}.'''
    if release not in abcfp:
        raise Exit(f'Invalid release value: {release}', 1)
    old_version, new_version = bump_version(release, force_year_bump)


@task(pre=[is_git_dirty])
def bump_build(c, force_year_bump=True):
    '''Bump build number.'''
    old_version, new_version = bump_version(build=True)


@task
def you_dont_say(c):
    '''You don't say?'''
    c.run('echo "We ❤️ Open Source! 😍"')
