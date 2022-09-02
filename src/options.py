"""
MIT License: Copyright (c) 2022 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
Full license text available in "LICENSE" file packaged with the program.
"""
from pathlib import Path

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
)

from .config import LeechToolkitConfigManager
from .consts import String, Config, Action, Macro, REMOVE_ICON_PATH, EditAction, RescheduleAction, QueueAction, \
    RESTORE_ICON_PATH
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


def redraw_list(fields_list: QListWidget, max_height=256):
    data_height = fields_list.sizeHintForRow(0) * fields_list.count()
    fields_list.setFixedHeight(data_height if data_height < max_height else fields_list.maximumHeight())
    fields_list.setMaximumWidth(fields_list.parent().maximumWidth())
    fields_list.setVisible(fields_list.count() != 0)
    # Emit signal for change updates
    fields_list.setCurrentRow(0)


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
            if action.text() == String.TOOLBAR_OPTIONS:
                mw.form.menuTools.removeAction(action)


def _bind_config_options():
    mw.addonManager.setConfigAction(__name__, on_options_called)


class OptionsDialog(QDialog):

    def __init__(self, manager: LeechToolkitConfigManager):
        super().__init__(flags=mw.windowFlags())
        self.manager = manager
        self.config = manager.config
        self.ui = Ui_OptionsDialog()
        self.ui.setupUi(OptionsDialog=self)

        self.reverse_form = ReverseWidget(mw.windowFlags())
        self.ui.optionsScrollLayout.addWidget(self.reverse_form.ui.reverseGroup)

        self.leech_actions = ActionsWidget(Config.LEECH_ACTIONS)
        self.ui.actionsScrollLayout.addWidget(self.leech_actions)

        self.reverse_actions = ActionsWidget(Config.UN_LEECH_ACTIONS)
        self.ui.actionsScrollLayout.addWidget(self.reverse_actions)

        self._load()

        # Just in case
        self.ui.tabWidget.setCurrentIndex(0)

    def _load(self):
        self.ui.toolsOptionsCheckBox.setChecked(self.config[Config.TOOLBAR_ENABLED])

        self.ui.showMarkerChecbkbox.setChecked(self.config[Config.SHOW_LEECH_MARKER])
        self.ui.almostCheckbox.setChecked(self.config[Config.USE_ALMOST_MARKER])
        self.ui.almostPosDropdown.setCurrentIndex(self.config[Config.MARKER_POSITION])
        self.ui.almostBackCheckbox.setChecked(self.config[Config.ONLY_SHOW_BACK_MARKER])

        self.ui.browseButtonCheckbox.setChecked(self.config[Config.SHOW_BROWSE_BUTTON])
        self.ui.browseButtonBrowserCheckbox.setChecked(self.config[Config.BROWSE_BUTTON_ON_BROWSER])
        self.ui.browseButtonOverviewCheckbox.setChecked(self.config[Config.BROWSE_BUTTON_ON_OVERVIEW])

        self.leech_actions.load(self.config[Config.LEECH_ACTIONS])
        self.reverse_actions.load(self.config[Config.UN_LEECH_ACTIONS])
        self.reverse_form.load(self.config[Config.REVERSE_OPTIONS])

    def _save(self):
        self.config[Config.TOOLBAR_ENABLED] = self.ui.toolsOptionsCheckBox.isChecked()

        self.config[Config.SHOW_LEECH_MARKER] = self.ui.showMarkerChecbkbox.isChecked()
        self.config[Config.USE_ALMOST_MARKER] = self.ui.almostCheckbox.isChecked()
        self.config[Config.MARKER_POSITION] = self.ui.almostPosDropdown.currentIndex()
        self.config[Config.ONLY_SHOW_BACK_MARKER] = self.ui.almostBackCheckbox.isChecked()

        self.config[Config.SHOW_BROWSE_BUTTON] = self.ui.browseButtonCheckbox.isChecked()
        self.config[Config.BROWSE_BUTTON_ON_BROWSER] = self.ui.browseButtonBrowserCheckbox.isChecked()
        self.config[Config.BROWSE_BUTTON_ON_OVERVIEW] = self.ui.browseButtonOverviewCheckbox.isChecked()

        self.leech_actions.save_all(self.config[Config.LEECH_ACTIONS])
        self.reverse_actions.save_all(self.config[Config.UN_LEECH_ACTIONS])
        self.reverse_form.save(self.config[Config.REVERSE_OPTIONS])

        # Write
        self.manager.write_config()

    def accept(self) -> None:
        self._save()
        super().accept()
        bind_actions()
        mw.reset()


class ReverseWidget(QWidget):
    def __init__(self, flags):
        super().__init__(flags=flags)
        self.ui = Ui_ReverseForm()
        self.ui.setupUi(self)

        def toggle_threshold(checked: bool):
            self.ui.reverseThresholdSpinbox.setEnabled(checked)

        self.ui.useLeechThresholdCheckbox.stateChanged.connect(lambda checked: toggle_threshold(not checked))

    def load(self, reverse_config: dict):
        self.ui.reverseCheckbox.setChecked(reverse_config[Config.REVERSE_ENABLED])
        self.ui.useLeechThresholdCheckbox.setChecked(reverse_config[Config.REVERSE_USE_LEECH_THRESHOLD])
        self.ui.reverseMethodDropdown.setCurrentIndex(reverse_config[Config.REVERSE_METHOD])
        self.ui.reverseThresholdSpinbox.setValue(reverse_config[Config.REVERSE_THRESHOLD])
        self.ui.consAnswerSpinbox.setValue(reverse_config[Config.REVERSE_CONS_ANS])

    def save(self, reverse_config: dict):
        reverse_enabled = self.ui.reverseCheckbox.isChecked()
        reverse_config[Config.REVERSE_ENABLED] = reverse_enabled
        reverse_config[Config.REVERSE_METHOD] = self.ui.reverseMethodDropdown.currentIndex()
        reverse_config[Config.REVERSE_USE_LEECH_THRESHOLD] = self.ui.useLeechThresholdCheckbox.isChecked()
        reverse_config[Config.REVERSE_THRESHOLD] = self.ui.reverseThresholdSpinbox.value()
        reverse_config[Config.REVERSE_CONS_ANS] = self.ui.consAnswerSpinbox.value()


def _fill_menu_fields(add_button: aqt.qt.QToolButton):
    menu: QMenu = add_button.menu()
    menu.clear()

    for note_type in mw.col.models.all():
        sub_menu = menu.addMenu(f'{note_type["name"]}')

        for field in mw.col.models.field_names(note_type):
            action = QAction(f'{field}', add_button)
            action.setData(note_type['id'])
            sub_menu.addAction(action)


class ActionsWidget(QWidget):
    def __init__(self, actions_type: str, parent=None, expanded=True):
        super().__init__(parent, mw.windowFlags())
        self.ui = Ui_ActionsForm()
        self.ui.setupUi(ActionsForm=self)
        self.actions_type = actions_type

        if self.actions_type == Config.LEECH_ACTIONS:
            self.ui.expandoButton.setText(String.LEECH_ACTIONS)
        if self.actions_type == Config.UN_LEECH_ACTIONS:
            self.ui.expandoButton.setText(String.LEECH_REVERSE_ACTIONS)

        self.ui.editFieldsList.setStyleSheet('#editFieldsList {background-color: transparent;}')

        self.ui.queueExcludedFieldList.setStyleSheet('#editFieldsList {background-color: transparent;}')
        self.ui.queueLabelBottom.setGraphicsEffect(QGraphicsOpacityEffect())
        self.ui.queueLabelTop.setGraphicsEffect(QGraphicsOpacityEffect())

        self.ui.queueFromSpinbox.dropdown = self.ui.queueFromDropdown
        self.ui.queueToSpinbox.dropdown = self.ui.queueToDropdown
        self.ui.queueFromDropdown.currentIndexChanged.connect(lambda _: self.ui.queueFromSpinbox.refresh())
        self.ui.queueToDropdown.currentIndexChanged.connect(lambda _: self.ui.queueToSpinbox.refresh())

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

        self.ui.queueExcludeTextEdit.textChanged.connect(lambda: update_text_size(self.ui.queueExcludeTextEdit))

        self.ui.queueAddFieldButton.setMenu(QMenu(self.ui.queueAddFieldButton))
        self.ui.queueAddFieldButton.menu().triggered.connect(
            lambda action: _handle_new_field(self.ui.queueExcludedFieldList, action, add_excluded_field)
        )

        self.ui.editAddFieldButton.setMenu(QMenu(self.ui.editAddFieldButton))
        self.ui.editAddFieldButton.menu().triggered.connect(
            lambda action: _handle_new_field(self.ui.editFieldsList, action, add_edit_field)
        )

        self.ui.expandoWidget.set_click_function(lambda: self.toggle_expando(self.ui.expandoButton))
        self.ui.expandoButton.pressed.connect(lambda: self.toggle_expando(self.ui.expandoButton))
        self.toggle_expando(self.ui.expandoButton, expanded)

    def load_default_buttons(self, actions_meta: dict, default_meta: dict):

        def build_default_button(action: str, signals: list[aqt.qt.pyqtBoundSignal], callback, anchor_widget):
            button = aqt.qt.QPushButton(anchor_widget)
            button.setMaximumSize(QSize(16, 16))
            button.setFlat(True)
            button.setToolTip(String.RESTORE_DEFAULT_SETTING)
            button.setIcon(QIcon(f'{Path(__file__).parent.resolve()}\\{RESTORE_ICON_PATH}'))

            size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            size_policy.setHorizontalStretch(0)
            size_policy.setVerticalStretch(0)
            size_policy.setHeightForWidth(button.sizePolicy().hasHeightForWidth())

            button.setSizePolicy(size_policy)

            widget_index = self.ui.actionsFrame.layout().indexOf(anchor_widget)
            widget_row = self.ui.actionsFrame.layout().getItemPosition(widget_index)[0]
            self.ui.actionsFrame.layout().addWidget(button, widget_row, 4)

            for signal in signals:
                def refresh_default_button(*args):
                    callback(actions_meta) if callback else None
                    button.setVisible(actions_meta[action] != default_meta[action])

                signal.connect(refresh_default_button)

            # Initial update
            button.setVisible(actions_meta[action] != default_meta[action])
            print(f'{action}')
            print(f'    actions_meta: {actions_meta[action]}\n      default_meta: {default_meta[action]}')

            return button

        flag_signals = [
            self.ui.flagCheckbox.stateChanged,
            self.ui.flagDropdown.currentTextChanged,
        ]
        build_default_button(Action.FLAG, flag_signals, self.save_flag, self.ui.flagCheckbox)

        suspend_signals = [
            self.ui.suspendCheckbox.stateChanged,
            self.ui.suspendOnButton.toggled,
            self.ui.suspendOffButton.toggled,
        ]
        build_default_button(Action.SUSPEND, suspend_signals, self.save_suspend, self.ui.suspendCheckbox)

        add_tags_signals = [
            self.ui.addTagsCheckbox.stateChanged,
            self.ui.addTagsLine.textChanged,
        ]
        build_default_button(Action.ADD_TAGS, add_tags_signals, self.save_add_tags, self.ui.addTagsCheckbox)

        remove_tags_signals = [
            self.ui.removeTagsCheckbox.stateChanged,
            self.ui.removeTagsLine.textChanged,
        ]
        build_default_button(Action.REMOVE_TAGS, remove_tags_signals, self.save_remove_tags, self.ui.removeTagsCheckbox)

        forget_signals = [
            self.ui.forgetCheckbox.stateChanged,
            self.ui.forgetOnRadio.toggled,
            self.ui.forgetOffRadio.toggled,
            self.ui.forgetResetCheckbox.stateChanged,
            self.ui.forgetRestorePosCheckbox.stateChanged,
        ]
        build_default_button(Action.FORGET, forget_signals, self.save_forget, self.ui.forgetCheckbox)

        edit_fields_signals = [
            self.ui.editFieldsCheckbox.stateChanged,
            self.ui.editFieldsList.currentRowChanged,
        ]
        build_default_button(Action.EDIT_FIELDS, edit_fields_signals, self.save_edit_fields, self.ui.editFieldsCheckbox)

        deck_move_signals = [
            self.ui.deckMoveCheckbox.stateChanged,
            self.ui.deckMoveLine.textChanged,
        ]
        build_default_button(Action.MOVE_TO_DECK, deck_move_signals, self.save_deck_move, self.ui.deckMoveCheckbox)

        reschedule_signals = [
            self.ui.rescheduleCheckbox.stateChanged,
            self.ui.rescheduleFromDays.valueChanged,
            self.ui.rescheduleToDays.valueChanged,
            self.ui.rescheduleResetCheckbox.stateChanged,
        ]
        build_default_button(Action.RESCHEDULE, reschedule_signals, self.save_reschedule, self.ui.rescheduleCheckbox)

        queue_signals = [
            self.ui.queueCheckbox.stateChanged,
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
        ]
        build_default_button(Action.ADD_TO_QUEUE, queue_signals, self.save_add_to_queue, self.ui.queueCheckbox)

    def load(self, actions_config: dict, default_config: dict = None):
        default_config = default_config if default_config else Config.DEFAULT_CONFIG[self.actions_type]

        # FLAG
        def load_flag():
            self.ui.flagCheckbox.setChecked(actions_config[Action.FLAG][Action.ENABLED])
            self.ui.flagDropdown.setCurrentIndex(actions_config[Action.FLAG][Action.INPUT])

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
        def load_suspend():
            self.ui.suspendCheckbox.setChecked(actions_config[Action.SUSPEND][Action.ENABLED])
            self.ui.suspendOnButton.setChecked(actions_config[Action.SUSPEND][Action.INPUT])
            self.ui.suspendOffButton.setChecked(not actions_config[Action.SUSPEND][Action.INPUT])

        # TAGS
        tag_suggestions = mw.col.weakref().tags.all() + list(Macro.MACROS)

        # ADD TAGS
        def load_add_tags():
            self.add_completer.set_list([suggestion for suggestion in tag_suggestions if suggestion != Macro.REGEX])
            self.ui.addTagsCheckbox.setChecked(actions_config[Action.ADD_TAGS][Action.ENABLED])
            self.ui.addTagsLine.setText(actions_config[Action.ADD_TAGS][Action.INPUT])
            self.ui.addTagsLine.setCompleter(self.add_completer)

        # REMOVE TAGS
        def load_remove_tags():
            self.remove_completer.set_list(tag_suggestions)
            self.ui.removeTagsCheckbox.setChecked(actions_config[Action.REMOVE_TAGS][Action.ENABLED])
            self.ui.removeTagsLine.setText(actions_config[Action.REMOVE_TAGS][Action.INPUT])
            self.ui.removeTagsLine.setCompleter(self.remove_completer)

        # FORGET
        def load_forget():
            self.ui.forgetCheckbox.setChecked(actions_config[Action.FORGET][Action.ENABLED])
            self.ui.forgetOnRadio.setChecked(actions_config[Action.FORGET][Action.INPUT][0])
            self.ui.forgetOffRadio.setChecked(not actions_config[Action.FORGET][Action.INPUT][0])
            self.ui.forgetRestorePosCheckbox.setChecked(actions_config[Action.FORGET][Action.INPUT][1])
            self.ui.forgetResetCheckbox.setChecked(actions_config[Action.FORGET][Action.INPUT][2])

        # EDIT FIELD
        def load_edit_field():
            self.ui.editFieldsCheckbox.setChecked(actions_config[Action.EDIT_FIELDS][Action.ENABLED])
            for field_item in actions_config[Action.EDIT_FIELDS][Action.INPUT]:
                mid, item_data = list(field_item.items())[0]

                note_dict = mw.col.models.get(NotetypeId(mid))
                field_name = mw.col.models.field_names(note_dict)[item_data[0]] if note_dict else String.NOTE_NOT_FOUND

                add_edit_field(self.ui.editFieldsList, mid, field_name, item_data[1], item_data[2], item_data[3])

            redraw_list(self.ui.editFieldsList, max_fields_height)

            _fill_menu_fields(self.ui.editAddFieldButton)

        # DECK MOVE
        def load_deck_move():
            self.ui.deckMoveCheckbox.setChecked(actions_config[Action.MOVE_TO_DECK][Action.ENABLED])
            deck_names = [dnid.name for dnid in mw.col.decks.all_names_and_ids()]
            deck_name = mw.col.decks.name_if_exists(actions_config[Action.MOVE_TO_DECK][Action.INPUT])
            self.deck_completer.set_list(deck_names)
            self.ui.deckMoveLine.setCompleter(self.deck_completer)
            self.ui.deckMoveLine.setText(deck_name)

        # RESCHEDULE
        def load_reschedule():
            reschedule_input = actions_config[Action.RESCHEDULE][Action.INPUT]
            self.ui.rescheduleCheckbox.setChecked(actions_config[Action.RESCHEDULE][Action.ENABLED])
            self.ui.rescheduleFromDays.setValue(reschedule_input[RescheduleAction.FROM])
            self.ui.rescheduleToDays.setValue(reschedule_input[RescheduleAction.TO])
            self.ui.rescheduleResetCheckbox.setChecked(reschedule_input[RescheduleAction.RESET])

        # ADD TO QUEUE
        def load_queue():
            queue_input = actions_config[Action.ADD_TO_QUEUE][Action.INPUT]
            self.ui.queueCheckbox.setChecked(actions_config[Action.ADD_TO_QUEUE][Action.ENABLED])
            self.ui.queueFromDropdown.setCurrentIndex(queue_input[QueueAction.FROM_INDEX])
            self.ui.queueToDropdown.setCurrentIndex(queue_input[QueueAction.TO_INDEX])
            self.ui.queueFromSpinbox.setValue(queue_input[QueueAction.FROM_VAL])
            self.ui.queueToSpinbox.setValue(queue_input[QueueAction.TO_VAL])
            top, bottom = mw.col.db.first(
                f"select min(due), max(due) from cards where type={CARD_TYPE_NEW} and odid=0"
            )
            self.ui.queueLabelTopPos.setText(str(top))
            self.ui.queueLabelBottomPos.setText(str(bottom))
            self.ui.queueSimilarCheckbox.setChecked(queue_input[QueueAction.NEAR_SIMILAR])
            self.ui.queueSiblingCheckbox.setChecked(queue_input[QueueAction.NEAR_SIBLING])
            self.ui.queueIncludeFieldsCheckbox.setChecked(queue_input[QueueAction.INCLUSIVE_FIELDS])

            for note_dict in queue_input[QueueAction.FILTERED_FIELDS]:
                mid = list(note_dict)[0]
                for field_ord in list(note_dict.values()):
                    note = mw.col.models.get(NotetypeId(int(mid)))
                    field_name = mw.col.models.field_names(note)[field_ord]
                    add_excluded_field(self.ui.queueExcludedFieldList, mid, field_name)

            self.ui.queueExcludedFieldList.sortItems()
            redraw_list(self.ui.queueExcludedFieldList)

            _fill_menu_fields(self.ui.queueAddFieldButton)

            self.ui.queueExcludeTextEdit.setText(queue_input[QueueAction.EXCLUDED_TEXT])
            self.ui.queueRatioSlider.setValue(queue_input[QueueAction.SIMILAR_RATIO] * 100)

        # A little easier to read/debug
        load_flag()
        load_suspend()
        load_add_tags()
        load_remove_tags()
        load_forget()
        load_edit_field()
        load_deck_move()
        load_reschedule()
        load_queue()

        self.load_default_buttons(actions_config, default_config)

    def save_all(self, actions_config: dict):
        # A little easier to read/debug
        self.save_flag(actions_config)
        self.save_suspend(actions_config)
        self.save_add_tags(actions_config)
        self.save_remove_tags(actions_config)
        self.save_forget(actions_config)
        self.save_edit_fields(actions_config)
        self.save_deck_move(actions_config)
        self.save_reschedule(actions_config)
        self.save_add_to_queue(actions_config)

    def save_flag(self, actions_config: dict):
        actions_config[Action.FLAG][Action.ENABLED] = self.ui.flagCheckbox.isChecked()
        actions_config[Action.FLAG][Action.INPUT] = self.ui.flagDropdown.currentIndex()

    def save_suspend(self, actions_config: dict):
        actions_config[Action.SUSPEND][Action.ENABLED] = self.ui.suspendCheckbox.isChecked()
        actions_config[Action.SUSPEND][Action.INPUT] = self.ui.suspendOnButton.isChecked()

    def save_add_tags(self, actions_config: dict):
        actions_config[Action.ADD_TAGS][Action.ENABLED] = self.ui.addTagsCheckbox.isChecked()
        actions_config[Action.ADD_TAGS][Action.INPUT] = \
            mw.col.tags.join(mw.col.tags.split(self.ui.addTagsLine.text()))

    def save_remove_tags(self, actions_config: dict):
        actions_config[Action.REMOVE_TAGS][Action.ENABLED] = self.ui.removeTagsCheckbox.isChecked()
        actions_config[Action.REMOVE_TAGS][Action.INPUT] = \
            mw.col.tags.join(mw.col.tags.split(self.ui.removeTagsLine.text()))

    def save_forget(self, actions_config: dict):
        actions_config[Action.FORGET][Action.ENABLED] = self.ui.forgetCheckbox.isChecked()
        actions_config[Action.FORGET][Action.INPUT][0] = self.ui.forgetOnRadio.isChecked()
        actions_config[Action.FORGET][Action.INPUT][1] = self.ui.forgetRestorePosCheckbox.isChecked()
        actions_config[Action.FORGET][Action.INPUT][2] = self.ui.forgetResetCheckbox.isChecked()

    def save_edit_fields(self, actions_config: dict):
        actions_config[Action.EDIT_FIELDS][Action.ENABLED] = self.ui.editFieldsCheckbox.isChecked()
        edit_input: list = actions_config[Action.EDIT_FIELDS][Action.INPUT]

        edit_input.clear()
        for i in range(self.ui.editFieldsList.count()):
            item = EditFieldItem.from_list_widget(self.ui.editFieldsList, self.ui.editFieldsList.item(i))
            edit_input.append(item.get_field_edit_dict()) if item is not None else None

    def save_deck_move(self, actions_config: dict):
        actions_config[Action.MOVE_TO_DECK][Action.ENABLED] = self.ui.deckMoveCheckbox.isChecked()
        stored_did = self.ui.deckMoveLine.text()
        actions_config[Action.MOVE_TO_DECK][Action.INPUT] = mw.col.decks.id(stored_did) if stored_did else ''

    def save_reschedule(self, actions_config: dict):
        actions_config[Action.RESCHEDULE][Action.ENABLED] = self.ui.rescheduleCheckbox.isChecked()
        reschedule_input = actions_config[Action.RESCHEDULE][Action.INPUT]
        reschedule_input[RescheduleAction.FROM] = self.ui.rescheduleFromDays.value()
        reschedule_input[RescheduleAction.TO] = self.ui.rescheduleToDays.value()
        reschedule_input[RescheduleAction.RESET] = self.ui.rescheduleResetCheckbox.isChecked()

    def save_add_to_queue(self, actions_config: dict):
        actions_config[Action.ADD_TO_QUEUE][Action.ENABLED] = self.ui.queueCheckbox.isChecked()

        queue_input = actions_config[Action.ADD_TO_QUEUE][Action.INPUT]
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


def _add_list_item(list_widget: QListWidget, list_item: QListWidgetItem, item_widget: QWidget):
    list_item.setSizeHint(item_widget.sizeHint())
    list_item.setFlags(Qt.NoItemFlags)

    list_widget.addItem(list_item)
    list_widget.setItemWidget(list_item, item_widget)


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


def _handle_new_field(list_widget: QListWidget, action: QAction, callback):
    callback(list_widget, action.data(), action.text())
    redraw_list(list_widget)


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
                    redraw_list(self.list_widget)

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
            text: str
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
                    redraw_list(self.list_widget)

        self.widget.removeButton.clicked.connect(remove_self)
        self.widget.methodDropdown.currentIndexChanged.connect(self.update_method)
        self.widget.fieldButtonLabel.menu().triggered.connect(
            lambda action: _handle_new_field(self.list_widget, action, self.set_model)
        )

        self._load()

    def set_model(self, list_widget, mid: int, field_name: str):
        self.list_widget = list_widget
        self.mid = mid
        self.field_name = field_name
        self._load()

    def _load(self):
        self.note_type_dict = mw.col.models.get(NotetypeId(self.mid))
        self.model_name = self.note_type_dict["name"] if self.note_type_dict else ''

        _fill_menu_fields(self.widget.fieldButtonLabel)
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
