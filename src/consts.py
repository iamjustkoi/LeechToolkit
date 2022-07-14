"""
MIT License: Copyright (c) 2022 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
Full license text available in "LICENSE" file packaged with the program.
"""
from typing import NewType

CURRENT_VERSION = '0.0.1a'

ANKI_LEGACY_VER = 35

PosType = NewType('PosIndex', int)
DEFAULT = PosType(0)
LEFT = PosType(1)
RIGHT = PosType(2)
MARKER_POS_STYLES = {DEFAULT: 'unset', LEFT: 'left', RIGHT: 'right'}


class Config:
    TOOLBAR_ENABLED = 'Use Toolbar Options'
    SHOW_ALMOST_LEECH_MARKER = 'Show Almost Leech Marker'
    ALMOST_MARKER_POSITION = 'Marker Position'
    DEFAULT_CONFIG = {
        TOOLBAR_ENABLED: True,
        SHOW_ALMOST_LEECH_MARKER: True,
        ALMOST_MARKER_POSITION: DEFAULT
    }


class String:
    TOOLBAR_OPTIONS = '&Leech Toolkit Options...'
    pass
