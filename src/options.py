"""
MIT License: Copyright (c) 2022 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
Full license text available in "LICENSE" file packaged with the program.
"""
from pathlib import Path

import anki.decks
import aqt.flags
from anki.consts import CARD_TYPE_NEW
from anki.models import NotetypeId
from anki.notes import NoteId
from aqt import mw
from aqt.qt import (
    Qt,
    QAction,
    QDialog,
    QIcon,
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
)

from .config import LeechToolkitConfigManager
from .consts import (
    String, Config, Action, Macro, REMOVE_ICON_PATH, EditAction, RescheduleAction, QueueAction,
    RESTORE_ICON_PATH,
)
from .sync import sync_collection
from ..res.ui.actions_form import Ui_ActionsForm
from ..res.ui.edit_field_item import Ui_EditFieldItem
from ..res.ui.exclude_field_item import Ui_ExcludedFieldItem
from ..res.ui.forms import CustomCompleter
from ..res.ui.options_dialog import Ui_OptionsDialog
from ..res.ui.reverse_form import Ui_ReverseForm

max_fields_height = 572
max_queue_height = 256
arrow_types = [Qt.RightArrow, Qt.DownArrow]


def bind_actions():
    _bind_config_options()
    _bind_tools_options()


def on_options_called(*args):
    options = OptionsDialog(LeechToolkitConfigManager(mw))
    options.exec()


def append_restore_button(parent: QWidget, insert_col=4):
    if not hasattr(parent, 'button'):
        parent.default_button = aqt.qt.QPushButton(parent)

        parent.default_button.setMaximumSize(QSize(16, 16))
        parent.default_button.setFlat(True)
        parent.default_button.setToolTip(String.RESTORE_DEFAULT_SETTING)
        parent.default_button.setIcon(QIcon(f'{Path(__file__).parent.resolve()}\\{RESTORE_ICON_PATH}'))

        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(parent.default_button.sizePolicy().hasHeightForWidth())
        parent.default_button.setSizePolicy(size_policy)
        parent.default_button.setContentsMargins(0, 0, 0, 0)

        layout = parent.parent().layout()
        pos = layout.indexOf(parent) + 1

        if layout is not None:
            if isinstance(layout, QGridLayout):
                layout.addItem(parent.default_button, pos, insert_col)
            elif isinstance(layout, QBoxLayout):
                layout.insertWidget(pos, parent.default_button, alignment=Qt.AlignRight | Qt.AlignBottom)
            else:
                layout.addWidget(parent.default_button)

            layout.insertSpacing(layout.indexOf(parent), 6)

    return parent.default_button


def setup_restore_button(
    default_button: aqt.qt.QPushButton,
    signals: list[pyqtBoundSignal],
    write_callback,
    load_callback,
    scoped_conf: dict,
    default_scoped_conf: dict = None,
):
    default_copy = default_scoped_conf.copy() if default_scoped_conf else None

    for signal in signals:
        def refresh_button_visibility(*args):
            """
            Intercept function for the created button. Refreshes the button's visibility after running the input
            write-callback.
            """
            write_callback(scoped_conf)
            default_button.setVisible(scoped_conf != default_copy)

        signal.connect(refresh_button_visibility)

    def restore_defaults(*args):
        """
        Broadcast function for the created button. Refreshes the button's visibility after running the input
        load_ui-callback.
        """
        load_callback(default_copy)
        refresh_button_visibility()

    default_button.clicked.connect(restore_defaults)

    # Initial update
    default_button.setVisible(scoped_conf != default_copy)


def add_edit_field(list_widget: QListWidget, mid: int, field_name: str, method_idx=0, repl='', text=''):
    edit_item = EditFieldItem(list_widget, mid, field_name, EditAction.EditMethod(method_idx), repl, text)
    list_item = QListWidgetItem(list_widget)
    _add_list_item(list_widget, list_item, edit_item)


def add_excluded_field(list_widget: QListWidget, mid: int, field_name=''):
    """
Inserts a new excluded field item to the excluded fields list if not already present.
    :param list_widget:
    :param mid: Model ID of the note/field
    :param field_name: text string of the field's name/title
    """

    for i in range(0, list_widget.count()):
        item = list_widget.item(i)
        exclude_item = ExcludeFieldItem.from_list_widget(list_widget, item)
        fields_names = mw.col.models.field_names(mw.col.models.get(mid))
        if exclude_item.get_model_field_dict() == {f'{mid}': fields_names.index(field_name)}:
            return

    exclude_item = ExcludeFieldItem(list_widget, mid=mid, field_name=field_name)
    list_item = ExcludeFieldItem.ExcludedFieldListItem(list_widget)
    _add_list_item(list_widget, list_item, exclude_item)


def _bind_tools_options(*args):
    config = LeechToolkitConfigManager(mw).config
    if config[Config.TOOLBAR_ENABLED]:
        options_action = QAction(String.TOOLBAR_OPTIONS, mw)
        options_action.triggered.connect(on_options_called)

        # Handles edge cases where toolbar action already exists in the tools menu
        if options_action.text() not in [action.text() for action in mw.form.menuTools.actions()]:
            mw.form.menuTools.addAction(options_action)
    else:
        for action in mw.form.menuTools.actions():
            mw.form.menuTools.removeAction(action) if action.text() == String.TOOLBAR_OPTIONS else None


def _bind_config_options():
    mw.addonManager.setConfigAction(__name__, on_options_called)


def _fill_menu_fields(add_button: aqt.qt.QToolButton):
    menu: QMenu = add_button.menu()
    menu.clear()
    for note_type in mw.col.models.all():
        sub_menu = menu.addMenu(f'{note_type["name"]}')

        for field in mw.col.models.field_names(note_type):
            action = QAction(f'{field}', add_button)
            action.setData(note_type['id'])
            sub_menu.addAction(action)


def _handle_new_field(list_widget: QListWidget, action: QAction, callback):
    callback(list_widget, action.data(), action.text())
    _redraw_list(list_widget)


def _add_list_item(list_widget: QListWidget, list_item: QListWidgetItem, item_widget: QWidget):
    list_item.setSizeHint(item_widget.sizeHint())
    list_item.setFlags(Qt.NoItemFlags)

    list_widget.addItem(list_item)
    list_widget.setItemWidget(list_item, item_widget)


def _redraw_list(fields_list: QListWidget, max_height=256):
    data_height = fields_list.sizeHintForRow(0) * fields_list.count()
    fields_list.setFixedHeight(data_height if data_height < max_height else fields_list.maximumHeight())
    fields_list.setMaximumWidth(fields_list.parent().maximumWidth())
    fields_list.setVisible(fields_list.count() != 0)
    fields_list.currentRowChanged.emit(fields_list.currentRow())  # Used for updating any change receivers


class OptionsDialog(QDialog):
    restore_buttons: list[aqt.qt.QPushButton] = []

    def __init__(self, manager: LeechToolkitConfigManager):
        super().__init__(flags=mw.windowFlags())
        self.manager = manager
        self.config = manager.config
        self.ui = Ui_OptionsDialog()
        self.ui.setupUi(OptionsDialog=self)

        self.reverse_form = ReverseWidget(flags=mw.windowFlags(), restore_buttons=self.restore_buttons)
        self.ui.optionsScrollLayout.addWidget(self.reverse_form)

        self.leech_form = ActionsWidget(Config.LEECH_ACTIONS, restore_buttons=self.restore_buttons)
        self.ui.actionsScrollLayout.addWidget(self.leech_form)

        self.unleech_form = ActionsWidget(Config.UN_LEECH_ACTIONS, restore_buttons=self.restore_buttons)
        self.ui.actionsScrollLayout.addWidget(self.unleech_form)

        self.restore_buttons.append(append_restore_button(self.ui.markerGroup))
        self.restore_buttons.append(append_restore_button(self.ui.browseButtonGroup))
        self.restore_buttons.append(append_restore_button(self.ui.syncTagCheckbox))

        self.apply_button = self.ui.buttonBox.button(aqt.qt.QDialogButtonBox.Apply)
        self.apply_button.setEnabled(False)

        self.ui.buttonBox.button(aqt.qt.QDialogButtonBox.Apply).clicked.connect(self.apply)
        self.ui.buttonBox.button(aqt.qt.QDialogButtonBox.RestoreDefaults).clicked.connect(self.restore_defaults)

        self.ui.syncUpdateButton.clicked.connect(sync_collection)

        self._load()
        self.setup_restorables()

        # Just in case
        self.ui.tabWidget.setCurrentIndex(0)

    def setup_restorables(self):
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
            'toolbar_signals': [
                self.ui.toolsOptionsCheckBox.stateChanged,
            ],
            'sync_signals': [
                self.ui.syncUpdateCheckbox.stateChanged,
            ],
            'sync_tag_signals': [
                self.ui.syncTagCheckbox.clicked,
                self.ui.syncTagLineEdit.textChanged,
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
            )
        ]

        for args in global_button_args:
            setup_restore_button(*args)

        signal_lists = list(global_signals.values()) \
                       + list(self.leech_form.get_signals().values()) \
                       + list(self.unleech_form.get_signals().values())

        for signals in signal_lists:
            self.append_apply_signals(signals)

        leech_conf = self.config[Config.LEECH_ACTIONS]
        unleech_conf = self.config[Config.UN_LEECH_ACTIONS]
        reverse_conf = self.config[Config.REVERSE_OPTIONS]

        self.leech_form.setup_restorables(leech_conf, Config.DEFAULT_CONFIG[Config.LEECH_ACTIONS])
        self.unleech_form.setup_restorables(unleech_conf, Config.DEFAULT_CONFIG[Config.UN_LEECH_ACTIONS])
        self.reverse_form.setup_restorables(reverse_conf, Config.DEFAULT_CONFIG[Config.REVERSE_OPTIONS])

    def append_apply_signals(self, signals: list[pyqtBoundSignal]):
        for signal in signals:
            signal.connect(lambda *args: self.apply_button.setEnabled(True))

    def apply(self):
        self._write()
        bind_actions()
        mw.reset()
        self.apply_button.setEnabled(False)

    def restore_defaults(self):
        self.config = Config.DEFAULT_CONFIG.copy()
        self._load()
        [button.setVisible(False) for button in self.restore_buttons]

    def accept(self) -> None:
        self.apply()
        super().accept()

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
        print(f' write_toolkit_conf: {sync_tag_conf}')
        sync_tag_conf[Config.SYNC_TAG_ENABLED] = self.ui.syncTagCheckbox.isChecked()
        sync_tag_conf[Config.SYNC_TAG_TEXT] = self.ui.syncTagLineEdit.text()

    def _load(self):
        self.ui.toolsOptionsCheckBox.setChecked(self.config[Config.TOOLBAR_ENABLED])
        self.ui.syncUpdateCheckbox.setChecked(self.config[Config.SYNC_ENABLED])

        self.load_marker(self.config[Config.MARKER_OPTIONS])
        self.load_leech_button(self.config[Config.BUTTON_OPTIONS])
        self.load_sync_tag(self.config[Config.SYNC_TAG_OPTIONS])

        self.leech_form.load_ui(self.config[Config.LEECH_ACTIONS])
        self.unleech_form.load_ui(self.config[Config.UN_LEECH_ACTIONS])
        self.reverse_form.load_ui(self.config[Config.REVERSE_OPTIONS])

    def _write(self):
        self.config[Config.TOOLBAR_ENABLED] = self.ui.toolsOptionsCheckBox.isChecked()
        self.config[Config.SYNC_ENABLED] = self.ui.syncUpdateCheckbox.isChecked()

        self.write_marker(self.config[Config.MARKER_OPTIONS])
        self.write_button(self.config[Config.BUTTON_OPTIONS])
        self.write_sync_tag(self.config[Config.SYNC_TAG_OPTIONS])

        self.leech_form.write_all(self.config[Config.LEECH_ACTIONS])
        self.unleech_form.write_all(self.config[Config.UN_LEECH_ACTIONS])
        self.reverse_form.write(self.config[Config.REVERSE_OPTIONS])

        # Save config
        self.manager.save_config()


class ReverseWidget(QWidget):
    def __init__(self, flags, restore_buttons: list = None):
        super().__init__(parent=None, flags=flags)
        self.ui = Ui_ReverseForm()
        self.ui.setupUi(self)

        def toggle_threshold(checked: bool):
            self.ui.reverseThresholdSpinbox.setEnabled(checked)

        self.ui.useLeechThresholdCheckbox.stateChanged.connect(lambda checked: toggle_threshold(not checked))

        append_restore_button(self.ui.reverseGroup)
        restore_buttons.append(self.ui.reverseGroup.default_button) if restore_buttons else None

    def get_signals(self):
        return [
            self.ui.reverseGroup.clicked,
            self.ui.useLeechThresholdCheckbox.stateChanged,
            self.ui.reverseMethodDropdown.currentIndexChanged,
            self.ui.reverseThresholdSpinbox.valueChanged,
            self.ui.consAnswerSpinbox.valueChanged,
        ]

    def load_ui(self, reverse_config: dict):
        self.ui.reverseGroup.setChecked(reverse_config[Config.REVERSE_ENABLED])
        self.ui.useLeechThresholdCheckbox.setChecked(reverse_config[Config.REVERSE_USE_LEECH_THRESHOLD])
        self.ui.reverseMethodDropdown.setCurrentIndex(reverse_config[Config.REVERSE_METHOD])
        self.ui.reverseThresholdSpinbox.setValue(reverse_config[Config.REVERSE_THRESHOLD])
        self.ui.consAnswerSpinbox.setValue(reverse_config[Config.REVERSE_CONS_ANS])

    def setup_restorables(self, reverse_conf: dict, default_conf: dict = None):
        setup_restore_button(
            self.ui.reverseGroup.default_button,
            self.get_signals(),
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
        super().__init__(parent, mw.windowFlags())
        self.ui = Ui_ActionsForm()
        self.ui.setupUi(ActionsForm=self)

        self.actions_type = actions_type

        self.dids = [int(name_id.id) for name_id in mw.col.decks.all_names_and_ids()] if not dids else dids

        if self.actions_type == Config.LEECH_ACTIONS:
            self.ui.expandoButton.setText(String.LEECH_ACTIONS)
        if self.actions_type == Config.UN_LEECH_ACTIONS:
            self.ui.expandoButton.setText(String.UN_LEECH_ACTIONS)

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

        flag_manager = aqt.flags.FlagManager(mw)
        for index in range(1, self.ui.flagDropdown.count()):
            flag = flag_manager.get_flag(index)
            pixmap = QPixmap(flag.icon.path)
            mask = pixmap.createMaskFromColor(QColor('black'), aqt.qt.Qt.MaskOutColor)
            pixmap.fill(QColor(flag.icon.current_color(mw.pm.night_mode())))
            pixmap.setMask(mask)
            self.ui.flagDropdown.setItemIcon(index, QIcon(pixmap))
            self.ui.flagDropdown.setItemText(index, f'{flag.label}')

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
            note_dict = mw.col.models.get(NotetypeId(mid))
            field_name = mw.col.models.field_names(note_dict)[item_data[0]] if note_dict else String.NOTE_NOT_FOUND

            add_edit_field(self.ui.editFieldsList, mid, field_name, item_data[1], item_data[2], item_data[3])

        _redraw_list(self.ui.editFieldsList, max_fields_height)

    # DECK MOVE
    def load_move_deck(self, action_conf: dict):
        self.ui.deckMoveGroup.setChecked(action_conf[Action.ENABLED])
        deck_names = [dnid.name for dnid in mw.col.decks.all_names_and_ids()]
        deck_name = mw.col.decks.name_if_exists(action_conf[Action.INPUT])
        self.deck_completer.set_list(deck_names)
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
                note = mw.col.models.get(NotetypeId(int(mid)))
                field_name = mw.col.models.field_names(note)[field_ord]
                add_excluded_field(self.ui.queueExcludedFieldList, mid, field_name)
        self.ui.queueExcludedFieldList.sortItems()
        _redraw_list(self.ui.queueExcludedFieldList)

        self.ui.queueSiblingCheckbox.setChecked(queue_input[QueueAction.NEAR_SIBLING])

    def update_queue_info(self, use_current_deck=False):
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
        self.write_move_deck(actions_config[Action.MOVE_DECK])
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

    def write_move_deck(self, actions_config: dict):
        actions_config[Action.ENABLED] = self.ui.deckMoveGroup.isChecked()
        stored_did = self.ui.deckMoveLine.text()
        actions_config[Action.INPUT] = mw.col.decks.id(stored_did) if stored_did else ''

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

    def toggle_expando(self, button: aqt.qt.QToolButton, toggle: bool = None):
        toggle = not self.ui.actionsFrame.isVisible() if toggle is None else toggle
        button.setArrowType(arrow_types[toggle])
        if button == self.ui.expandoButton:
            self.ui.actionsFrame.setVisible(toggle)


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
        super().__init__(flags=mw.windowFlags())
        self.list_widget = list_widget
        self.mid = mid
        self.widget = Ui_ExcludedFieldItem()
        self.widget.setupUi(ExcludedFieldItem=self)
        self.widget.fieldLabel.setText(field_name)
        self.widget.removeButton.setIcon(QIcon(f'{Path(__file__).parent.resolve()}\\{REMOVE_ICON_PATH}'))
        self.widget.fieldLabel.setToolTip(f'{mw.col.models.get(NoteId(self.mid))["name"]}')

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
        fields_names = mw.col.models.field_names(mw.col.models.get(self.mid))
        return {f'{self.mid}': fields_names.index(self.widget.fieldLabel.text())}

    class ExcludedFieldListItem(QListWidgetItem):
        def __lt__(self, other):
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
    NoteItem used for the field edit list.
        :param edit_list:
        :param mid:
        :param field_name:
        :param method_idx:
        :param repl:
        :param text:
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
        self.widget.methodDropdown.currentIndexChanged.connect(self.update_method)
        self.widget.fieldButtonLabel.setMenu(QMenu(self.widget.fieldButtonLabel))
        self.widget.fieldButtonLabel.menu().triggered.connect(
            lambda action: _handle_new_field(self.list_widget, action, self.set_model)
        )
        _fill_menu_fields(self.widget.fieldButtonLabel)

        self._load()

    def set_model(self, list_widget, mid: int, field_name: str):
        self.list_widget = list_widget
        self.mid = mid
        self.field_name = field_name
        self._load()

    def _load(self):
        self.note_type_dict = mw.col.models.get(NotetypeId(self.mid))
        self.model_name = self.note_type_dict["name"] if self.note_type_dict else ''
        self.widget.fieldButtonLabel.setToolTip(self.model_name)
        self.widget.fieldButtonLabel.setText(self.field_name)
        self.update_method(self.method_idx)
        self.widget.replaceEdit.setText(self._repl)
        self.widget.inputEdit.setText(self._text)

    def update_method(self, method_idx: int):
        self.method_idx = method_idx
        if self.method_idx >= 0:
            replace_selected = self.method_idx in (EditAction.REPLACE_METHOD, EditAction.REGEX_METHOD)
            self.widget.methodDropdown.setCurrentIndex(self.method_idx)
            self.widget.replaceEdit.setVisible(replace_selected)
            self.widget.inputEdit.setPlaceholderText(String.REPLACE_WITH if replace_selected else String.OUTPUT_TEXT)

    def get_field_edit_dict(self):
        if self.note_type_dict:
            fields_names = mw.col.models.field_names(self.note_type_dict)
            field_idx = fields_names.index(self.widget.fieldButtonLabel.text())
        else:
            field_idx = 0
        method_idx = self.widget.methodDropdown.currentIndex()
        repl, text = self.widget.replaceEdit.text(), self.widget.inputEdit.text()

        return {f'{self.mid}': [field_idx, method_idx, repl, text]}
