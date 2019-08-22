from pick import pick
from invoke import task
from rscli.utils import LANGUAGES, ensure_gitignore, check_command, RELEASES


@task()
def init(c):
    title = 'Please pick a language to init'
    language, _ = pick(LANGUAGES, title)
    ensure_gitignore(language)
    c.run('ls -a')


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
