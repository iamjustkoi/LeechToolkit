"""
MIT License: Copyright (c) 2022 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
Full license text available in "LICENSE" file packaged with the program.
"""
import os.path

from .src import options, reviewer, bottombar, deckoptions, sync, browser
from .src.consts import MARKER_HTML_TEMP, ROOT_DIR

options.bind_actions()
reviewer.build_hooks()
bottombar.build_bottom_bar()
deckoptions.build_hooks()
sync.build_hooks()
browser.build_hooks()

if not os.path.isfile(f'{ROOT_DIR}\\marker_html.html'):
    with open(f'{ROOT_DIR}\\marker_html.html', 'w') as f:
        f.write(MARKER_HTML_TEMP)
