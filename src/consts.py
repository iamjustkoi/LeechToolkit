"""
MIT License: Copyright (c) 2022 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
Full license text available in "LICENSE" file packaged with the program.
"""
from typing import NewType

CURRENT_VERSION = '0.3.0-beta'

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
    OUTPUT_TEXT = 'Text'
    REPLACE_WITH = 'Replace With'
    TOOLBAR_OPTIONS = '&Leech Toolkit Options...'
    VIEW_LEECHES = 'Leech Cards'
    BUTTON_SHORTCUT_HINT = 'Shortcut key'
    LAPSES_DECREASED = r"Lapses decreased!"
    LAPSES_RESET = r"Lapses reset!"
    LEECH_REVERSED = r"Leech reversed!"

    LEECHES_URL = 'viewleeches'


class EditAction:
    FIELD = 'field'
    METHOD = 'method'
    REPL = 'repl'
    TEXT = 'text'
    EditMethod = NewType('EditMethod', int)
    APPEND_METHOD = EditMethod(0)
    PREPEND_METHOD = EditMethod(1)
    REPLACE_METHOD = EditMethod(2)
    REGEX_METHOD = EditMethod(3)


class RescheduleAction:
    FROM = 'from'
    TO = 'to'
    RESET = 'resetInterval'


class Action:
    ADD_TO_QUEUE = 'addToQueue'
    RESCHEDULE = 'reschedule'
    MOVE_TO_DECK = 'moveToDeck'
    EDIT_FIELDS = 'editFields'
    FORGET = 'forget'
    DISABLE_DEFAULT = 'disableDefault'
    FLAG = 'flag'
    SUSPEND = 'suspend'
    ADD_TAGS = 'addTags'
    REMOVE_TAGS = 'removeTags'

    ENABLED = 'enabled'
    INPUT = 'input'


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
    REVERSE_USE_LEECH_THRESHOLD = 'reverseUseLeechThreshold'
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
        REVERSE_USE_LEECH_THRESHOLD: True,
        REVERSE_THRESHOLD: 4,
        REVERSE_CONS_ANS: 2,
        REVERSE_METHOD: 0,
        LEECH_ACTIONS: {
            Action.FLAG: {Action.ENABLED: False, Action.INPUT: 0},
            Action.SUSPEND: {Action.ENABLED: False, Action.INPUT: True},
            Action.ADD_TAGS: {Action.ENABLED: False, Action.INPUT: 'leech_update'},
            Action.REMOVE_TAGS: {Action.ENABLED: False, Action.INPUT: ''},
            Action.FORGET: {Action.ENABLED: False, Action.INPUT: [True, True, True]},
            Action.EDIT_FIELDS: {
                Action.ENABLED: False,
                Action.INPUT: {}
            },
            Action.MOVE_TO_DECK: {Action.ENABLED: False, Action.INPUT: ''},
            Action.RESCHEDULE: {
                Action.ENABLED: False,
                Action.INPUT: {
                    RescheduleAction.FROM: 0,
                    RescheduleAction.TO: 7,
                    RescheduleAction.RESET: True,
                }
            },
        }
    }
