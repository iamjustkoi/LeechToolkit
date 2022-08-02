"""
MIT License: Copyright (c) 2022 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
Full license text available in "LICENSE" file packaged with the program.
"""
import re

import aqt.flags
from aqt import mw
from aqt.models import Models
from aqt.qt import QAction, QDialog, QIcon, QPixmap, QColor, QCompleter, QDialogButtonBox, qconnect
from aqt.qt import Qt
from aqt.tagedit import TagEdit

from .config import LeechToolkitConfigManager
from .consts import String, Config, Action, Macro
from ..res.ui.options_dialog import Ui_OptionsDialog


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

        def open_note_selection():
            dialog = Models(mw, self, fromMain=False)
            dialog.form.buttonBox.clear()
            button = dialog.form.buttonBox.addButton('Select', QDialogButtonBox.ButtonRole.ActionRole)
            qconnect(button.clicked, lambda _: print(f'Note selected!'))

        self.ui.addFieldButton.clicked.connect(open_note_selection)

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
        self.ui.reverseMethodDropdown.setCurrentIndex(self.config[Config.REVERSE_METHOD])
        self.ui.reverseThreshold.setValue(self.config[Config.REVERSE_THRESHOLD])
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
        self.config[Config.REVERSE_THRESHOLD] = self.ui.reverseThreshold.value()
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

        # Write
        self.manager.write_config()

    def accept(self) -> None:
        self._save()
        super().accept()
        bind_actions()
        mw.reset()
