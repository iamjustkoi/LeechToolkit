"""
MIT License: Copyright (c) 2022 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
Full license text available in "LICENSE" file packaged with the program.
"""
import re
from pathlib import Path

import anki.models
import aqt.flags
from anki.models import NotetypeNameIdUseCount
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
    QListWidget
)

from .config import LeechToolkitConfigManager
from .consts import String, Config, Action, Macro, REMOVE_ICON_PATH, EditAction
from ..res.ui.options_dialog import Ui_OptionsDialog
from ..res.ui.edit_field_item import Ui_FieldWidgetItem


def bind_actions():
    _bind_config_options()
    _bind_tools_options()


def on_options_called(result=False):
    options = OptionsDialog(LeechToolkitConfigManager(mw))
    options.exec()


def _bind_config_options():
    mw.addonManager.setConfigAction(__name__, on_options_called)


def get_colored_icon(path, color):
    icon = QIcon(path)
    pixmap = icon.pixmap()
    pixmap.fill(color)
    return QIcon(pixmap)


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


class TagCompleter(QCompleter):
    def __init__(
            self,
            parent: aqt.qt.QLineEdit
    ) -> None:
        QCompleter.__init__(self, aqt.qt.QStringListModel(), parent)
        self.tags: list[str] = []
        self.edit = parent
        self.cursor_pos: int or None = None

    def set_list(self, suggestions: list):
        self.setModel(aqt.qt.QStringListModel(suggestions))

    def splitPath(self, tags_path: str) -> list[str]:
        stripped_tags = re.sub("  +", " ", tags_path.strip())
        self.tags = mw.col.tags.split(stripped_tags)
        # self.tags.append("")
        pos = self.edit.cursorPosition()
        self.cursor_pos = len(self.tags) - 1 if tags_path.endswith("  ") else stripped_tags.count(" ", 0, pos)
        return [self.tags[self.cursor_pos]]

    def pathFromIndex(self, idx: aqt.qt.QModelIndex) -> str:
        if self.cursor_pos is None:
            return self.edit.text()
        ret = QCompleter.pathFromIndex(self, idx)
        self.tags[self.cursor_pos] = ret
        try:
            self.tags.remove("")
        except ValueError:
            pass
        return f"{' '.join(self.tags)} "


class OptionsDialog(QDialog):
    add_completer: TagCompleter
    remove_completer: TagCompleter

    def __init__(self, manager: LeechToolkitConfigManager):
        super().__init__(flags=manager.mw.windowFlags())
        self.manager = manager
        self.config = manager.config
        self.ui = Ui_OptionsDialog()
        self.ui.setupUi(OptionsDialog=self)

        self.add_completer = TagCompleter(self.ui.addTagsLine)
        self.add_completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.add_completer.setFilterMode(Qt.MatchContains)

        self.remove_completer = TagCompleter(self.ui.removeTagsLine)
        self.remove_completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.remove_completer.setFilterMode(Qt.MatchContains)

        def handle_note_selected(dialog: Models):
            dialog.close()
            selected = dialog.form.modelsList.currentRow()
            self.add_edit_item(dialog.models[selected].id)
            self.redraw_list()

        def open_note_selection():
            dialog = Models(mw, self, fromMain=False)
            dialog.form.buttonBox.clear()
            dialog.form.modelsList.itemDoubleClicked.disconnect()

            select_button = dialog.form.buttonBox.addButton('Select', QDialogButtonBox.ButtonRole.ActionRole)
            qconnect(select_button.clicked, lambda _: handle_note_selected(dialog))

            cancel_button = dialog.form.buttonBox.addButton('Cancel', QDialogButtonBox.ButtonRole.ActionRole)
            qconnect(cancel_button.clicked, lambda _: dialog.reject())

            qconnect(dialog.form.modelsList.itemDoubleClicked, lambda _: handle_note_selected(dialog))

        self.ui.addFieldButton.clicked.connect(open_note_selection)

        self.ui.editFieldsList.setStyleSheet('#editFieldsList {background-color: transparent;}')

        self.ui.useLeechThresholdCheckbox.stateChanged.connect(
            lambda checked:
            self.ui.reverseThresholdSpinbox.setEnabled(not checked)
        )

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

        self.ui.reverseCheckbox.setChecked(self.config[Config.REVERSE_ENABLED])
        self.ui.useLeechThresholdCheckbox.setChecked(self.config[Config.REVERSE_USE_LEECH_THRESHOLD])
        self.ui.reverseMethodDropdown.setCurrentIndex(self.config[Config.REVERSE_METHOD])
        self.ui.reverseThresholdSpinbox.setValue(self.config[Config.REVERSE_THRESHOLD])
        self.ui.consAnswerSpinbox.setValue(self.config[Config.REVERSE_CONS_ANS])

        # Leech Actions
        action_config = self.config[Config.LEECH_ACTIONS]

        # FLAG
        self.ui.flagCheckbox.setChecked(action_config[Action.FLAG][Action.ENABLED])
        self.ui.flagDropdown.setCurrentIndex(action_config[Action.FLAG][Action.INPUT])

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
        self.ui.suspendCheckbox.setChecked(action_config[Action.SUSPEND][Action.ENABLED])
        self.ui.suspendOnButton.setChecked(action_config[Action.SUSPEND][Action.INPUT])
        self.ui.suspendOffButton.setChecked(not action_config[Action.SUSPEND][Action.INPUT])

        # TAGS
        suggestions = mw.col.weakref().tags.all() + list(Macro.MACROS)
        self.add_completer.set_list([suggestion for suggestion in suggestions if suggestion != Macro.REGEX])
        self.remove_completer.set_list(suggestions)

        # tags.focusInEvent = lambda: show_completer_with_focus(evt, self.ui.tags)
        # tags.textEdited.connect(lambda: self.ui.tags.setFocus())

        # ADD TAGS
        self.ui.addTagsCheckbox.setChecked(action_config[Action.ADD_TAGS][Action.ENABLED])
        self.ui.addTagsLine.setText(action_config[Action.ADD_TAGS][Action.INPUT])
        self.ui.addTagsLine.setCompleter(self.add_completer)

        # REMOVE TAGS
        self.ui.removeTagsCheckbox.setChecked(action_config[Action.REMOVE_TAGS][Action.ENABLED])
        self.ui.removeTagsLine.setText(action_config[Action.REMOVE_TAGS][Action.INPUT])
        self.ui.removeTagsLine.setCompleter(self.remove_completer)

        # FORGET
        self.ui.forgetCheckbox.setChecked(action_config[Action.FORGET][Action.ENABLED])
        self.ui.forgetOnRadio.setChecked(action_config[Action.FORGET][Action.INPUT][0])
        self.ui.forgetOffRadio.setChecked(not action_config[Action.FORGET][Action.INPUT][0])
        self.ui.forgetRestorePosCheckbox.setChecked(action_config[Action.FORGET][Action.INPUT][1])
        self.ui.forgetResetCheckbox.setChecked(action_config[Action.FORGET][Action.INPUT][2])

        # # FIELDS
        self.ui.editFieldsCheckbox.setChecked(action_config[Action.EDIT_FIELDS][Action.ENABLED])
        self.add_edit_items(action_config[Action.EDIT_FIELDS][Action.INPUT])
        self.redraw_list()

    def _save(self):
        self.config[Config.TOOLBAR_ENABLED] = self.ui.toolsOptionsCheckBox.isChecked()

        self.config[Config.SHOW_LEECH_MARKER] = self.ui.showMarkerChecbkbox.isChecked()
        self.config[Config.USE_ALMOST_MARKER] = self.ui.almostCheckbox.isChecked()
        self.config[Config.MARKER_POSITION] = self.ui.almostPosDropdown.currentIndex()
        self.config[Config.ONLY_SHOW_BACK_MARKER] = self.ui.almostBackCheckbox.isChecked()

        self.config[Config.SHOW_BROWSE_BUTTON] = self.ui.browseButtonCheckbox.isChecked()
        self.config[Config.BROWSE_BUTTON_ON_BROWSER] = self.ui.browseButtonBrowserCheckbox.isChecked()
        self.config[Config.BROWSE_BUTTON_ON_OVERVIEW] = self.ui.browseButtonOverviewCheckbox.isChecked()

        self.config[Config.REVERSE_ENABLED] = self.ui.reverseCheckbox.isChecked()
        self.config[Config.REVERSE_METHOD] = self.ui.reverseMethodDropdown.currentIndex()
        self.config[Config.REVERSE_USE_LEECH_THRESHOLD] = self.ui.useLeechThresholdCheckbox.isChecked()
        self.config[Config.REVERSE_THRESHOLD] = self.ui.reverseThresholdSpinbox.value()
        self.config[Config.REVERSE_CONS_ANS] = self.ui.consAnswerSpinbox.value()

        # Leech Actions
        action_config = self.config[Config.LEECH_ACTIONS]

        # FLAG
        action_config[Action.FLAG][Action.ENABLED] = self.ui.flagCheckbox.isChecked()
        action_config[Action.FLAG][Action.INPUT] = self.ui.flagDropdown.currentIndex()

        # SUSPEND
        action_config[Action.SUSPEND][Action.ENABLED] = self.ui.suspendCheckbox.isChecked()
        action_config[Action.SUSPEND][Action.INPUT] = self.ui.suspendOnButton.isChecked()

        # ADD TAGS
        action_config[Action.ADD_TAGS][Action.ENABLED] = self.ui.addTagsCheckbox.isChecked()
        action_config[Action.ADD_TAGS][Action.INPUT] = \
            mw.col.tags.join(mw.col.tags.split(self.ui.addTagsLine.text()))

        # REMOVE TAGS
        action_config[Action.REMOVE_TAGS][Action.ENABLED] = self.ui.removeTagsCheckbox.isChecked()
        action_config[Action.REMOVE_TAGS][Action.INPUT] = \
            mw.col.tags.join(mw.col.tags.split(self.ui.removeTagsLine.text()))

        # FORGET
        action_config[Action.FORGET][Action.ENABLED] = self.ui.forgetCheckbox.isChecked()
        action_config[Action.FORGET][Action.INPUT][0] = self.ui.forgetOnRadio.isChecked()
        action_config[Action.FORGET][Action.INPUT][1] = self.ui.forgetRestorePosCheckbox.isChecked()
        action_config[Action.FORGET][Action.INPUT][2] = self.ui.forgetResetCheckbox.isChecked()

        # FIELDS
        action_config[Action.EDIT_FIELDS][Action.ENABLED] = self.ui.editFieldsCheckbox.isChecked()
        action_config[Action.EDIT_FIELDS][Action.INPUT] = {}
        for i in range(self.ui.editFieldsList.count()):
            item = EditFieldItem.from_list_widget(self.ui.editFieldsList, self.ui.editFieldsList.item(i))
            note_id = str(item.note['id'])
            if note_id in action_config[Action.EDIT_FIELDS][Action.INPUT]:
                note_id += f'.{self.get_same_notes_count(note_id)}'
            action_config[Action.EDIT_FIELDS][Action.INPUT][note_id] = item.get_data()

        # Write
        self.manager.write_config()

    def get_same_notes_count(self, nid):
        filtered_nids = self.config[Config.LEECH_ACTIONS][Action.EDIT_FIELDS][Action.INPUT]
        return len(
            [
                filtered_nid
                for filtered_nid in filtered_nids
                if str(filtered_nid).find(str(nid)) >= 0
            ]
        )

    def accept(self) -> None:
        self._save()
        super().accept()
        bind_actions()
        mw.reset()

    def redraw_list(self):
        fields_list = self.ui.editFieldsList
        fields_list.setMinimumWidth(fields_list.sizeHintForColumn(0))
        fields_list.setMinimumHeight(fields_list.sizeHintForRow(0) * fields_list.count())

    def add_edit_items(self, data: {str: {str: int or str}}):
        print(f'data {data}')
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

    def add_edit_item(self, nid: int, field_idx: int = -1, method_idx=EditAction.EditMethod(-1), repl='', input_text=''):
        edit_item = EditFieldItem(self, nid, field_idx, method_idx, repl, input_text)
        list_item = QListWidgetItem(self.ui.editFieldsList)
        list_item.setSizeHint(edit_item.sizeHint())
        list_item.setFlags(Qt.NoItemFlags)

        self.ui.editFieldsList.addItem(list_item)
        self.ui.editFieldsList.setItemWidget(list_item, edit_item)


class EditFieldItem(QWidget):
    # model: Models
    note: aqt.models.NotetypeDict

    @staticmethod
    def from_list_widget(edit_fields_list: QListWidget, item: QListWidgetItem) -> "EditFieldItem":
        return edit_fields_list.itemWidget(item)

    def __init__(
            self,
            dialog: OptionsDialog,
            nid: int,
            field_idx: int = -1,
            method_idx=EditAction.EditMethod(-1),
            repl: str = None,
            text: str = None
    ):
        """
NoteItem used for the field edit list.
        :param text: string value to use for the label of the list item
        :param dialog: reference to the base class to use for context menu actions
        """
        super().__init__()
        self.context_menu = QMenu(self)
        self.dialog = dialog
        self.widget = Ui_FieldWidgetItem()
        self.widget.setupUi(FieldWidgetItem=self)

        self.set_note(nid)
        self.update_forms(field_idx=field_idx, method_idx=method_idx, repl=repl, text=text)
        self.widget.removeButton.setIcon(QIcon(f'{Path(__file__).parent.resolve()}\\{REMOVE_ICON_PATH}'))

        def refresh_replace_input(index: int):
            self.widget.replaceEdit.setVisible(index in (EditAction.REPLACE_METHOD, EditAction.REGEX_METHOD))

        self.widget.methodDropdown.currentIndexChanged.connect(refresh_replace_input)

        def remove(_):
            for i in range(self.dialog.ui.editFieldsList.count()):
                item = self.dialog.ui.editFieldsList.item(i)
                if self == self.from_list_widget(self.dialog.ui.editFieldsList, item):
                    self.dialog.ui.editFieldsList.takeItem(i)
                    self.dialog.redraw_list()

        self.widget.removeButton.clicked.connect(remove)

    def update_forms(
            self,
            field_idx: int = -1,
            method_idx=EditAction.EditMethod(-1),
            repl: str = None,
            text: str = None
    ):
        note_fields = mw.col.models.get(self.note['id']).get('flds')

        self.widget.fieldDropdown.addItems([field['name'] for field in note_fields])
        if field_idx >= 0:
            self.widget.fieldDropdown.setCurrentIndex(field_idx)
        if method_idx >= 0:
            self.widget.methodDropdown.setCurrentIndex(method_idx)
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
