"""
MIT License: Copyright (c) 2022 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
Full license text available in "LICENSE" file packaged with the program.
"""
from .src import options, reviewer, bottombar, deckoptions


def init():
    options.bind_actions()
    reviewer.build_hooks()
    bottombar.build_bottom_bar()
    deckoptions.build_hooks()


init()
