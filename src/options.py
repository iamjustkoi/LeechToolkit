"""
MIT License: Copyright (c) 2022 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
Full license text available in "LICENSE" file packaged with the program.
"""
import traceback
import webbrowser
from pathlib import Path
from typing import List

import anki.decks
import markdown
from anki.consts import CARD_TYPE_NEW
from .consts import CURRENT_QT_VER, MARKER_HTML_TEMP, ROOT_DIR
from aqt import mw
from aqt.qt import (
    Qt,
    QLabel,
    QKeyEvent,
    QVBoxLayout,
    QAction,
    QDialog,
    QIcon,
    QToolButton,
    QPushButton,
    QDialogButtonBox,
    QPixmap,
    QColor,
    QWidget,
    QMenu,
    QListWidgetItem,
    QListWidget,
    QGraphicsOpacityEffect,
    QTextEdit,
    QSizePolicy,
    QSize,
    pyqtBoundSignal,
    QGridLayout,
    QBoxLayout,
    QFontMetrics,
    QT_VERSION_STR,
)

# AlignHCenter | AlignVCenter
if CURRENT_QT_VER == 6:
    AutoText = Qt.TextFormat.AutoText
    AlignHCenter, AlignVCenter = Qt.AlignmentFlag.AlignHCenter, Qt.AlignmentFlag.AlignVCenter
    AlignRight, AlignBottom = Qt.AlignmentFlag.AlignRight, Qt.AlignmentFlag.AlignBottom
    arrow_types = [Qt.ArrowType.RightArrow, Qt.ArrowType.DownArrow]

    Qt.MaskOutColor = Qt.MaskMode(1)
    Qt.TextBrowserInteraction = Qt.TextInteractionFlag.TextBrowserInteraction
    Qt.NoItemFlags = Qt.ItemFlag.NoItemFlags
    QDialogButtonBox.Apply = QDialogButtonBox.StandardButton.Apply
    QDialogButtonBox.RestoreDefaults = QDialogButtonBox.StandardButton.RestoreDefaults
    QSizePolicy.Fixed = QSizePolicy.Policy.Fixed
else:
    # noinspection PyUnresolvedReferences
    AutoText = Qt.AutoText
    # noinspection PyUnresolvedReferences
    arrow_types = [Qt.RightArrow, Qt.DownArrow]
    # noinspection PyUnresolvedReferences
    AlignHCenter, AlignVCenter = Qt.AlignHCenter, Qt.AlignVCenter
    # noinspection PyUnresolvedReferences
    AlignRight, AlignBottom = Qt.AlignRight, Qt.AlignBottom

from .config import LeechToolkitConfigManager
from .consts import (
    ANKI_LEGACY_VER,
    ANKI_LIKE_ICON_PATH, ANKI_UNDO_UPDATE_VER,
    ANKI_URL, CURRENT_ANKI_VER,
    CURRENT_VERSION, ErrorMsg,
    KOFI_ICON_PATH,
    KOFI_URL,
    Keys,
    LEECH_ICON_PATH,
    LEGACY_FLAGS_PLACEHOLDER,
    PATREON_ICON_PATH,
    PATREON_URL,
    QT5_MARKDOWN_VER, String,
    Config,
    Action,
    Macro,
    REMOVE_ICON_PATH,
    EditAction,
    RescheduleAction,
    QueueAction,
    RESTORE_ICON_PATH,
)

from .sync import sync_collection
from ..res.ui.actions_form import Ui_ActionsForm
from ..res.ui.edit_field_item import Ui_EditFieldItem
from ..res.ui.exclude_field_item import Ui_ExcludedFieldItem
from ..res.ui.forms import CustomCompleter
from ..res.ui.options_dialog import Ui_OptionsDialog
from ..res.ui.reverse_form import Ui_ReverseForm

try:
    import aqt.flags
    from anki.collection import OpChanges
    from anki.models import NotetypeId
    from anki.notes import NoteId
except ModuleNotFoundError:
    print(f'{traceback.format_exc()}\n{ErrorMsg.MODULE_NOT_FOUND_LEGACY}')


class DeckNameId:
    def __init__(self, name, did):
        self.name = name
        self.id = did


def legacy_name_id_handler(*args):
    return [DeckNameId(deck["name"], deck["id"]) for deck in mw.col.decks.all()]


max_fields_height = 572
max_queue_height = 256
button_attr = 'button'


def bind_actions():
    """
    Binds option-related function to Anki.
    """
    _bind_config_options()
    _bind_tools_options()


def on_options_called(*args):
    """
    Show options dialog and pause main UI thread using an exec call to prevent reloading the options while editing them.

    :param args: unused arguments parameter
    """
    options = OptionsDialog(LeechToolkitConfigManager(mw))
    options.exec()


def append_restore_button(parent: QWidget, insert_col=4):
    """
    Appends a stylized, default restoration button to a parent QWidget using the widgets position and parent layout.

    :param parent: parent QWidget that will have the button added to its own class attributes
    :param insert_col: optional column to place the button into if the provided parent's surrounding layout supports it
    :return: the newly appended restore button
    """
    if not hasattr(parent, button_attr):
        parent.default_button = QPushButton(parent)

        parent.default_button.setMaximumSize(QSize(16, 16))
        parent.default_button.setFlat(True)
        parent.default_button.setToolTip(String.RESTORE_DEFAULT_SETTING)

        pixmap = QPixmap(f'{Path(__file__).parent.resolve()}\\{RESTORE_ICON_PATH}')
        mask = pixmap.createMaskFromColor(QColor('black'), Qt.MaskOutColor)
        # pixmap.fill(QColor('#adadad' if mw.pm.night_mode() else '#1a1a1a'))
        pixmap.fill(QColor('#adadad'))
        pixmap.setMask(mask)
        parent.default_button.setIcon(QIcon(pixmap))

        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(parent.default_button.sizePolicy().hasHeightForWidth())

        parent.default_button.setSizePolicy(size_policy)
        parent.default_button.setContentsMargins(0, 0, 0, 0)

        parent.default_button.setAutoFillBackground(False)

        layout = parent.parent().layout()
        pos = layout.indexOf(parent) + 1

        if layout is not None:
            if isinstance(layout, QGridLayout):
                if CURRENT_QT_VER == 5:
                    # noinspection PyTypeChecker
                    layout.addItem(parent.default_button, pos, insert_col)
                else:
                    layout.addItem(parent.default_button.layout(), pos, insert_col)

            elif isinstance(layout, QBoxLayout) or isinstance(layout, QVBoxLayout):
                layout.insertWidget(pos, parent.default_button, alignment=AlignRight | AlignBottom)
            else:
                layout.addWidget(parent.default_button)

            layout.insertSpacing(pos - 1, 6)

    return parent.default_button


def setup_restore_button(
    button: QPushButton,
    signals: List[pyqtBoundSignal],
    write_callback,
    load_callback,
    scoped_conf: dict = None,
    default_scoped_conf: dict = None,
    str_callback=None,
    default_str: str = None,
):
    """
    Fills and applies action and signal updates to restore buttons.

    :param button: referenced, restore QPushbutton
    :param signals: signals connect visual and config updates to the button with
    :param write_callback: function used to write config data to the button to recognize differences between the held
    default and its respective changes
    :param load_callback: function to read config data to when applying default config data from the button
    :param scoped_conf: config meta that holds a set of data to read/write to
    :param default_scoped_conf: default config meta with the same scope as the scoped config parameter
    :param str_callback: [Optional] string getter function to retrieve an updated string holder
    :param default_str: [Optional] string to use as a default comparable base instead of a dict
    """
    default_copy = default_scoped_conf.copy() if default_scoped_conf else None

    for signal in signals:
        def refresh_button_visibility(*args):
            """
            Intercept function for the created button. Refreshes the button's visibility after running the input
            write-callback.
            """
            if scoped_conf:
                write_callback(scoped_conf)
                button.setVisible(scoped_conf != default_copy)
            elif str_callback:
                button.setVisible(str_callback() != default_str)

        signal.connect(refresh_button_visibility)

    def restore_defaults(*args):
        """
        Broadcast function for the created button. Refreshes the button's visibility after running the input
        load_ui-callback.
        """
        if default_copy:
            load_callback(default_copy)
        elif default_str:
            load_callback(default_str)
        refresh_button_visibility()

    button.clicked.connect(restore_defaults)

    # Initial update
    if scoped_conf:
        write_callback(scoped_conf)
        button.setVisible(scoped_conf != default_copy)
    elif str_callback:
        button.setVisible(str_callback() != default_str)


def add_edit_field(list_widget: QListWidget, mid: int, field_name: str, method_idx=0, repl='', text=''):
    """
    Adds an EditFieldItem widget to the input list widget.

    :param list_widget: QListWidget to add the item to
    :param mid: note-type/model id to use as the field's holder
    :param field_name: name of the field to add
    :param method_idx: index of the method to use when editing a field
    :param repl: optional replacement text to search for replace-method edits
    :param text: input text used to fill in the QLineEdit, used when applying the edit to the selected field
    """
    edit_item = EditFieldItem(list_widget, mid, field_name, EditAction.EditMethod(method_idx), repl, text)
    list_item = QListWidgetItem(list_widget)
    _add_list_item(list_widget, list_item, edit_item)


def add_excluded_field(list_widget: QListWidget, mid: int, field_name=''):
    """
    Inserts a new excluded field item to the excluded fields list if not already present.

    :param list_widget: QListWidget to add the item to
    :param mid: note-type/model ID of the note/field
    :param field_name: text string of the field's name/title
    """

    for i in range(0, list_widget.count()):
        item = list_widget.item(i)
        exclude_item = ExcludeFieldItem.from_list_widget(list_widget, item)
        fields_names = _try_get_field_names(mw.col.models.get(mid))
        if exclude_item.get_model_field_dict() == {f'{mid}': fields_names.index(field_name)}:
            return

    exclude_item = ExcludeFieldItem(list_widget, mid=mid, field_name=field_name)
    list_item = ExcludeFieldItem.ExcludedFieldListItem(list_widget)
    _add_list_item(list_widget, list_item, exclude_item)


def refresh_window():
    """
    Filters the current window state and resets using different function calls depending on whether Anki is currently
    in the reviewer, or not.
    """
    if mw.state != 'review':
        mw.reset()
    else:
        if CURRENT_ANKI_VER >= ANKI_UNDO_UPDATE_VER:
            mw.reviewer.toolkit_wrapper.refresh_if_needed(OpChanges(study_queues=True))
        else:
            mw.reset()


def _bind_tools_options(*args):
    """
    Binds an options dialog launcher to the toolbar menu, under Tools.

    :param args: unused arguments parameter
    """
    config = LeechToolkitConfigManager(mw).config
    if config[Config.TOOLBAR_ENABLED]:
        options_action = QAction(String.LEECH_TOOLKIT_OPTIONS, mw)
        # noinspection PyUnresolvedReferences
        options_action.triggered.connect(on_options_called)

        # Handles edge cases where toolbar action already exists in the tools menu
        if options_action.text() not in [action.text() for action in mw.form.menuTools.actions()]:
            mw.form.menuTools.addAction(options_action)
    else:
        for action in mw.form.menuTools.actions():
            mw.form.menuTools.removeAction(action) if action.text() == String.LEECH_TOOLKIT_OPTIONS else None


def _bind_config_options():
    """
    Binds an options dialog launcher to the Config button in the add-ons window.
    """
    mw.addonManager.setConfigAction(__name__, on_options_called)


def _try_get_field_names(note_type: dict):
    if CURRENT_ANKI_VER > ANKI_LEGACY_VER:
        return mw.col.models.field_names(note_type)
    else:
        return [f["name"] for f in note_type["flds"]]


def _try_get_deck_name(did: int):
    if CURRENT_ANKI_VER > ANKI_LEGACY_VER:
        return mw.col.decks.name_if_exists(did)
    else:
        deck = mw.col.decks.get(did, default=False)
        return deck["name"] if deck else None


def _fill_menu_fields(add_button: QToolButton):
    """
    Fills the field menus for an "Add" field button with respective model-id data and field strings per action.

    :param add_button: button to append the menus to
    """
    menu: QMenu = add_button.menu()
    menu.clear()
    for note_type in mw.col.models.all():
        sub_menu = menu.addMenu(f'{note_type["name"]}')

        for field in _try_get_field_names(note_type):
            action = QAction(f'{field}', add_button)
            action.setData(note_type['id'])
            sub_menu.addAction(action)


def _handle_new_field(list_widget: QListWidget, action: QAction, callback):
    """
    Handler for adding fields to and redrawing field lists.

    :param list_widget: QListWidget referenced for new field events
    :param action: action data retrieved from add action calls that holds model-id data and field text
    :param callback: function for handling more specific field list changes using the input data
    """
    callback(list_widget, action.data(), action.text())
    _redraw_list(list_widget)


def _add_list_item(list_widget: QListWidget, list_item: QListWidgetItem, item_widget: QWidget):
    """
    Adds a QListWidgetItem to the input QListWidget using information from the input QWidget.

    :param list_widget: QListWidget to add the item to
    :param list_item: QListWidgetItem to fill
    :param item_widget: QWidget to use for the list item's UI
    """
    list_item.setSizeHint(item_widget.sizeHint())
    list_item.setFlags(Qt.NoItemFlags)

    list_widget.addItem(list_item)
    list_widget.setItemWidget(list_item, item_widget)


def _redraw_list(list_widget: QListWidget, max_height=256):
    """
    Redraws the QListWidget using its items as a size reference.

    :param list_widget: QListWidget object to resize
    :param max_height: optional maximum size to stop at
    """
    data_height = list_widget.sizeHintForRow(0) * list_widget.count()
    list_widget.setFixedHeight(data_height if data_height < max_height else list_widget.maximumHeight())
    list_widget.setMaximumWidth(list_widget.parent().maximumWidth())
    list_widget.setVisible(list_widget.count() != 0)
    list_widget.currentRowChanged.emit(list_widget.currentRow())  # Used for updating any change receivers


class OptionsDialog(QDialog):
    restore_buttons: List[QPushButton] = []

    class ShortcutHandler(QDialog):
        """
        A Dialog that handles keyboard shortcuts for a given QPushButton.

        Listens for button presses and update the push button
        with the returned keys.
        """

        def __init__(self, parent, button: QPushButton):
            """
            Initialize the ShortcutHandler.
            Sets up the dialog and connects the necessary signals and slots.

            :param parent: parent widget for this dialog
            :param button: push button to update with the returned key
            """
            super().__init__(parent=parent, flags=mw.windowFlags())

            self.button = button
            self.layout = QVBoxLayout()
            self.label = QLabel()
            self.layout.addWidget(self.label, alignment=AlignHCenter | AlignVCenter)

            self.setLayout(self.layout)

            self.main = None
            self.modifiers = []
            self.combination = ''
            self.update_combination()

        def update_combination(self):
            if not self.main and len(self.modifiers) > 0:
                self.combination = f'{"+".join(self.modifiers)}'
            elif self.main and len(self.modifiers) > 0:
                self.combination = f'{"+".join(self.modifiers)}+{chr(self.main)}'
            elif self.main and not len(self.modifiers) > 0:
                self.combination = chr(self.main)
            else:
                self.combination = None

            if not self.combination:
                result = String.SHORTCUT_ELLIPSES
            elif self.combination in Keys.DEFAULT_KEYS or self.main in Keys.DISABLED_KEYS:
                result = String.SHORTCUT_UNRECOGNIZED_OR_DEFAULT
            else:
                result = self.combination
                if self.main and self.main > 0:
                    self.update_shortcut()

            self.label.setText(result)

        def keyPressEvent(self, evt: QKeyEvent):
            if evt.key() in Keys.ESCAPE_KEYS:
                self.close()

            if 30 < evt.key() < 127:
                self.main = evt.key()
            elif evt.key() in Keys.MODIFIER_KEY_DICT.keys():
                self.modifiers.append(Keys.MODIFIER_KEY_DICT[evt.key()])
            else:
                self.main = None
                self.modifiers.clear()

            if self.main or len(self.modifiers) > 0:
                self.update_combination()

        def keyReleaseEvent(self, evt: QKeyEvent):
            if evt.key() in Keys.MODIFIER_KEY_DICT.keys():
                self.modifiers.remove(Keys.MODIFIER_KEY_DICT.get(evt.key(), None))
            else:
                self.main = None

            self.update_combination()

        def update_shortcut(self):
            self.button.setText(self.combination)
            self.close()

    # noinspection PyUnresolvedReferences
    def __init__(self, manager: LeechToolkitConfigManager):
        """
        Add-on options window.

        :param manager: Toolkit Manager object to use for config reads/writes.
        """
        super().__init__(flags=mw.windowFlags())
        self.manager = manager
        self.config = manager.config
        self.ui = Ui_OptionsDialog()
        if int(QT_VERSION_STR.split('.')[1]) < QT5_MARKDOWN_VER:
            self.ui.QTCore = aqt.qt
            self.ui.QTCore.Qt = aqt.qt.Qt
            self.ui.QTCore.Qt.MarkdownText = AutoText
        self.ui.setupUi(OptionsDialog=self)

        self.setWindowIcon(QIcon(f'{Path(__file__).parent.resolve()}\\{LEECH_ICON_PATH}'))

        self.reverse_form = ReverseWidget(flags=mw.windowFlags(), restore_buttons=self.restore_buttons)
        self.ui.optionsScrollLayout.addWidget(self.reverse_form)

        self.leech_form = ActionsWidget(Config.LEECH_ACTIONS, restore_buttons=self.restore_buttons)
        self.ui.actionsScrollLayout.addWidget(self.leech_form)

        self.unleech_form = ActionsWidget(Config.UN_LEECH_ACTIONS, restore_buttons=self.restore_buttons)
        self.ui.actionsScrollLayout.addWidget(self.unleech_form)

        self.restore_buttons.append(append_restore_button(self.ui.markerGroup))
        self.restore_buttons.append(append_restore_button(self.ui.browseButtonGroup))
        self.restore_buttons.append(append_restore_button(self.ui.syncTagCheckbox))
        self.restore_buttons.append(append_restore_button(self.ui.shortcutsGroupbox))
        self.restore_buttons.append(append_restore_button(self.ui.markHtmlGroupbox))

        self.apply_button = self.ui.buttonBox.button(QDialogButtonBox.Apply)
        self.apply_button.setEnabled(False)

        self.ui.buttonBox.button(QDialogButtonBox.Apply).clicked.connect(self.apply)
        self.ui.buttonBox.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.restore_defaults)

        self.ui.leechShortcutButton.clicked.connect(
            lambda *args: self.ShortcutHandler(self, self.ui.leechShortcutButton).exec_()
        )
        self.ui.unleechShortcutButton.clicked.connect(
            lambda *args: self.ShortcutHandler(self, self.ui.unleechShortcutButton).exec_()
        )
        tab_width = QFontMetrics(self.ui.markHtmlTextEdit.font()).horizontalAdvance('    ')
        self.ui.markHtmlTextEdit.setTabStopDistance(tab_width)

        self.ui.syncUpdateButton.clicked.connect(lambda: sync_collection(True))

        self.build_about_page()

        self._load()
        self.setup_restorables()

        # Just in case
        self.ui.tabWidget.setCurrentIndex(0)

    def setup_restorables(self):
        """
        Loads data to default restoration buttons.
        """
        global_signals = {
            'marker_signals': [
                self.ui.markerGroup.clicked,
                self.ui.almostCheckbox.stateChanged,
                self.ui.almostPosDropdown.currentIndexChanged,
                self.ui.almostBackCheckbox.stateChanged,
            ],
            'button_signals': [
                self.ui.browseButtonGroup.clicked,
                self.ui.browseButtonBrowserCheckbox.stateChanged,
                self.ui.browseButtonOverviewCheckbox.stateChanged,
            ],
            'misc_signals': [
                self.ui.toolsOptionsCheckBox.stateChanged,
                self.ui.syncUpdateCheckbox.stateChanged,
                self.ui.toastCheckbox.stateChanged,
            ],
            'sync_tag_signals': [
                self.ui.syncTagCheckbox.clicked,
                self.ui.syncTagLineEdit.textChanged,
            ],
            'mark_html_signals': [
                self.ui.markHtmlTextEdit.textChanged,
            ],
            'shortcut_signals': [
                self.ui.leechShortcutButton.clicked,
                self.ui.unleechShortcutButton.clicked,
            ],
        }

        global_button_args = [
            (
                self.ui.markerGroup.default_button,
                global_signals['marker_signals'],
                self.write_marker,
                self.load_marker,
                self.config[Config.MARKER_OPTIONS],
                Config.DEFAULT_CONFIG[Config.MARKER_OPTIONS],
            ),
            (
                self.ui.browseButtonGroup.default_button,
                global_signals['button_signals'],
                self.write_button,
                self.load_leech_button,
                self.config[Config.BUTTON_OPTIONS],
                Config.DEFAULT_CONFIG[Config.BUTTON_OPTIONS],
            ),
            (
                self.ui.syncTagCheckbox.default_button,
                global_signals['sync_tag_signals'],
                self.write_sync_tag,
                self.load_sync_tag,
                self.config[Config.SYNC_TAG_OPTIONS],
                Config.DEFAULT_CONFIG[Config.SYNC_TAG_OPTIONS],
            ),
            (
                self.ui.shortcutsGroupbox.default_button,
                global_signals['shortcut_signals'],
                self.write_shortcuts,
                self.load_shortcuts,
                self.config[Config.SHORTCUT_OPTIONS],
                Config.DEFAULT_CONFIG[Config.SHORTCUT_OPTIONS],
            ),
            (
                self.ui.markHtmlGroupbox.default_button,
                global_signals['mark_html_signals'],
                self.write_mark_html,
                self.load_mark_html,
                None,
                None,
                self.ui.markHtmlTextEdit.toPlainText,
                MARKER_HTML_TEMP,
            )
        ]

        for args in global_button_args:
            setup_restore_button(*args)

        signal_lists = list(global_signals.values()) \
                       + list(self.leech_form.get_signals().values()) \
                       + list(self.unleech_form.get_signals().values()) \
                       + list(self.reverse_form.get_signals().values())

        for signals in signal_lists:
            self._append_apply_signals(signals)

        leech_conf = self.config[Config.LEECH_ACTIONS]
        unleech_conf = self.config[Config.UN_LEECH_ACTIONS]
        reverse_conf = self.config[Config.REVERSE_OPTIONS]

        self.leech_form.setup_restorables(leech_conf, Config.DEFAULT_CONFIG[Config.LEECH_ACTIONS])
        self.unleech_form.setup_restorables(unleech_conf, Config.DEFAULT_CONFIG[Config.UN_LEECH_ACTIONS])
        self.reverse_form.setup_restorables(reverse_conf, Config.DEFAULT_CONFIG[Config.REVERSE_OPTIONS])

    def _append_apply_signals(self, signals: List[pyqtBoundSignal]):
        for signal in signals:
            signal.connect(lambda *args: self.apply_button.setEnabled(True))

    def apply(self):
        """
        Write options to add-on config, refresh the Anki window, and disable the apply button.
        """
        self._write()
        bind_actions()
        refresh_window()
        self.apply_button.setEnabled(False)

    def restore_defaults(self):
        """
        Restore all options to their default values in the UI.
        """
        self.config = Config.DEFAULT_CONFIG.copy()
        self._load()
        [button.setVisible(False) for button in self.restore_buttons]

    def accept(self) -> None:
        """
        Apply the options and close the dialog.
        """
        self.apply()
        super().accept()

    def build_about_page(self):
        # About page buttons
        self.ui.context_menu = QMenu(self)

        def on_copy_link(button):
            """
            Copies a link to the clipboard based on the input button.
            :param button: button to use for determining which link to copy
            """
            cb = mw.app.clipboard()
            if CURRENT_QT_VER == 6:
                clip_mode = cb.Mode.Clipboard
            else:
                # noinspection PyUnresolvedReferences
                clip_mode = cb.Clipboard
            cb.clear(mode=clip_mode)

            if button.objectName() == self.ui.patreon_button.objectName():
                cb.setText(PATREON_URL, mode=clip_mode)
            elif button.objectName() == self.ui.kofi_button.objectName():
                cb.setText(KOFI_URL, mode=clip_mode)
            elif button.objectName() == self.ui.like_button.objectName():
                cb.setText(ANKI_URL, mode=clip_mode)

        def on_line_context_menu(point, button):
            """
            Handles context menu actions for the input button.
            :param point: input coordinate to display the menu
            :param button: button being clicked/triggered
            """
            self.ui.context_menu = QMenu(self)
            self.ui.context_menu.addAction(String.COPY_LINK_ACTION).triggered.connect(lambda: on_copy_link(button))
            self.ui.context_menu.exec(button.mapToGlobal(point))

        self.ui.kofi_button.setIcon(QIcon(f'{Path(__file__).parent.resolve()}\\{KOFI_ICON_PATH}'))
        self.ui.kofi_button.released.connect(lambda: webbrowser.open(KOFI_URL))
        self.ui.kofi_button.customContextMenuRequested.connect(
            lambda point: on_line_context_menu(point, self.ui.kofi_button)
        )

        self.ui.patreon_button.setIcon(QIcon(f'{Path(__file__).parent.resolve()}\\{PATREON_ICON_PATH}'))
        self.ui.patreon_button.released.connect(lambda: webbrowser.open(PATREON_URL))
        self.ui.patreon_button.customContextMenuRequested.connect(
            lambda point: on_line_context_menu(point, self.ui.patreon_button)
        )

        self.ui.like_button.setIcon(QIcon(f'{Path(__file__).parent.resolve()}\\{ANKI_LIKE_ICON_PATH}'))
        self.ui.like_button.released.connect(lambda: webbrowser.open(ANKI_URL))
        self.ui.like_button.customContextMenuRequested.connect(
            lambda point: on_line_context_menu(point, self.ui.like_button)
        )

        # Update about header text with the current version number
        updated_about_header = self.ui.about_label_header.text().format(version=CURRENT_VERSION)
        self.ui.about_label_header.setText(updated_about_header)

        # Allow link navigation
        self.ui.about_label_body.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.ui.about_label_header.setTextInteractionFlags(Qt.TextBrowserInteraction)

        # Convert markdown to HTML and update
        self.ui.about_label_header.setText(markdown.markdown(self.ui.about_label_header.text()))
        self.ui.about_label_body.setText(markdown.markdown(self.ui.about_label_body.text()))

    def load_marker(self, marker_conf: dict):
        self.ui.markerGroup.setChecked(marker_conf[Config.SHOW_LEECH_MARKER])
        self.ui.almostCheckbox.setChecked(marker_conf[Config.USE_ALMOST_MARKER])
        self.ui.almostPosDropdown.setCurrentIndex(marker_conf[Config.MARKER_POSITION])
        self.ui.almostBackCheckbox.setChecked(marker_conf[Config.ONLY_SHOW_BACK_MARKER])

    def load_leech_button(self, button_conf: dict):
        self.ui.browseButtonGroup.setChecked(button_conf[Config.SHOW_BUTTON])
        self.ui.browseButtonBrowserCheckbox.setChecked(button_conf[Config.SHOW_BROWSER_BUTTON])
        self.ui.browseButtonOverviewCheckbox.setChecked(button_conf[Config.SHOW_OVERVIEW_BUTTON])

    def load_sync_tag(self, sync_tag_conf: dict):
        self.ui.syncTagCheckbox.setChecked(sync_tag_conf[Config.SYNC_TAG_ENABLED])
        self.ui.syncTagLineEdit.setText(sync_tag_conf[Config.SYNC_TAG_TEXT])

    def load_shortcuts(self, shortcut_conf: dict):
        self.ui.leechShortcutButton.setText(shortcut_conf[Config.LEECH_SHORTCUT])
        self.ui.unleechShortcutButton.setText(shortcut_conf[Config.UNLEECH_SHORTCUT])

    def load_mark_html(self, html_str: str = None):
        with open(f'{ROOT_DIR}\\marker_html.html', 'r') as f:
            if not html_str:
                self.ui.markHtmlTextEdit.setPlainText(f.read())
            else:
                self.ui.markHtmlTextEdit.setPlainText(html_str)

    def write_marker(self, marker_conf: dict):
        marker_conf[Config.SHOW_LEECH_MARKER] = self.ui.markerGroup.isChecked()
        marker_conf[Config.USE_ALMOST_MARKER] = self.ui.almostCheckbox.isChecked()
        marker_conf[Config.MARKER_POSITION] = self.ui.almostPosDropdown.currentIndex()
        marker_conf[Config.ONLY_SHOW_BACK_MARKER] = self.ui.almostBackCheckbox.isChecked()

    def write_button(self, button_conf: dict):
        button_conf[Config.SHOW_BUTTON] = self.ui.browseButtonGroup.isChecked()
        button_conf[Config.SHOW_BROWSER_BUTTON] = self.ui.browseButtonBrowserCheckbox.isChecked()
        button_conf[Config.SHOW_OVERVIEW_BUTTON] = self.ui.browseButtonOverviewCheckbox.isChecked()

    def write_sync_tag(self, sync_tag_conf: dict):
        sync_tag_conf[Config.SYNC_TAG_ENABLED] = self.ui.syncTagCheckbox.isChecked()
        sync_tag_conf[Config.SYNC_TAG_TEXT] = self.ui.syncTagLineEdit.text()

    def write_shortcuts(self, shortcut_conf: dict):
        shortcut_conf[Config.LEECH_SHORTCUT] = self.ui.leechShortcutButton.text()
        shortcut_conf[Config.UNLEECH_SHORTCUT] = self.ui.unleechShortcutButton.text()

    def write_mark_html(self, html_str: str = None):
        with open(f'{ROOT_DIR}\\marker_html.html', 'w') as f:
            if not html_str:
                f.write(self.ui.markHtmlTextEdit.toPlainText())
            else:
                f.write(html_str)

    def _load(self):
        """
        Load all options.
        """
        self.ui.toolsOptionsCheckBox.setChecked(self.config[Config.TOOLBAR_ENABLED])
        self.ui.toastCheckbox.setChecked(self.config[Config.TOAST_ENABLED])
        self.ui.syncUpdateCheckbox.setChecked(self.config[Config.SYNC_ENABLED])

        self.load_marker(self.config[Config.MARKER_OPTIONS])
        self.load_leech_button(self.config[Config.BUTTON_OPTIONS])
        self.load_sync_tag(self.config[Config.SYNC_TAG_OPTIONS])
        self.load_shortcuts(self.config[Config.SHORTCUT_OPTIONS])
        self.load_mark_html()

        self.leech_form.load_ui(self.config[Config.LEECH_ACTIONS])
        self.unleech_form.load_ui(self.config[Config.UN_LEECH_ACTIONS])
        self.reverse_form.load_ui(self.config[Config.REVERSE_OPTIONS])

    def _write(self):
        """
        Write all options.
        """
        self.config[Config.TOOLBAR_ENABLED] = self.ui.toolsOptionsCheckBox.isChecked()
        self.config[Config.TOAST_ENABLED] = self.ui.toastCheckbox.isChecked()
        self.config[Config.SYNC_ENABLED] = self.ui.syncUpdateCheckbox.isChecked()

        self.write_marker(self.config[Config.MARKER_OPTIONS])
        self.write_button(self.config[Config.BUTTON_OPTIONS])
        self.write_sync_tag(self.config[Config.SYNC_TAG_OPTIONS])
        self.write_shortcuts(self.config[Config.SHORTCUT_OPTIONS])
        self.write_mark_html()

        self.leech_form.write_all(self.config[Config.LEECH_ACTIONS])
        self.unleech_form.write_all(self.config[Config.UN_LEECH_ACTIONS])
        self.reverse_form.write(self.config[Config.REVERSE_OPTIONS])

        # Save config
        self.manager.save_config()


class ReverseWidget(QWidget):
    def __init__(self, flags, restore_buttons: list = None, global_conf=True):
        """
        Widget container for leech reverse UI options.

        :param flags: QT window flags
        :param restore_buttons: list of buttons to append the reverse widget's restore button to
        :param global_conf: optional global config used for determining option scope and applying config options to
        the widget
        """
        super().__init__(parent=None, flags=flags)
        self.ui = Ui_ReverseForm()
        self.ui.setupUi(self)

        title = self.ui.reverseGroup.title() + (f' {String.GLOBAL_SUFFIX}' if global_conf else '')
        self.ui.reverseGroup.setTitle(title)

        def toggle_threshold(checked: bool):
            self.ui.reverseThresholdSpinbox.setEnabled(checked)

        self.ui.useLeechThresholdCheckbox.stateChanged.connect(lambda checked: toggle_threshold(not checked))

        append_restore_button(self.ui.reverseGroup)
        restore_buttons.append(self.ui.reverseGroup.default_button) if restore_buttons else None

    def get_signals(self):
        return {
            'reverse_signals': [
                self.ui.reverseGroup.clicked,
                self.ui.useLeechThresholdCheckbox.stateChanged,
                self.ui.reverseMethodDropdown.currentIndexChanged,
                self.ui.reverseThresholdSpinbox.valueChanged,
                self.ui.consAnswerSpinbox.valueChanged,
            ]
        }

    def load_ui(self, reverse_config: dict):
        self.ui.reverseGroup.setChecked(reverse_config[Config.REVERSE_ENABLED])
        self.ui.useLeechThresholdCheckbox.setChecked(reverse_config[Config.REVERSE_USE_LEECH_THRESHOLD])
        self.ui.reverseMethodDropdown.setCurrentIndex(reverse_config[Config.REVERSE_METHOD])
        self.ui.reverseThresholdSpinbox.setValue(reverse_config[Config.REVERSE_THRESHOLD])
        self.ui.consAnswerSpinbox.setValue(reverse_config[Config.REVERSE_CONS_ANS])

    def setup_restorables(self, reverse_conf: dict, default_conf: dict = None):
        setup_restore_button(
            self.ui.reverseGroup.default_button,
            list(self.get_signals().values())[0],
            self.write,
            self.load_ui,
            reverse_conf,
            default_conf,
        )

    def write(self, reverse_config: dict):
        reverse_enabled = self.ui.reverseGroup.isChecked()
        reverse_config[Config.REVERSE_ENABLED] = reverse_enabled
        reverse_config[Config.REVERSE_METHOD] = self.ui.reverseMethodDropdown.currentIndex()
        reverse_config[Config.REVERSE_USE_LEECH_THRESHOLD] = self.ui.useLeechThresholdCheckbox.isChecked()
        reverse_config[Config.REVERSE_THRESHOLD] = self.ui.reverseThresholdSpinbox.value()
        reverse_config[Config.REVERSE_CONS_ANS] = self.ui.consAnswerSpinbox.value()


class ActionsWidget(QWidget):
    def __init__(self, actions_type: str, parent=None, expanded=True, dids=None, restore_buttons: list = None):
        """
        Leech/Un-leech action options UI widget.

        :param actions_type: action type string used for determining UI text elements and config values to read/write
        :param parent: parent QObject
        :param expanded: whether to expand the actions expandos by default, or not
        :param dids: options list of deck id's, used to determine config scope (global vs deck) and apply
        deck-specific values
        :param restore_buttons: list of buttons to append the action widget's restore buttons to
        """
        super().__init__(parent, mw.windowFlags())
        self.ui = Ui_ActionsForm()
        self.ui.setupUi(ActionsForm=self)

        self.actions_type = actions_type

        expando_text = String.LEECH_ACTIONS if actions_type == Config.LEECH_ACTIONS else String.UN_LEECH_ACTIONS
        expando_text += f' {String.GLOBAL_SUFFIX}' if not dids else ''

        self.ui.expandoButton.setText(expando_text)

        if CURRENT_ANKI_VER <= ANKI_LEGACY_VER:
            mw.col.decks.all_names_and_ids = legacy_name_id_handler

        self.dids = [int(name_id.id) for name_id in mw.col.decks.all_names_and_ids()] if not dids else dids

        self.ui.editFieldsList.setStyleSheet('#editFieldsList {background-color: transparent;}')

        self.ui.queueExcludedFieldList.setStyleSheet('#editFieldsList {background-color: transparent;}')
        self.ui.queueLabelBottom.setGraphicsEffect(QGraphicsOpacityEffect())
        self.ui.queueLabelTop.setGraphicsEffect(QGraphicsOpacityEffect())

        self.ui.queueFromSpinbox.dropdown = self.ui.queueFromDropdown
        self.ui.queueFromDropdown.currentIndexChanged.connect(lambda *args: self.ui.queueFromSpinbox.refresh())

        self.ui.queueToSpinbox.dropdown = self.ui.queueToDropdown
        self.ui.queueToDropdown.currentIndexChanged.connect(lambda *args: self.ui.queueToSpinbox.refresh())

        self.ui.queueCurrentDeckCheckbox.stateChanged.connect(lambda checked: self.update_queue_info(checked))

        self.add_completer = CustomCompleter(self.ui.addTagsLine)
        self.remove_completer = CustomCompleter(self.ui.removeTagsLine)
        self.deck_completer = CustomCompleter(self.ui.deckMoveLine)

        def update_text_size(text_box: QTextEdit):
            doc_height = text_box.document().size().height()
            max_height, min_height = 256, 24
            if doc_height <= max_height:
                text_box.setFixedHeight(min_height if doc_height <= min_height else doc_height + 5)
            else:
                text_box.setFixedHeight(max_height)

        self.ui.queueExcludeTextEdit.textChanged.connect(lambda *args: update_text_size(self.ui.queueExcludeTextEdit))

        self.ui.editAddFieldButton.setMenu(QMenu(self.ui.editAddFieldButton))
        _fill_menu_fields(self.ui.editAddFieldButton)
        self.ui.editAddFieldButton.menu().triggered.connect(
            lambda action: _handle_new_field(self.ui.editFieldsList, action, add_edit_field)
        )

        self.ui.queueAddFieldButton.setMenu(QMenu(self.ui.queueAddFieldButton))
        _fill_menu_fields(self.ui.queueAddFieldButton)
        self.ui.queueAddFieldButton.menu().triggered.connect(
            lambda action: _handle_new_field(self.ui.queueExcludedFieldList, action, add_excluded_field)
        )

        self.ui.expandoWidget.set_click_function(lambda: self.toggle_expando(self.ui.expandoButton))
        self.ui.expandoButton.pressed.connect(lambda: self.toggle_expando(self.ui.expandoButton))
        self.toggle_expando(self.ui.expandoButton, expanded)

        appended_buttons = [
            append_restore_button(self.ui.flagGroup),
            append_restore_button(self.ui.suspendGroup),
            append_restore_button(self.ui.addTagGroup),
            append_restore_button(self.ui.removeTagGroup),
            append_restore_button(self.ui.forgetGroup),
            append_restore_button(self.ui.editFieldsGroup),
            append_restore_button(self.ui.deckMoveGroup),
            append_restore_button(self.ui.rescheduleGroup),
            append_restore_button(self.ui.queueGroup),
        ]

        [restore_buttons.append(button) for button in appended_buttons] if restore_buttons else None

    def get_signals(self):
        return {
            'flag_signals': [
                self.ui.flagGroup.clicked,
                self.ui.flagDropdown.currentTextChanged,
            ],
            'suspend_signals': [
                self.ui.suspendGroup.clicked,
                self.ui.suspendOnButton.toggled,
                self.ui.suspendOffButton.toggled,
            ],
            'add_tags_signals': [
                self.ui.addTagGroup.clicked,
                self.ui.addTagsLine.textChanged,
            ],
            'remove_tags_signals': [
                self.ui.removeTagGroup.clicked,
                self.ui.removeTagsLine.textChanged,
            ],
            'forget_signals': [
                self.ui.forgetGroup.clicked,
                self.ui.forgetOnRadio.toggled,
                self.ui.forgetOffRadio.toggled,
                self.ui.forgetResetCheckbox.stateChanged,
                self.ui.forgetRestorePosCheckbox.stateChanged,
            ],
            'edit_fields_signals': [
                self.ui.editFieldsGroup.clicked,
                self.ui.editFieldsList.currentRowChanged,
            ],
            'deck_move_signals': [
                self.ui.deckMoveGroup.clicked,
                self.ui.deckMoveLine.textChanged,
            ],
            'reschedule_signals': [
                self.ui.rescheduleGroup.clicked,
                self.ui.rescheduleFromDays.valueChanged,
                self.ui.rescheduleToDays.valueChanged,
                self.ui.rescheduleResetCheckbox.stateChanged,
            ],
            'queue_signals': [
                self.ui.queueGroup.clicked,
                self.ui.queueCurrentDeckCheckbox.stateChanged,
                self.ui.queueFromSpinbox.valueChanged,
                self.ui.queueToSpinbox.valueChanged,
                self.ui.queueFromDropdown.currentIndexChanged,
                self.ui.queueToDropdown.currentIndexChanged,
                self.ui.queueSimilarCheckbox.stateChanged,
                self.ui.queueIncludeFieldsCheckbox.stateChanged,
                self.ui.queueExcludedFieldList.currentRowChanged,
                self.ui.queueExcludeTextEdit.textChanged,
                self.ui.queueRatioSlider.valueChanged,
                self.ui.queueSiblingCheckbox.stateChanged,
            ],
        }

    def setup_restorables(self, actions_config: dict, default_config):
        # Remove any re-assignment potential issues
        signals = self.get_signals()
        restorable_args = [
            (
                self.ui.flagGroup.default_button,
                signals['flag_signals'],
                self.write_flag,
                self.load_flag,
                actions_config[Action.FLAG],
                default_config[Action.FLAG],
            ),
            (
                self.ui.suspendGroup.default_button,
                signals['suspend_signals'],
                self.write_suspend,
                self.load_suspend,
                actions_config[Action.SUSPEND],
                default_config[Action.SUSPEND],
            ),
            (
                self.ui.addTagGroup.default_button,
                signals['add_tags_signals'],
                self.write_add_tags,
                self.load_add_tags,
                actions_config[Action.ADD_TAGS],
                default_config[Action.ADD_TAGS],
            ),
            (
                self.ui.removeTagGroup.default_button,
                signals['remove_tags_signals'],
                self.write_remove_tags,
                self.load_remove_tags,
                actions_config[Action.REMOVE_TAGS],
                default_config[Action.REMOVE_TAGS],
            ),
            (
                self.ui.forgetGroup.default_button,
                signals['forget_signals'],
                self.write_forget,
                self.load_forget,
                actions_config[Action.FORGET],
                default_config[Action.FORGET],
            ),
            (
                self.ui.editFieldsGroup.default_button,
                signals['edit_fields_signals'],
                self.write_edit_fields,
                self.load_edit_fields,
                actions_config[Action.EDIT_FIELDS],
                default_config[Action.EDIT_FIELDS],
            ),
            (
                self.ui.deckMoveGroup.default_button,
                signals['deck_move_signals'],
                self.write_move_deck,
                self.load_move_deck,
                actions_config[Action.MOVE_DECK],
                default_config[Action.MOVE_DECK],
            ),
            (
                self.ui.rescheduleGroup.default_button,
                signals['reschedule_signals'],
                self.write_reschedule,
                self.load_reschedule,
                actions_config[Action.RESCHEDULE],
                default_config[Action.RESCHEDULE],
            ),
            (
                self.ui.queueGroup.default_button,
                signals['queue_signals'],
                self.write_add_to_queue,
                self.load_add_to_queue,
                actions_config[Action.ADD_TO_QUEUE],
                default_config[Action.ADD_TO_QUEUE],
            )
        ]
        [setup_restore_button(*args) for args in restorable_args]

    # FLAG
    def load_flag(self, action_conf: dict):
        self.ui.flagGroup.setChecked(action_conf[Action.ENABLED])
        self.ui.flagDropdown.setCurrentIndex(action_conf[Action.INPUT])

        flag_manager = aqt.flags.FlagManager(mw) if CURRENT_ANKI_VER > ANKI_LEGACY_VER else None

        for index in range(1, self.ui.flagDropdown.count()):
            if CURRENT_ANKI_VER > ANKI_LEGACY_VER:
                flag = flag_manager.get_flag(index)
                pixmap = QPixmap(flag.icon.path)
                mask = pixmap.createMaskFromColor(QColor('black'), Qt.MaskOutColor)
                pixmap.fill(QColor(flag.icon.current_color(mw.pm.night_mode())))
                pixmap.setMask(mask)
                self.ui.flagDropdown.setItemIcon(index, QIcon(pixmap))
                self.ui.flagDropdown.setItemText(index, f'{flag.label}')
            else:
                self.ui.flagDropdown.setItemText(index, f'{LEGACY_FLAGS_PLACEHOLDER[index - 1]}')

    # SUSPEND
    def load_suspend(self, action_conf: dict):
        self.ui.suspendGroup.setChecked(action_conf[Action.ENABLED])
        self.ui.suspendOnButton.setChecked(action_conf[Action.INPUT])
        self.ui.suspendOffButton.setChecked(not action_conf[Action.INPUT])

    # ADD TAGS
    def load_add_tags(self, action_conf: dict):
        # TAGS
        tag_suggestions = mw.col.weakref().tags.all() + list(Macro.MACROS)

        self.add_completer.set_list([suggestion for suggestion in tag_suggestions if suggestion != Macro.REGEX])
        self.ui.addTagGroup.setChecked(action_conf[Action.ENABLED])
        self.ui.addTagsLine.setText(action_conf[Action.INPUT])
        self.ui.addTagsLine.setCompleter(self.add_completer)

    # REMOVE TAGS
    def load_remove_tags(self, action_conf: dict):
        # TAGS
        tag_suggestions = mw.col.weakref().tags.all() + list(Macro.MACROS)
        self.remove_completer.set_list(tag_suggestions)
        self.ui.removeTagGroup.setChecked(action_conf[Action.ENABLED])
        self.ui.removeTagsLine.setText(action_conf[Action.INPUT])
        self.ui.removeTagsLine.setCompleter(self.remove_completer)

    # FORGET
    def load_forget(self, action_conf: dict):
        self.ui.forgetGroup.setChecked(action_conf[Action.ENABLED])
        self.ui.forgetOnRadio.setChecked(action_conf[Action.INPUT][0])
        self.ui.forgetOffRadio.setChecked(not action_conf[Action.INPUT][0])
        self.ui.forgetRestorePosCheckbox.setChecked(action_conf[Action.INPUT][1])
        self.ui.forgetResetCheckbox.setChecked(action_conf[Action.INPUT][2])

    # EDIT FIELD
    def load_edit_fields(self, action_conf: dict):
        self.ui.editFieldsGroup.setChecked(action_conf[Action.ENABLED])
        self.ui.editFieldsList.clear()
        for field_item in action_conf[Action.INPUT]:
            mid, item_data = list(field_item.items())[0]
            if CURRENT_ANKI_VER > ANKI_LEGACY_VER:
                note_dict = mw.col.models.get(NotetypeId(mid) if CURRENT_ANKI_VER > ANKI_LEGACY_VER else int(mid))
                field_name = _try_get_field_names(note_dict)[item_data[0]] if note_dict else String.NOTE_NOT_FOUND
            else:
                note_dict = mw.col.models.get(int(mid))
                field_name = _try_get_field_names(note_dict)[item_data[0]] if note_dict else String.NOTE_NOT_FOUND

            add_edit_field(self.ui.editFieldsList, mid, field_name, item_data[1], item_data[2], item_data[3])

        _redraw_list(self.ui.editFieldsList, max_fields_height)

    # DECK MOVE
    def load_move_deck(self, action_conf: dict):
        self.ui.deckMoveGroup.setChecked(action_conf[Action.ENABLED])
        if CURRENT_ANKI_VER <= ANKI_LEGACY_VER:
            mw.col.decks.all_names_and_ids = legacy_name_id_handler
        suggestions = [dnid.name for dnid in mw.col.decks.all_names_and_ids()]
        [suggestions.append(suggestion) for suggestion in Macro.MACROS if suggestion != Macro.REGEX]
        deck_name = _try_get_deck_name(action_conf[Action.INPUT])
        self.deck_completer.set_list(suggestions)
        self.ui.deckMoveLine.setCompleter(self.deck_completer)
        self.ui.deckMoveLine.setText(deck_name)

    # RESCHEDULE
    def load_reschedule(self, action_conf: dict):
        reschedule_input = action_conf[Action.INPUT]
        self.ui.rescheduleGroup.setChecked(action_conf[Action.ENABLED])
        self.ui.rescheduleFromDays.setValue(reschedule_input[RescheduleAction.FROM])
        self.ui.rescheduleToDays.setValue(reschedule_input[RescheduleAction.TO])
        self.ui.rescheduleResetCheckbox.setChecked(reschedule_input[RescheduleAction.RESET])

    # ADD TO QUEUE
    def load_add_to_queue(self, action_conf: dict):
        queue_input = action_conf[Action.INPUT]
        self.ui.queueGroup.setChecked(action_conf[Action.ENABLED])

        self.ui.queueFromDropdown.setCurrentIndex(queue_input[QueueAction.FROM_INDEX])
        self.ui.queueToDropdown.setCurrentIndex(queue_input[QueueAction.TO_INDEX])
        self.ui.queueFromSpinbox.setValue(queue_input[QueueAction.FROM_VAL])
        self.ui.queueToSpinbox.setValue(queue_input[QueueAction.TO_VAL])

        self.ui.queueCurrentDeckCheckbox.setChecked(queue_input[QueueAction.CURRENT_DECK])
        self.update_queue_info(queue_input[QueueAction.CURRENT_DECK])

        self.ui.queueSimilarCheckbox.setChecked(queue_input[QueueAction.NEAR_SIMILAR])
        self.ui.queueExcludeTextEdit.setText(queue_input[QueueAction.EXCLUDED_TEXT])
        self.ui.queueIncludeFieldsCheckbox.setChecked(queue_input[QueueAction.INCLUSIVE_FIELDS])
        self.ui.queueRatioSlider.setValue(queue_input[QueueAction.SIMILAR_RATIO] * 100)

        self.ui.queueExcludedFieldList.clear()
        for note_dict in queue_input[QueueAction.FILTERED_FIELDS]:
            mid = list(note_dict)[0]
            for field_ord in list(note_dict.values()):
                note = mw.col.models.get(NotetypeId(int(mid)) if CURRENT_ANKI_VER > ANKI_LEGACY_VER else int(mid))
                if not note:
                    continue
                field_name = _try_get_field_names(note)[field_ord]

                add_excluded_field(self.ui.queueExcludedFieldList, mid, field_name)
        self.ui.queueExcludedFieldList.sortItems()
        _redraw_list(self.ui.queueExcludedFieldList)

        self.ui.queueSiblingCheckbox.setChecked(queue_input[QueueAction.NEAR_SIBLING])

    def update_queue_info(self, use_current_deck=False):
        """
        Updates the current queue label text using the current deck id's or global scope values.

        :param use_current_deck: whether to use the current deck for the queue reference
        """
        cmd = f'SELECT min(due), max(due) FROM cards WHERE type={CARD_TYPE_NEW} AND odid=0'
        cmd += f' AND did IN {anki.decks.ids2str(self.dids)}' if use_current_deck else ''

        top, bottom = mw.col.db.first(cmd)

        self.ui.queueLabelTopPos.setText(str(top))
        self.ui.queueLabelBottomPos.setText(str(bottom))

    def load_ui(self, actions_conf: dict):
        # A little easier to read/debug
        self.load_flag(actions_conf[Action.FLAG])
        self.load_suspend(actions_conf[Action.SUSPEND])
        self.load_add_tags(actions_conf[Action.ADD_TAGS])
        self.load_remove_tags(actions_conf[Action.REMOVE_TAGS])
        self.load_forget(actions_conf[Action.FORGET])
        self.load_edit_fields(actions_conf[Action.EDIT_FIELDS])
        self.load_move_deck(actions_conf[Action.MOVE_DECK])
        self.load_reschedule(actions_conf[Action.RESCHEDULE])
        self.load_add_to_queue(actions_conf[Action.ADD_TO_QUEUE])

    def write_all(self, actions_config: dict):
        # A little easier to read/debug
        self.write_flag(actions_config[Action.FLAG])
        self.write_suspend(actions_config[Action.SUSPEND])
        self.write_add_tags(actions_config[Action.ADD_TAGS])
        self.write_remove_tags(actions_config[Action.REMOVE_TAGS])
        self.write_forget(actions_config[Action.FORGET])
        self.write_edit_fields(actions_config[Action.EDIT_FIELDS])
        self.write_move_deck(actions_config[Action.MOVE_DECK], True)
        self.write_reschedule(actions_config[Action.RESCHEDULE])
        self.write_add_to_queue(actions_config[Action.ADD_TO_QUEUE])

    def write_flag(self, actions_config: dict):
        actions_config[Action.ENABLED] = self.ui.flagGroup.isChecked()
        actions_config[Action.INPUT] = self.ui.flagDropdown.currentIndex()

    def write_suspend(self, actions_config: dict):
        actions_config[Action.ENABLED] = self.ui.suspendGroup.isChecked()
        actions_config[Action.INPUT] = self.ui.suspendOnButton.isChecked()

    def write_add_tags(self, actions_config: dict):
        actions_config[Action.ENABLED] = self.ui.addTagGroup.isChecked()
        actions_config[Action.INPUT] = \
            mw.col.tags.join(mw.col.tags.split(self.ui.addTagsLine.text()))

    def write_remove_tags(self, actions_config: dict):
        actions_config[Action.ENABLED] = self.ui.removeTagGroup.isChecked()
        actions_config[Action.INPUT] = \
            mw.col.tags.join(mw.col.tags.split(self.ui.removeTagsLine.text()))

    def write_forget(self, actions_config: dict):
        actions_config[Action.ENABLED] = self.ui.forgetGroup.isChecked()
        actions_config[Action.INPUT][0] = self.ui.forgetOnRadio.isChecked()
        actions_config[Action.INPUT][1] = self.ui.forgetRestorePosCheckbox.isChecked()
        actions_config[Action.INPUT][2] = self.ui.forgetResetCheckbox.isChecked()

    def write_edit_fields(self, actions_config: dict):
        actions_config[Action.ENABLED] = self.ui.editFieldsGroup.isChecked()
        edit_input: list = actions_config[Action.INPUT]

        edit_input.clear()
        for i in range(self.ui.editFieldsList.count()):
            item = EditFieldItem.from_list_widget(self.ui.editFieldsList, self.ui.editFieldsList.item(i))
            edit_input.append(item.get_field_edit_dict()) if item is not None else None

    def write_move_deck(self, actions_config: dict, should_write=False):
        actions_config[Action.ENABLED] = self.ui.deckMoveGroup.isChecked()
        stored_deckname = self.ui.deckMoveLine.text()
        actions_config[Action.INPUT] = mw.col.decks.id(stored_deckname, should_write) if stored_deckname else ''

    def write_reschedule(self, actions_config: dict):
        actions_config[Action.ENABLED] = self.ui.rescheduleGroup.isChecked()
        reschedule_input = actions_config[Action.INPUT]
        reschedule_input[RescheduleAction.FROM] = self.ui.rescheduleFromDays.value()
        reschedule_input[RescheduleAction.TO] = self.ui.rescheduleToDays.value()
        reschedule_input[RescheduleAction.RESET] = self.ui.rescheduleResetCheckbox.isChecked()

    def write_add_to_queue(self, actions_config: dict):
        actions_config[Action.ENABLED] = self.ui.queueGroup.isChecked()

        queue_input = actions_config[Action.INPUT]

        queue_input[QueueAction.CURRENT_DECK] = self.ui.queueCurrentDeckCheckbox.isChecked()
        queue_input[QueueAction.FROM_INDEX] = self.ui.queueFromDropdown.currentIndex()
        queue_input[QueueAction.TO_INDEX] = self.ui.queueToDropdown.currentIndex()
        queue_input[QueueAction.FROM_VAL] = self.ui.queueFromSpinbox.formatted_value()
        queue_input[QueueAction.TO_VAL] = self.ui.queueToSpinbox.formatted_value()
        queue_input[QueueAction.NEAR_SIMILAR] = self.ui.queueSimilarCheckbox.isChecked()
        queue_input[QueueAction.NEAR_SIBLING] = self.ui.queueSiblingCheckbox.isChecked()
        queue_input[QueueAction.INCLUSIVE_FIELDS] = self.ui.queueIncludeFieldsCheckbox.isChecked()

        queue_input[QueueAction.FILTERED_FIELDS] = []
        for i in range(self.ui.queueExcludedFieldList.count()):
            item = self.ui.queueExcludedFieldList.item(i)
            field_item = ExcludeFieldItem.from_list_widget(self.ui.queueExcludedFieldList, item)
            if field_item is not None:
                field_dict = field_item.get_model_field_dict()
                queue_input[QueueAction.FILTERED_FIELDS].append(field_dict)

        queue_input[QueueAction.EXCLUDED_TEXT] = self.ui.queueExcludeTextEdit.toPlainText()
        queue_input[QueueAction.SIMILAR_RATIO] = self.ui.queueRatioSlider.value() / 100

    def toggle_expando(self, button: QToolButton, toggle: bool = None):
        """
        Toggles the action expando's expanded state to the input, or opposite of its current value.

        :param button: expando QToolButton reference
        :param toggle: optional toggle assignment, expands if true, else collapses
        """
        toggle = not self.ui.actionsFrame.isVisible() if toggle is None else toggle
        button.setArrowType(arrow_types[toggle])
        self.ui.actionsFrame.setVisible(toggle) if button == self.ui.expandoButton else None


class ExcludeFieldItem(QWidget):

    @staticmethod
    def from_list_widget(field_list: QListWidget, item: QListWidgetItem) -> "ExcludeFieldItem":
        """
        Returns an ExcludedFieldItem using a base QListWidgetItem.

        :param field_list: reference list
        :param item: QListWidgetItem object located in the referenced list
        :return: an ExcludedFieldItem object
        """
        return field_list.itemWidget(item)

    def __init__(self, list_widget: QListWidget, mid: int, field_name: str):
        """
        Field item used in excluded field lists.

        :param list_widget: QListWidget reference
        :param mid: note-type/model id for the field
        :param field_name: field name string
        """
        super().__init__(flags=mw.windowFlags())
        self.list_widget = list_widget
        self.mid = mid
        self.widget = Ui_ExcludedFieldItem()
        self.widget.setupUi(ExcludedFieldItem=self)
        self.widget.fieldLabel.setText(field_name)
        self.widget.removeButton.setIcon(QIcon(f'{Path(__file__).parent.resolve()}\\{REMOVE_ICON_PATH}'))
        nid = NoteId(self.mid) if CURRENT_ANKI_VER > ANKI_LEGACY_VER else self.mid
        self.widget.fieldLabel.setToolTip(f'{mw.col.models.get(nid)["name"]}')

        def remove_self(_):
            """
            Removes the current item from its list widget.

            :param _: placeholder argument given by QAction calls
            """
            for i in range(self.list_widget.count()):
                item = self.list_widget.item(i)
                if self == self.from_list_widget(self.list_widget, item):
                    self.list_widget.takeItem(i)
                    _redraw_list(self.list_widget)

        self.widget.removeButton.clicked.connect(remove_self)

    def get_model_field_dict(self):
        """
        Retrieves a dictionary object for the current item.

        :return: a dict object with the format {'note-type/model id': field-ord/field index}
        """
        fields_names = _try_get_field_names(mw.col.models.get(self.mid))
        return {f'{self.mid}': fields_names.index(self.widget.fieldLabel.text())}

    class ExcludedFieldListItem(QListWidgetItem):
        """
        ExcludedFieldListItem used for comparing items against each other.
        """

        def __lt__(self, other):
            """
            Custom less than function for ExcludedFieldItems.

            :param other: other ExcludedFieldListItem object
            :return: true if this item should be below another one, else false if not found or above it
            """
            this_item = ExcludeFieldItem.from_list_widget(self.listWidget(), self)
            other_item = ExcludeFieldItem.from_list_widget(other.listWidget(), other)
            if other_item is None:
                return False
            else:
                this_data = f'{this_item.mid}{this_item.widget.fieldLabel.text()}'
                other_data = f'{other_item.mid}{other_item.widget.fieldLabel.text()}'
                return this_data < other_data


class EditFieldItem(QWidget):
    mid: int
    note_type_dict: dict
    model_name: str
    field_name: str
    list_widget: QListWidget

    @staticmethod
    def from_list_widget(edit_fields_list: QListWidget, item: QListWidgetItem) -> "EditFieldItem":
        """
        Returns an EditFieldItem using a base QListWidgetItem.

        :param edit_fields_list: reference list
        :param item: QListWidgetItem object located in the referenced list
        :return: an EditFieldItem object
        """
        return edit_fields_list.itemWidget(item)

    def __init__(
        self,
        edit_list: QListWidget,
        mid: int,
        field_name: str,
        method_idx: EditAction.EditMethod,
        repl: str,
        text: str,
    ):
        """
        Field item used in edit field lists.

        :param edit_list: QListWidget object holding edit field items
        :param mid: note-type/model id for the field
        :param field_name: field name string
        :param method_idx: index of the method to use when editing a field
        :param repl: optional replacement text to search for replace-method edits
        :param text: input text used to fill in the QLineEdit, used when applying the edit to the selected field
        """
        super().__init__(flags=mw.windowFlags())
        self.context_menu = QMenu(self)
        self.method_idx = method_idx
        self._repl = repl
        self._text = text

        self.widget = Ui_EditFieldItem()
        self.widget.setupUi(EditFieldItem=self)
        self.widget.fieldButtonLabel.setMenu(QMenu(self.widget.fieldButtonLabel))
        self.widget.removeButton.setIcon(QIcon(f'{Path(__file__).parent.resolve()}\\{REMOVE_ICON_PATH}'))

        self.set_model(edit_list, mid, field_name)

        def remove_self(*args):
            """
            Removes the current item from its list widget.

            :param args: unused arguments parameter
            """
            for i in range(self.list_widget.count()):
                item = self.list_widget.item(i)
                if self == self.from_list_widget(self.list_widget, item):
                    self.list_widget.takeItem(i)
                    _redraw_list(self.list_widget)

        self.widget.removeButton.clicked.connect(remove_self)
        self.widget.methodDropdown.currentIndexChanged.connect(self.update_method)
        self.widget.fieldButtonLabel.setMenu(QMenu(self.widget.fieldButtonLabel))
        self.widget.fieldButtonLabel.menu().triggered.connect(
            lambda action: _handle_new_field(self.list_widget, action, self.set_model)
        )
        _fill_menu_fields(self.widget.fieldButtonLabel)

        self.completer = CustomCompleter(self.widget.inputEdit)
        self.completer.set_list([suggestion for suggestion in Macro.MACROS if suggestion != Macro.REGEX])
        self.widget.inputEdit.setCompleter(self.completer)

        self._load()

    def set_model(self, list_widget, mid: int, field_name: str):
        """
        Set the list note-type/model and field.

        :param list_widget: QListWidget object holding edit field items
        :param mid: index of the method to use when editing a field
        :param field_name: field name string
        """
        self.list_widget = list_widget
        self.mid = mid
        self.field_name = field_name
        self._load()

    def _load(self):
        self.note_type_dict = mw.col.models.get(
            NotetypeId(self.mid) if CURRENT_ANKI_VER > ANKI_LEGACY_VER else int(self.mid)
        )
        self.model_name = self.note_type_dict["name"] if self.note_type_dict else ''
        self.widget.fieldButtonLabel.setToolTip(self.model_name)
        self.widget.fieldButtonLabel.setText(self.field_name)
        self.update_method(self.method_idx)
        self.widget.replaceEdit.setText(self._repl)
        self.widget.inputEdit.setText(self._text)

    def update_method(self, method_idx: int):
        """
        Function for updating UI elements and the current edit method index.

        Does not update UI if method is negative.

        :param method_idx: new method index
        """
        self.method_idx = method_idx
        if self.method_idx >= 0:
            replace_selected = self.method_idx in (EditAction.REPLACE_METHOD, EditAction.REGEX_METHOD)
            self.widget.methodDropdown.setCurrentIndex(self.method_idx)
            self.widget.replaceEdit.setVisible(replace_selected)
            self.widget.inputEdit.setPlaceholderText(String.REPLACE_WITH if replace_selected else String.OUTPUT_TEXT)

    def get_field_edit_dict(self):
        if self.note_type_dict:
            fields_names = _try_get_field_names(self.note_type_dict)
            field_idx = fields_names.index(self.widget.fieldButtonLabel.text())
        else:
            field_idx = 0
        method_idx = self.widget.methodDropdown.currentIndex()
        repl, text = self.widget.replaceEdit.text(), self.widget.inputEdit.text()

        return {f'{self.mid}': [field_idx, method_idx, repl, text]}
