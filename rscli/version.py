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

    def bump(self, release: str) -> str:
        if release not in abcfp:
            raise ValueError(f'Not a valid release: {release}!')
        year = datetime.now().year
        if year != self.year:
            # Happy new year! Let's reset the build number!!
            self.year = year
            self.build = 1
            self.release = 'a'
            self.release_number = 1
            return self.version_string
        if release in set('abc'):
            if release == self.release:
                self.release_number += 1
            elif release > self.release:
                self.release = release
                self.release_number = 1
            else:
                self.build += 1
                self.release = release
                self.release_number = 1
        elif release == 'p':
            if self.release == 'p':
                self.release_number += 1
            else:
                self.release = release
                self.release_number = 1
        elif release == 'f':
            if self.release in set('fp'):
                raise ValueError('Cannot do a final release!!!')
            else:
                self.release = release
                self.release_number = 0
        return self.version_string

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


def compute_version(release):
    last_kwargs = load(open('.version.json'))['version']
    last_version = Version.load(last_kwargs)
    __import__('ipdb').set_trace()
    if release is None:
        release = ''
        # No release given. Attempting to identity a release
        if last_version.post:
            # If the last version was a post release, just
            last_version.post_number += 1
        elif last_version.release:
            pass
    __import__('ipdb').set_trace()
