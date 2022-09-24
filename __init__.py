"""
MIT License: Copyright (c) 2022 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
Full license text available in "LICENSE" file packaged with the program.
"""
from .src import options, reviewer, bottombar, deckoptions, sync, browser

options.bind_actions()
reviewer.build_hooks()
bottombar.build_bottom_bar()
deckoptions.build_hooks()
sync.build_hooks()
browser.build_hooks()
