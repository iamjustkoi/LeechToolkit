"""
MIT License: Copyright (c) 2022 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
Full license text available in "LICENSE" file packaged with the program.
"""
from typing import NewType

CURRENT_VERSION = '0.0.3-alpha'

ANKI_LEGACY_VER = 35

PosType = NewType('PosIndex', int)
DEFAULT = PosType(0)
LEFT = PosType(1)
RIGHT = PosType(2)
MARKER_POS_STYLES = {DEFAULT: 'unset', LEFT: 'left', RIGHT: 'right'}
LEECHES_URL = 'viewleeches'


class Config:
    SHOW_BROWSE_BUTTON = 'show browse button'
    TOOLBAR_ENABLED = 'show tools menu options'
    SHOW_ALMOST_LEECH_MARKER = 'show almost leech marker'
    ALMOST_ON_BACK = 'show almost marker on back'
    ALMOST_MARK_POSITION = 'almost mark position'
    BROWSE_BUTTON_ON_BROWSER = 'show browse button on browser'
    BROWSE_BUTTON_ON_OVERVIEW = 'show browse button on overview'
    DEFAULT_CONFIG = {
        TOOLBAR_ENABLED: True,
        SHOW_ALMOST_LEECH_MARKER: True,
        ALMOST_ON_BACK: True,
        SHOW_BROWSE_BUTTON: True,
        ALMOST_MARK_POSITION: DEFAULT,
        BROWSE_BUTTON_ON_BROWSER: True,
        BROWSE_BUTTON_ON_OVERVIEW: True
    }


class String:
    TOOLBAR_OPTIONS = '&Leech Toolkit Options...'
    VIEW_LEECHES = 'Leech Cards'
    SHORTCUT_KEY = 'Shortcut key'
    pass
