'''Utilities to bump version'''
from json import load
from datetime import datetime
from dataclasses import dataclass

from rscli.utils import abcfp


@dataclass
class Version:
    year: int
    build: int
    release: str
    release_number: int

    @classmethod
    def load(cls, kwargs):
        return cls(**kwargs)

    @property
    def version_string(self) -> str:
        v = f'{self.year}.{self.build}'
        release_str = self.release
        if release_str == 'f':
            release_str = ''
        elif release_str == 'p':
            release_str = '.post'
        if self.release_number != 0:
            v = f'{v}{release_str}'
            v = f'{v}{self.release_number}'
        return v

    def bump_build(self):
        self.build += 1
        self.release = 'a'
        self.release_number = 1
        return self.version_string

    def bump(self, release: str, force_year_bump: bool = True) -> str:
        if release not in abcfp:
            raise ValueError(f'Not a valid release: {release}!')

        year = datetime.now().year
        if force_year_bump and year != self.year:
            # Happy new year! Let's reset the build number!!
            self.year = year
            self.build = 0
            return self.bump_build()

        if release in set('abc'):
            if release == self.release:
                self.release_number += 1
            elif release > self.release:
                self.release = release
                self.release_number = 1
            else:
                raise ValueError('Can\'t Downgrade! try bump_build maybe?')

        elif release == 'f':
            if self.release in set('fp'):
                raise ValueError('Can\'t do a final release! Try bump_build?')
            else:
                self.release = release
                self.release_number = 0

        elif release == 'p':
            if self.release == 'p':
                self.release_number += 1
            else:
                self.release = release
                self.release_number = 1

        return self.version_string

    def __lt__(self, other) -> bool:
        attrs = ['year', 'build', 'release', 'release_number']
        for attr in attrs:
            self_val = getattr(self, attr)
            other_val = getattr(other, attr)
            if self_val < other_val:
                return True
            if self_val > other_val:
                return False
        return False

    def __le__(self, other) -> bool:
        return self < other or self == other

    def __gt__(self, other) -> bool:
        return not self <= other

    def __ge__(self, other) -> bool:
        return self > other or self == other


def _get_currnet_version():
    current_kwargs = load(open('.version.json'))['version']
    return Version.load(current_kwargs)


def bump_version(release):
    current_version = _get_currnet_version()
    current_version.bump(release)
    return current_version


def bump_build():
    current_version = _get_currnet_version()
    current_version.bump_build()
    return current_version
