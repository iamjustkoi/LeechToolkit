"""
MIT License: Copyright (c) 2022 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
Full license text available in "LICENSE" file packaged with the program.
"""
from typing import NewType

CURRENT_VERSION = '0.2.0-beta'

ANKI_LEGACY_VER = 35

PosType = NewType('PosIndex', int)
DEFAULT = PosType(0)
LEFT = PosType(1)
RIGHT = PosType(2)
MARKER_POS_STYLES = {DEFAULT: 'unset', LEFT: 'left', RIGHT: 'right'}

ReverseType = NewType('ReverseType', int)
REV_DECREASE = ReverseType(0)
REV_RESET = ReverseType(1)

CARD_TYPE_STR = {0: 'new', 1: 'learn', 2: 'review', 3: 'relearn'}

LEECH_TAG = 'leech'

REMOVE_ICON_PATH = '../res/img/remove_icon.svg'


class Macro:
    DATE = '%date'
    REVIEWS = '%reviews'
    REGEX = '%re'
    MACROS = {DATE, REVIEWS, REGEX}


class String:
    TOOLBAR_OPTIONS = '&Leech Toolkit Options...'
    VIEW_LEECHES = 'Leech Cards'
    BUTTON_SHORTCUT_HINT = 'Shortcut key'
    LAPSES_DECREASED = r"Card's lapses decreased"
    LAPSES_RESET = r"Card's lapses reset"

    LEECHES_URL = 'viewleeches'


class Action:
    EDIT_FIELDS = 'editFields'

    class Fields:
        FIELD = 'field'
        METHOD = 'method'
        REPL = 'repl'
        TEXT = 'text'
        EditType = NewType('EditType', int)
        EDIT_APPEND = EditType(0)
        EDIT_PREPEND = EditType(1)
        EDIT_REPLACE = EditType(2)
        EDIT_REGEX = EditType(3)

    FORGET = 'forget'
    DISABLE_DEFAULT = 'disableDefault'
    FLAG = 'flag'
    SUSPEND = 'suspend'
    ADD_TAGS = 'addTags'
    REMOVE_TAGS = 'removeTags'

    ENABLED = 'enabled'
    INPUT = 'input'
    EXTRA = 'extra'


class Config:
    TOOLBAR_ENABLED = 'showToolsMenuOptions'

    SHOW_LEECH_MARKER = 'showLeechMarker'
    USE_ALMOST_MARKER = 'showAlmostLeechMarker'
    ONLY_SHOW_BACK_MARKER = 'showMarkerOnBack'
    MARKER_POSITION = 'almostMarkPosition'

    SHOW_BROWSE_BUTTON = 'showBrowseButton'
    BROWSE_BUTTON_ON_BROWSER = 'showBrowseButtonOnBrowser'
    BROWSE_BUTTON_ON_OVERVIEW = 'showBrowseButtonOnOverview'

    REVERSE_ENABLED = 'reverseEnabled'
    REVERSE_METHOD = 'reverseType'
    REVERSE_THRESHOLD = 'reverseThreshold'
    REVERSE_CONS_ANS = 'reverseConsecutiveAnswers'

    LEECH_ACTIONS = 'leechActions'

    DEFAULT_CONFIG = {
        TOOLBAR_ENABLED: True,
        SHOW_LEECH_MARKER: True,
        USE_ALMOST_MARKER: True,
        ONLY_SHOW_BACK_MARKER: True,
        MARKER_POSITION: DEFAULT,
        SHOW_BROWSE_BUTTON: True,
        BROWSE_BUTTON_ON_BROWSER: True,
        BROWSE_BUTTON_ON_OVERVIEW: True,
        REVERSE_ENABLED: True,
        REVERSE_THRESHOLD: 4,
        REVERSE_CONS_ANS: 2,
        REVERSE_METHOD: 0,
        LEECH_ACTIONS: {
            Action.FLAG: {Action.ENABLED: False, Action.INPUT: 0},
            Action.SUSPEND: {Action.ENABLED: False, Action.INPUT: True},
            Action.ADD_TAGS: {Action.ENABLED: False, Action.INPUT: 'leech'},
            Action.REMOVE_TAGS: {Action.ENABLED: False, Action.INPUT: ''},
            Action.FORGET: {Action.ENABLED: False, Action.INPUT: [True, True, True]},
            Action.EDIT_FIELDS: {
                Action.ENABLED: False,
                Action.INPUT: {
                    # Action.Fields.NOTE_ID: {
                    #     Action.Fields.FIELD: 0,
                    #     Action.Fields.METHOD: 0,
                    #     Action.Fields.FIND: 'repl',
                    #     Action.Fields.TEXT: 'input'
                    # }
                }
            }
        }
    }
