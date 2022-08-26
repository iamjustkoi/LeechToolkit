"""
MIT License: Copyright (c) 2022 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
Full license text available in "LICENSE" file packaged with the program.
"""
import re
from pathlib import Path

import aqt.flags
from anki.consts import CARD_TYPE_NEW
from anki.models import NotetypeId
from anki.notes import NoteId
from aqt import mw
from aqt.models import Models
from aqt.qt import (
    Qt,
    QAction,
    QDialog,
    QIcon,
    QPixmap,
    QColor,
    QCompleter,
    QDialogButtonBox,
    qconnect,
    QWidget,
    QMenu,
    QListWidgetItem,
    QListWidget,
    QGraphicsOpacityEffect,
    QTextEdit,
)

from . import reviewer
from .config import LeechToolkitConfigManager
from .consts import String, Config, Action, Macro, REMOVE_ICON_PATH, EditAction, RescheduleAction, QueueAction
from ..res.ui.actions_widget import Ui_ActionsWidget
from ..res.ui.edit_field_item import Ui_EditFieldItem
from ..res.ui.exclude_field_item import Ui_ExcludedFieldItem
from ..res.ui.options_dialog import Ui_OptionsDialog
from ..res.ui.reverse_form import Ui_ReverseForm

max_fields_height = 572
max_queue_height = 256
arrow_types = [Qt.RightArrow, Qt.DownArrow]


def bind_actions():
    _bind_config_options()
    _bind_tools_options()


def on_options_called(result=False):
    options = OptionsDialog(LeechToolkitConfigManager(mw))
    options.exec()


def get_colored_icon(path, color):
    icon = QIcon(path)
    pixmap = icon.pixmap()
    pixmap.fill(color)
    return QIcon(pixmap)


def redraw_list(fields_list: QListWidget, max_height=256):
    data_height = fields_list.sizeHintForRow(0) * fields_list.count()
    fields_list.setFixedHeight(data_height if data_height < max_height else fields_list.maximumHeight())
    fields_list.setMaximumWidth(fields_list.parent().maximumWidth())
    fields_list.setVisible(fields_list.count() != 0)


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


class CustomCompleter(QCompleter):

    def __init__(self, parent_line_edit: aqt.qt.QLineEdit) -> None:
        QCompleter.__init__(self, aqt.qt.QStringListModel(), parent_line_edit)

        self.current_data: list[str] = []
        self.cursor_index: int or None = None
        self.cursor_item_pos: int or None = None

        self.line_edit = parent_line_edit

        self.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.setFilterMode(Qt.MatchContains)
        self.setCompletionPrefix(' ')

        def focus_event(event):
            default_focus_evt(event)
            if len(self.line_edit.text()) <= 0:
                self.complete()

        def release_event(event):
            default_release_evt(event)
            if len(self.line_edit.text()) <= 0:
                self.complete()

        default_focus_evt = self.line_edit.focusInEvent
        default_release_evt = self.line_edit.mouseReleaseEvent
        self.line_edit.focusInEvent = focus_event
        self.line_edit.mouseReleaseEvent = release_event

    def set_list(self, data: list[str]):
        self.setModel(aqt.qt.QStringListModel(data))

    def get_path_pos(self):
        return sum([len(item) for item in self.current_data[:self.cursor_index]])

    def splitPath(self, path: str) -> list[str]:
        """
    Splits the line edit's path based on a variety of filters, updates the current cursor position variables,
    and outputs a list with a single item to use as
    auto-completion suggestions.
        :param path: the current path to split/filter
        :return: a list containing a single string to use as a reference for completer suggestions
        """
        formatted_path = re.sub('  +', ' ', path)
        stripped_path = formatted_path.strip()
        cursor_pos = self.line_edit.cursorPosition()
        self.cursor_index = stripped_path.count(' ', 0, cursor_pos)
        self.current_data = formatted_path.strip().split(' ')
        self.cursor_item_pos = cursor_pos - self.get_path_pos()

        if formatted_path.endswith(' ') and cursor_pos >= len(formatted_path):
            self.current_data.append('')
            self.cursor_index += 1
            return ['']

        if cursor_pos == 0:
            self.current_data.insert(0, '')
            self.cursor_index = 0
            return ['']

        item_macro_pos = self.current_data[self.cursor_index].rfind('%', 1)
        if self.cursor_item_pos > item_macro_pos > 0:
            return [self.current_data[self.cursor_index][item_macro_pos:]]

        return [self.current_data[self.cursor_index]]

    def pathFromIndex(self, index: aqt.qt.QModelIndex) -> str:
        """
    Retrieves the line edit's path from the given index data.
        :param index: QModelIndex used as a reference for what to insert
        :return: the string output of the given path result
        """
        if self.cursor_index is None:
            return self.line_edit.text()

        current_item = self.current_data[self.cursor_index]
        item_macro_pos = self.current_data[self.cursor_index].rfind('%', 1)

        if self.cursor_item_pos > item_macro_pos > 0:
            self.current_data[self.cursor_index] = current_item[:item_macro_pos] + index.data()
        else:
            self.current_data[self.cursor_index] = index.data()

        def update_cursor_pos():
            raw_pos = self.get_path_pos() + len(self.current_data[:self.cursor_index])
            self.line_edit.setCursorPosition(len(self.current_data[self.cursor_index]) + raw_pos)

        # Timer to update cursor after completion (delayed)
        aqt.qt.QTimer(aqt.mw).singleShot(0, update_cursor_pos)

        return ' '.join(self.current_data)


class OptionsDialog(QDialog):
    add_completer: CustomCompleter
    remove_completer: CustomCompleter
    deck_completer: CustomCompleter

    def __init__(self, manager: LeechToolkitConfigManager):
        super().__init__(flags=mw.windowFlags())
        self.manager = manager
        self.config = manager.config
        self.ui = Ui_OptionsDialog()
        self.ui.setupUi(OptionsDialog=self)

        self.reverse_form = ReverseWidget(mw.windowFlags(), self.config)
        self.ui.optionsScrollLayout.addWidget(self.reverse_form.ui.reverseGroup)

        self.leech_actions = ActionsWidget(self.config, Config.LEECH_ACTIONS)
        self.ui.actionsScrollLayout.addWidget(self.leech_actions)

        self.reverse_actions = ActionsWidget(self.config, Config.REVERSE_ACTIONS)
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

        self.leech_actions.load()
        self.reverse_actions.load()

    def _save(self):
        self.config[Config.TOOLBAR_ENABLED] = self.ui.toolsOptionsCheckBox.isChecked()

        self.config[Config.SHOW_LEECH_MARKER] = self.ui.showMarkerChecbkbox.isChecked()
        self.config[Config.USE_ALMOST_MARKER] = self.ui.almostCheckbox.isChecked()
        self.config[Config.MARKER_POSITION] = self.ui.almostPosDropdown.currentIndex()
        self.config[Config.ONLY_SHOW_BACK_MARKER] = self.ui.almostBackCheckbox.isChecked()

        self.config[Config.SHOW_BROWSE_BUTTON] = self.ui.browseButtonCheckbox.isChecked()
        self.config[Config.BROWSE_BUTTON_ON_BROWSER] = self.ui.browseButtonBrowserCheckbox.isChecked()
        self.config[Config.BROWSE_BUTTON_ON_OVERVIEW] = self.ui.browseButtonOverviewCheckbox.isChecked()

        self.leech_actions.save()
        self.reverse_actions.save()

        # Write
        self.manager.write_config()

        # Refresh reviewer if currently active
        if mw.state == 'review':
            reviewer.refresh_action_manager(mw.reviewer)

    def accept(self) -> None:
        self._save()
        super().accept()
        bind_actions()
        mw.reset()


class ActionsWidget(QWidget):
    def __init__(self, config, actions_type: str, parent=None, expanded=True):
        super().__init__(parent, mw.windowFlags())
        self.ui = Ui_ActionsWidget()
        self.ui.setupUi(ActionsWidget=self)
        self.config = config[actions_type]

        def handle_note_selected(dialog: Models):
            dialog.close()
            selected = dialog.form.modelsList.currentRow()
            self.parent
            self.add_edit_item(dialog.models[selected].id)
            redraw_list(self.ui.editFieldsList, max_fields_height)

        def open_note_selection():
            dialog = Models(mw, self, fromMain=False)
            dialog.form.buttonBox.clear()
            dialog.form.modelsList.itemDoubleClicked.disconnect()

            select_button = dialog.form.buttonBox.addButton('Select', QDialogButtonBox.ActionRole)
            qconnect(select_button.clicked, lambda _: handle_note_selected(dialog))

            cancel_button = dialog.form.buttonBox.addButton('Cancel', QDialogButtonBox.ActionRole)
            qconnect(cancel_button.clicked, lambda _: dialog.reject())

            qconnect(dialog.form.modelsList.itemDoubleClicked, lambda _: handle_note_selected(dialog))

        def update_text_size(text_box: QTextEdit):
            doc_height = text_box.document().size().height()
            max_height, min_height = 256, 24
            if doc_height <= max_height:
                text_box.setFixedHeight(min_height if doc_height <= min_height else doc_height + 5)
            else:
                text_box.setFixedHeight(max_height)

        def handle_field_selected(action: QAction):
            self.add_excluded_field(action.data(), action.text())
            redraw_list(self.ui.queueExcludedFieldList)

        if actions_type == Config.LEECH_ACTIONS:
            self.ui.expandoButton.setText(String.LEECH_ACTIONS)
        if actions_type == Config.REVERSE_ACTIONS:
            self.ui.expandoButton.setText(String.LEECH_REVERSE_ACTIONS)

        self.ui.editFieldsList.setStyleSheet('#editFieldsList {background-color: transparent;}')

        self.ui.queueExcludedFieldList.setStyleSheet('#editFieldsList {background-color: transparent;}')
        self.ui.queueLabelBottom.setGraphicsEffect(QGraphicsOpacityEffect())
        self.ui.queueLabelTop.setGraphicsEffect(QGraphicsOpacityEffect())

        self.ui.queueFromSpinbox.dropdown = self.ui.queueFromDropdown
        self.ui.queueToSpinbox.dropdown = self.ui.queueToDropdown

        self.add_completer = CustomCompleter(self.ui.addTagsLine)
        self.remove_completer = CustomCompleter(self.ui.removeTagsLine)
        self.deck_completer = CustomCompleter(self.ui.deckMoveLine)

        self.ui.editAddFieldButton.clicked.connect(open_note_selection)

        self.ui.queueAddFieldButton.setMenu(QMenu(self.ui.queueAddFieldButton))

        self.ui.queueFromDropdown.currentIndexChanged.connect(lambda _: self.ui.queueFromSpinbox.refresh())
        self.ui.queueToDropdown.currentIndexChanged.connect(lambda _: self.ui.queueToSpinbox.refresh())
        self.ui.queueExcludeTextEdit.textChanged.connect(lambda: update_text_size(self.ui.queueExcludeTextEdit))
        self.ui.queueAddFieldButton.menu().triggered.connect(lambda action: handle_field_selected(action))

        self.ui.expandoWidget.set_click_function(lambda: self.toggle_expando(self.ui.expandoButton))
        self.ui.expandoButton.pressed.connect(lambda: self.toggle_expando(self.ui.expandoButton))
        self.toggle_expando(self.ui.expandoButton, expanded)

    def load(self):
        # FLAG
        self.ui.flagCheckbox.setChecked(self.config[Action.FLAG][Action.ENABLED])
        self.ui.flagDropdown.setCurrentIndex(self.config[Action.FLAG][Action.INPUT])

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
        self.ui.suspendCheckbox.setChecked(self.config[Action.SUSPEND][Action.ENABLED])
        self.ui.suspendOnButton.setChecked(self.config[Action.SUSPEND][Action.INPUT])
        self.ui.suspendOffButton.setChecked(not self.config[Action.SUSPEND][Action.INPUT])

        # TAGS
        suggestions = mw.col.weakref().tags.all() + list(Macro.MACROS)
        self.add_completer.set_list([suggestion for suggestion in suggestions if suggestion != Macro.REGEX])
        self.remove_completer.set_list(suggestions)

        # ADD TAGS
        self.ui.addTagsCheckbox.setChecked(self.config[Action.ADD_TAGS][Action.ENABLED])
        self.ui.addTagsLine.setText(self.config[Action.ADD_TAGS][Action.INPUT])
        self.ui.addTagsLine.setCompleter(self.add_completer)

        # REMOVE TAGS
        self.ui.removeTagsCheckbox.setChecked(self.config[Action.REMOVE_TAGS][Action.ENABLED])
        self.ui.removeTagsLine.setText(self.config[Action.REMOVE_TAGS][Action.INPUT])
        self.ui.removeTagsLine.setCompleter(self.remove_completer)

        # FORGET
        self.ui.forgetCheckbox.setChecked(self.config[Action.FORGET][Action.ENABLED])
        self.ui.forgetOnRadio.setChecked(self.config[Action.FORGET][Action.INPUT][0])
        self.ui.forgetOffRadio.setChecked(not self.config[Action.FORGET][Action.INPUT][0])
        self.ui.forgetRestorePosCheckbox.setChecked(self.config[Action.FORGET][Action.INPUT][1])
        self.ui.forgetResetCheckbox.setChecked(self.config[Action.FORGET][Action.INPUT][2])

        # FIELDS
        self.ui.editFieldsCheckbox.setChecked(self.config[Action.EDIT_FIELDS][Action.ENABLED])
        self.add_edit_items(self.config[Action.EDIT_FIELDS][Action.INPUT])
        redraw_list(self.ui.editFieldsList, max_fields_height)

        # DECK MOVE
        self.ui.deckMoveCheckbox.setChecked(self.config[Action.MOVE_TO_DECK][Action.ENABLED])
        deck_names = mw.col.decks.all_names()
        deck_name = mw.col.decks.name_if_exists(self.config[Action.MOVE_TO_DECK][Action.INPUT])
        self.deck_completer.set_list(deck_names)
        self.ui.deckMoveLine.setCompleter(self.deck_completer)
        self.ui.deckMoveLine.setText(deck_name)

        # RESCHEDULE
        reschedule_input = self.config[Action.RESCHEDULE][Action.INPUT]
        self.ui.rescheduleCheckbox.setChecked(self.config[Action.RESCHEDULE][Action.ENABLED])
        self.ui.rescheduleFromDays.setValue(reschedule_input[RescheduleAction.FROM])
        self.ui.rescheduleToDays.setValue(reschedule_input[RescheduleAction.TO])
        self.ui.rescheduleResetCheckbox.setChecked(reschedule_input[RescheduleAction.RESET])

        # ADD TO QUEUE
        queue_input = self.config[Action.ADD_TO_QUEUE][Action.INPUT]
        self.ui.queueCheckbox.setChecked(self.config[Action.ADD_TO_QUEUE][Action.ENABLED])
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

        for note_type in mw.col.models.all():
            sub_menu = self.ui.queueAddFieldButton.menu().addMenu(f'{note_type["name"]}')
            for field in mw.col.models.field_names(note_type):
                action = QAction(f'{field}', self)
                action.setData(note_type['id'])
                sub_menu.addAction(action)

        for note_dict in queue_input[QueueAction.FILTERED_FIELDS]:
            note_type_id = list(note_dict)[0]
            for field_ord in list(note_dict.values()):
                note = mw.col.models.get(NotetypeId(int(note_type_id)))
                self.add_excluded_field(note_type_id, mw.col.models.field_names(note)[field_ord])
        redraw_list(self.ui.queueExcludedFieldList)
        self.ui.queueExcludedFieldList.sortItems()

        self.ui.queueExcludeTextEdit.setText(queue_input[QueueAction.EXCLUDED_TEXT])

        self.ui.queueRatioSlider.setValue(queue_input[QueueAction.SIMILAR_RATIO] * 100)

    def save(self):
        # FLAG
        self.config[Action.FLAG][Action.ENABLED] = self.ui.flagCheckbox.isChecked()
        self.config[Action.FLAG][Action.INPUT] = self.ui.flagDropdown.currentIndex()

        # SUSPEND
        self.config[Action.SUSPEND][Action.ENABLED] = self.ui.suspendCheckbox.isChecked()
        self.config[Action.SUSPEND][Action.INPUT] = self.ui.suspendOnButton.isChecked()

        # ADD TAGS
        self.config[Action.ADD_TAGS][Action.ENABLED] = self.ui.addTagsCheckbox.isChecked()
        self.config[Action.ADD_TAGS][Action.INPUT] = \
            mw.col.tags.join(mw.col.tags.split(self.ui.addTagsLine.text()))

        # REMOVE TAGS
        self.config[Action.REMOVE_TAGS][Action.ENABLED] = self.ui.removeTagsCheckbox.isChecked()
        self.config[Action.REMOVE_TAGS][Action.INPUT] = \
            mw.col.tags.join(mw.col.tags.split(self.ui.removeTagsLine.text()))

        # FORGET
        self.config[Action.FORGET][Action.ENABLED] = self.ui.forgetCheckbox.isChecked()
        self.config[Action.FORGET][Action.INPUT][0] = self.ui.forgetOnRadio.isChecked()
        self.config[Action.FORGET][Action.INPUT][1] = self.ui.forgetRestorePosCheckbox.isChecked()
        self.config[Action.FORGET][Action.INPUT][2] = self.ui.forgetResetCheckbox.isChecked()

        # FIELDS
        self.config[Action.EDIT_FIELDS][Action.ENABLED] = self.ui.editFieldsCheckbox.isChecked()
        self.config[Action.EDIT_FIELDS][Action.INPUT] = {}
        for i in range(self.ui.editFieldsList.count()):
            item = EditFieldItem.from_list_widget(self.ui.editFieldsList, self.ui.editFieldsList.item(i))
            note_id = str(item.note['id'])
            if note_id in self.config[Action.EDIT_FIELDS][Action.INPUT]:
                note_id += f'.{self.get_same_notes_count(note_id)}'
            self.config[Action.EDIT_FIELDS][Action.INPUT][note_id] = item.get_data()

        # DECK MOVE
        self.config[Action.MOVE_TO_DECK][Action.ENABLED] = self.ui.deckMoveCheckbox.isChecked()
        stored_did = self.ui.deckMoveLine.text()
        self.config[Action.MOVE_TO_DECK][Action.INPUT] = mw.col.decks.id(stored_did) if stored_did else None

        # RESCHEDULE
        reschedule_input = self.config[Action.RESCHEDULE][Action.INPUT]
        self.config[Action.RESCHEDULE][Action.ENABLED] = self.ui.rescheduleCheckbox.isChecked()
        reschedule_input[RescheduleAction.FROM] = self.ui.rescheduleFromDays.value()
        reschedule_input[RescheduleAction.TO] = self.ui.rescheduleToDays.value()
        reschedule_input[RescheduleAction.RESET] = self.ui.rescheduleResetCheckbox.isChecked()

        # ADD TO QUEUE
        queue_input = self.config[Action.ADD_TO_QUEUE][Action.INPUT]
        self.config[Action.ADD_TO_QUEUE][Action.ENABLED] = self.ui.queueCheckbox.isChecked()
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
            field_item = ExcludedFieldItem.from_list_widget(self.ui.queueExcludedFieldList, item)
            field_dict = field_item.get_model_field_dict()
            queue_input[QueueAction.FILTERED_FIELDS].append(field_dict)
        queue_input[QueueAction.EXCLUDED_TEXT] = self.ui.queueExcludeTextEdit.toPlainText()

        queue_input[QueueAction.SIMILAR_RATIO] = self.ui.queueRatioSlider.value() / 100

    def toggle_expando(self, button: aqt.qt.QToolButton, toggle: bool = None):
        toggle = not self.ui.actionsFrame.isVisible() if toggle is None else toggle
        button.setArrowType(arrow_types[toggle])
        if button == self.ui.expandoButton:
            self.ui.actionsFrame.setVisible(toggle)

    def get_same_notes_count(self, nid):
        filtered_nids = self.config[Config.LEECH_ACTIONS][Action.EDIT_FIELDS][Action.INPUT]
        return len(
            [
                filtered_nid
                for filtered_nid in filtered_nids
                if str(filtered_nid).find(str(nid)) >= 0
            ]
        )

    def add_edit_items(self, data: {str: {str: int or str}}):
        for filtered_nid in data:
            field = data[filtered_nid]
            nid = str(filtered_nid).split('.')[0]
            self.add_edit_item(
                nid=int(nid),
                field_idx=field[EditAction.FIELD],
                method_idx=field[EditAction.METHOD],
                repl=field[EditAction.REPL],
                input_text=field[EditAction.TEXT]
            )

    def add_edit_item(self, nid: int, field_idx: int = -1, method_idx=EditAction.EditMethod(0), repl='',
                      input_text=''):
        edit_item = EditFieldItem(self, nid, field_idx, method_idx, repl, input_text)
        list_item = QListWidgetItem(self.ui.editFieldsList)
        list_item.setSizeHint(edit_item.sizeHint())
        list_item.setFlags(Qt.NoItemFlags)

        self.ui.editFieldsList.addItem(list_item)
        self.ui.editFieldsList.setItemWidget(list_item, edit_item)

    def add_excluded_field(self, mid: int, text=''):
        """
    Inserts a new excluded field item to the excluded fields list if not already present.
        :param mid: Model ID of the note/field
        :param text: text string of the field's name/title
        """
        for i in range(0, self.ui.queueExcludedFieldList.count()):
            item = self.ui.queueExcludedFieldList.item(i)
            field_item = ExcludedFieldItem.from_list_widget(self.ui.queueExcludedFieldList, item)
            fields_names = mw.col.models.field_names(mw.col.models.get(mid))
            if field_item.get_model_field_dict() == {f'{mid}': fields_names.index(text)}:
                return

        field_item = ExcludedFieldItem(self, mid=mid, field_name=text)
        list_item = ExcludedFieldItem.ExcludedFieldListItem(self.ui.queueExcludedFieldList)
        list_item.setSizeHint(field_item.sizeHint())
        list_item.setFlags(Qt.NoItemFlags)

        self.ui.queueExcludedFieldList.addItem(list_item)
        self.ui.queueExcludedFieldList.setItemWidget(list_item, field_item)


class ReverseWidget(QWidget):
    def __init__(self, flags, config):
        super().__init__(flags=flags)
        self.ui = Ui_ReverseForm()
        self.ui.setupUi(self)
        self.config = config

        def toggle_threshold(checked: bool):
            self.ui.reverseThresholdSpinbox.setEnabled(checked)

        self.ui.useLeechThresholdCheckbox.stateChanged.connect(lambda checked: toggle_threshold(not checked))

    def load(self):
        self.ui.reverseCheckbox.setChecked(self.config[Config.REVERSE_ENABLED])
        self.ui.useLeechThresholdCheckbox.setChecked(self.config[Config.REVERSE_USE_LEECH_THRESHOLD])
        self.ui.reverseMethodDropdown.setCurrentIndex(self.config[Config.REVERSE_METHOD])
        self.ui.reverseThresholdSpinbox.setValue(self.config[Config.REVERSE_THRESHOLD])
        self.ui.consAnswerSpinbox.setValue(self.config[Config.REVERSE_CONS_ANS])

    def save(self):
        self.config[Config.REVERSE_ENABLED] = self.ui.reverseCheckbox.isChecked()
        self.config[Config.REVERSE_METHOD] = self.ui.reverseMethodDropdown.currentIndex()
        self.config[Config.REVERSE_USE_LEECH_THRESHOLD] = self.ui.useLeechThresholdCheckbox.isChecked()
        self.config[Config.REVERSE_THRESHOLD] = self.ui.reverseThresholdSpinbox.value()
        self.config[Config.REVERSE_CONS_ANS] = self.ui.consAnswerSpinbox.value()


class ExcludedFieldItem(QWidget):

    @staticmethod
    def from_list_widget(field_list: QListWidget, item: QListWidgetItem) -> "ExcludedFieldItem":
        """
    Returns an ExcludedFieldItem using a base QListWidgetItem.
        :param field_list: reference list
        :param item: QListWidgetItem object located in the referenced list
        :return: an ExcludedFieldItem object
        """
        return field_list.itemWidget(item)

    def __init__(self, actions_dialog: ActionsWidget, mid: int, field_name: str):
        super().__init__(flags=mw.windowFlags())
        self.dialog = actions_dialog
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
            for i in range(self.dialog.ui.queueExcludedFieldList.count()):
                item = self.dialog.ui.queueExcludedFieldList.item(i)
                if self == self.from_list_widget(self.dialog.ui.queueExcludedFieldList, item):
                    self.dialog.ui.queueExcludedFieldList.takeItem(i)
                    redraw_list(self.dialog.ui.queueExcludedFieldList)

        self.widget.removeButton.clicked.connect(remove_self)

    def get_model_field_dict(self):
        fields_names = mw.col.models.field_names(mw.col.models.get(self.mid))
        return {f'{self.mid}': fields_names.index(self.widget.fieldLabel.text())}

    class ExcludedFieldListItem(QListWidgetItem):
        def __lt__(self, other):
            this_item = ExcludedFieldItem.from_list_widget(self.listWidget(), self)
            other_item = ExcludedFieldItem.from_list_widget(other.listWidget(), other)
            if other_item is None:
                return False
            else:
                this_data = f'{this_item.mid}{this_item.widget.fieldLabel.text()}'
                other_data = f'{other_item.mid}{other_item.widget.fieldLabel.text()}'
                return this_data < other_data


class EditFieldItem(QWidget):
    note: aqt.models.NotetypeDict

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
            actions_dialog: ActionsWidget,
            nid: int,
            field_idx: int = -1,
            method_idx=EditAction.EditMethod(0),
            repl: str = None,
            text: str = None
    ):
        """
    NoteItem used for the field edit list.
        :param text: string value to use for the label of the list item
        :param actions_dialog: reference to the base class to use for context menu actions
        """
        super().__init__(flags=mw.windowFlags())
        self.context_menu = QMenu(self)
        self.dialog = actions_dialog
        self.widget = Ui_EditFieldItem()
        self.widget.setupUi(EditFieldItem=self)
        self.widget.removeButton.setIcon(QIcon(f'{Path(__file__).parent.resolve()}\\{REMOVE_ICON_PATH}'))

        self.set_note(nid)
        self.update_forms(field_idx=field_idx, method_idx=method_idx, repl=repl, text=text)

        def remove_self(_):
            """
        Removes the current item from its list widget.
            :param _: placeholder argument given by QAction calls
            """
            for i in range(self.dialog.ui.editFieldsList.count()):
                item = self.dialog.ui.editFieldsList.item(i)
                if self == self.from_list_widget(self.dialog.ui.editFieldsList, item):
                    self.dialog.ui.editFieldsList.takeItem(i)
                    redraw_list(self.dialog.ui.editFieldsList)

        self.widget.removeButton.clicked.connect(remove_self)
        self.widget.methodDropdown.currentIndexChanged.connect(self.refresh_method_forms)

    def refresh_method_forms(self, method_idx: int):
        is_replace = method_idx in (EditAction.REPLACE_METHOD, EditAction.REGEX_METHOD)
        self.widget.replaceEdit.setVisible(is_replace)
        self.widget.inputEdit.setPlaceholderText(String.REPLACE_WITH if is_replace else String.OUTPUT_TEXT)

    def update_forms(
            self,
            field_idx: int = -1,
            method_idx=EditAction.EditMethod(0),
            repl: str = None,
            text: str = None
    ):
        """
    Updates the item's forms to the input values.
        :param field_idx: index of the current note's fields to modify
        :param method_idx: index/EditMethod object of the method to use
        :param repl: text to try and replace
        :param text: text to use for appending/prepending/replacing
        """
        note_fields = mw.col.models.get(self.note['id']).get('flds')

        self.widget.fieldDropdown.addItems([field['name'] for field in note_fields])

        if field_idx >= 0:
            self.widget.fieldDropdown.setCurrentIndex(field_idx)
        if method_idx >= 0:
            self.widget.methodDropdown.setCurrentIndex(method_idx)
            self.refresh_method_forms(method_idx)
        if repl:
            self.widget.replaceEdit.setText(repl)
        if text:
            self.widget.inputEdit.setText(text)

    def set_note(self, nid: int):
        self.note = mw.col.models.get(NoteId(nid))
        self.widget.noteLabel.setText(mw.col.models.get(nid)['name'])

    def get_data(self):
        """
Retrieves the current, relevant data held in this list item.
        :return: Tuple(note id, field index, method index, find text, input text)
        """
        return {
            str(EditAction.FIELD): self.widget.fieldDropdown.currentIndex(),
            str(EditAction.METHOD): self.widget.methodDropdown.currentIndex(),
            str(EditAction.REPL): self.widget.replaceEdit.text(),
            str(EditAction.TEXT): self.widget.inputEdit.text()
        }
