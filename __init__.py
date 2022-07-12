"""
MIT License: Copyright (c) 2022 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
Full license text available in "LICENSE" file packaged with the program.
"""
from .src import options, reviewer


def init():
    options.bind_actions()
    reviewer.build_hooks()
    pass


init()
