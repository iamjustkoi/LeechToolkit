"""
MIT License: Copyright (c) 2022 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
Full license text available in "LICENSE" file packaged with the program.
"""
from typing import NewType

from anki import buildinfo
from aqt.utils import tr

CURRENT_VERSION = '0.5.0-beta'

ANKI_21_VERSION = int(buildinfo.version.replace('2.1.', ''))
ANKI_21_LEGACY_VER = 35

LEECH_TAG = 'leech'
LEECHES_URL = 'viewleeches'

REMOVE_ICON_PATH = '../res/img/remove_icon.svg'
RESTORE_ICON_PATH = '../res/img/restore_icon.svg'

MENU_CARDS_TEXT = tr.qt_accel_cards()

PosType = NewType('PosIndex', int)
DEFAULT = PosType(0)
LEFT = PosType(1)
RIGHT = PosType(2)
MARKER_POS_STYLES = {DEFAULT: 'unset', LEFT: 'left', RIGHT: 'right'}

ReverseType = NewType('ReverseType', int)
REV_DECREASE = ReverseType(0)
REV_RESET = ReverseType(1)


class ErrorMsg:
    ACTION_MANAGER_NOT_DEFINED = 'Action manager not yet defined.'
    TOOLKIT_MANAGER_NOT_FOUND = 'Toolkit manager not found.'


class Macro:
    DATE = '%date'
    REVIEWS = '%reviews'
    REGEX = '%re'
    MACROS = {DATE, REVIEWS, REGEX}


class String:
    LEECH_TOOLKIT_OPTIONS = '&Leech Toolkit Options...'

    RESTORE_DEFAULT_SETTING = 'Restore Default Setting'

    TOOLKIT_ACTIONS = 'Too&lkit Actions'
    ACTION_LEECH = '&Leech'
    ACTION_UNLEECH = '&Un-Leech'
    ACTION_SET_LAPSES = '&Set Lapses...'

    OUTPUT_TEXT = 'Text'
    REPLACE_WITH = 'Replace With'
    VIEW_LEECHES = 'Leech Cards'

    BUTTON_SHORTCUT_HINT = 'Shortcut key'

    LAPSES_DECREASED = r"Lapses decreased!"
    LAPSES_RESET = r"Lapses reset!"
    LEECH_REVERSED = r"Leech reversed!"

    LEECH_ACTIONS = 'Leech Actions'
    UN_LEECH_ACTIONS = 'Un-Leech Actions'

    NOTE_NOT_FOUND = 'Missing Note-Type'

    SYNC_TAG_DEFAULT = 'leech::toolkit-filtered'

    UNDO_ENTRY_SET_LAPSES = 'Set Lapses'
    UNDO_ENTRY_LEECH_ACTIONS = 'Leech Actions'
    UNDO_ENTRY_UNLEECH_ACTIONS = 'Un-leech Actions'

    TIP_LEECHED_TEMPLATE = 'Leeched {} cards'
    TIP_UNLEECHED_TEMPLATE = 'Un-leeched {} cards'
    TIP_SET_LAPSES_TEMPLATE = 'Set lapses for {} cards'


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


class QueueAction:
    CURRENT_DECK = 'currentDeck'
    SIMILAR_RATIO = 'similarityRatio'
    INCLUSIVE_FIELDS = 'shouldIncludeFields'
    FILTERED_FIELDS = 'filteredFields'
    EXCLUDED_TEXT = 'excludedText'
    NEAR_SIMILAR = 'nearSimilar'
    NEAR_SIBLING = 'nearSameNote'
    FROM_INDEX = 'fromIndex'
    FROM_VAL = 'fromValue'
    TO_INDEX = 'toIndex'
    TO_VAL = 'toValue'

    TOP = 0
    BOTTOM = 1
    POS = 2


class Action:
    ADD_TO_QUEUE = 'addToQueue'
    RESCHEDULE = 'reschedule'
    MOVE_DECK = 'moveToDeck'
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

    SYNC_ENABLED = 'applyOnSync'
    SYNC_TAG_OPTIONS = 'syncOptions'
    SYNC_TAG_ENABLED = 'syncTagEnabled'
    SYNC_TAG_TEXT = 'syncTagText'

    MARKER_OPTIONS = 'markerOptions'
    SHOW_LEECH_MARKER = 'showLeechMarker'
    USE_ALMOST_MARKER = 'showAlmostLeechMarker'
    ONLY_SHOW_BACK_MARKER = 'showMarkerOnBack'
    MARKER_POSITION = 'almostMarkPosition'

    BUTTON_OPTIONS = 'buttonOptions'
    SHOW_BUTTON = 'showBrowseButton'
    SHOW_BROWSER_BUTTON = 'showBrowseButtonOnBrowser'
    SHOW_OVERVIEW_BUTTON = 'showBrowseButtonOnOverview'

    REVERSE_OPTIONS = 'reverseOptions'
    REVERSE_ENABLED = 'enabled'
    REVERSE_METHOD = 'reverseType'
    REVERSE_USE_LEECH_THRESHOLD = 'reverseUseLeechThreshold'
    REVERSE_THRESHOLD = 'reverseThreshold'
    REVERSE_CONS_ANS = 'reverseConsecutiveAnswers'

    SET_LAPSES_INPUT = 'setLapseInput'
    SET_LAPSE_UPDATE_LEECHES = 'setLapseUpdateLeeches'

    LEECH_ACTIONS = 'leechActions'
    UN_LEECH_ACTIONS = 'unLeechActions'
    DEFAULT_ACTIONS = {
        Action.FLAG: {Action.ENABLED: False, Action.INPUT: 0},
        Action.SUSPEND: {Action.ENABLED: False, Action.INPUT: True},
        Action.ADD_TAGS: {Action.ENABLED: False, Action.INPUT: ''},
        Action.REMOVE_TAGS: {Action.ENABLED: False, Action.INPUT: ''},
        Action.FORGET: {Action.ENABLED: False, Action.INPUT: [True, True, True]},
        Action.EDIT_FIELDS: {
            Action.ENABLED: False,
            Action.INPUT: [
                # {'model-id', field_ord, method_index, 'repl', 'ref'}
            ]
        },
        Action.MOVE_DECK: {Action.ENABLED: False, Action.INPUT: ''},
        Action.RESCHEDULE: {
            Action.ENABLED: False,
            Action.INPUT: {
                RescheduleAction.FROM: 0,
                RescheduleAction.TO: 7,
                RescheduleAction.RESET: True,
            }
        },
        Action.ADD_TO_QUEUE: {
            Action.ENABLED: False,
            Action.INPUT: {
                QueueAction.CURRENT_DECK: True,
                QueueAction.FROM_INDEX: 0,
                QueueAction.FROM_VAL: 0,
                QueueAction.TO_INDEX: 0,
                QueueAction.TO_VAL: 0,
                QueueAction.NEAR_SIBLING: False,
                QueueAction.NEAR_SIMILAR: False,
                QueueAction.SIMILAR_RATIO: 0.25,
                QueueAction.INCLUSIVE_FIELDS: True,
                QueueAction.FILTERED_FIELDS: [
                    # {'model-id': field_ord},
                ],
                QueueAction.EXCLUDED_TEXT: '\\ ( ) ` \' " ; : . \\, ? ! & [ ] { } \\s'
            }
        }
    }

    DECK_CATEGORIES = [
        REVERSE_OPTIONS,
        LEECH_ACTIONS,
        UN_LEECH_ACTIONS,
    ]

    DEFAULT_CONFIG = {
        TOOLBAR_ENABLED: True,
        SYNC_ENABLED: False,
        SYNC_TAG_OPTIONS: {
            SYNC_TAG_ENABLED: True,
            SYNC_TAG_TEXT: String.SYNC_TAG_DEFAULT,
        },
        MARKER_OPTIONS: {
            SHOW_LEECH_MARKER: True,
            USE_ALMOST_MARKER: True,
            ONLY_SHOW_BACK_MARKER: True,
            MARKER_POSITION: DEFAULT,
        },
        BUTTON_OPTIONS: {
            SHOW_BUTTON: True,
            SHOW_BROWSER_BUTTON: True,
            SHOW_OVERVIEW_BUTTON: True,
        },
        REVERSE_OPTIONS: {
            REVERSE_ENABLED: True,
            REVERSE_USE_LEECH_THRESHOLD: True,
            REVERSE_THRESHOLD: 4,
            REVERSE_CONS_ANS: 2,
            REVERSE_METHOD: 0
        },
        LEECH_ACTIONS: DEFAULT_ACTIONS,
        UN_LEECH_ACTIONS: DEFAULT_ACTIONS
    }
