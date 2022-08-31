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
from aqt.models import Models
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
)

from .config import LeechToolkitConfigManager
from .consts import String, Config, Action, Macro, REMOVE_ICON_PATH, EditAction, RescheduleAction, QueueAction
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


def on_options_called(result=False):
    options = OptionsDialog(LeechToolkitConfigManager(mw))
    options.exec()


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

        self.leech_actions.save(self.config[Config.LEECH_ACTIONS])
        self.reverse_actions.save(self.config[Config.UN_LEECH_ACTIONS])
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


class ActionsWidget(QWidget):
    def __init__(self, actions_type: str, parent=None, expanded=True):
        super().__init__(parent, mw.windowFlags())
        self.ui = Ui_ActionsForm()
        self.ui.setupUi(ActionsForm=self)
        self.actions_type = actions_type

        def update_text_size(text_box: QTextEdit):
            doc_height = text_box.document().size().height()
            max_height, min_height = 256, 24
            if doc_height <= max_height:
                text_box.setFixedHeight(min_height if doc_height <= min_height else doc_height + 5)
            else:
                text_box.setFixedHeight(max_height)

        def handle_field_selected(action: QAction, list_widget: QListWidget):
            if list_widget.objectName() == self.ui.queueExcludedFieldList.objectName():
                self.add_excluded_field(action.data(), action.text())
            elif list_widget.objectName() == self.ui.editFieldsList.objectName():
                self.add_edit_field(action.data(), action.text())
            redraw_list(list_widget)

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

        self.ui.queueExcludeTextEdit.textChanged.connect(lambda: update_text_size(self.ui.queueExcludeTextEdit))

        # sub_menu = self.ui.queueAddFieldButton.menu().addMenu(f'{note_type["name"]}')

        self.ui.queueAddFieldButton.setMenu(QMenu(self.ui.queueAddFieldButton))
        self.ui.queueAddFieldButton.menu().triggered.connect(
            lambda action: handle_field_selected(action, self.ui.queueExcludedFieldList)
        )

        self.ui.editAddFieldButton.setMenu(QMenu(self.ui.editAddFieldButton))
        self.ui.editAddFieldButton.menu().triggered.connect(
            lambda action: handle_field_selected(action, self.ui.editFieldsList)
        )

        self.ui.expandoWidget.set_click_function(lambda: self.toggle_expando(self.ui.expandoButton))
        self.ui.expandoButton.pressed.connect(lambda: self.toggle_expando(self.ui.expandoButton))
        self.toggle_expando(self.ui.expandoButton, expanded)

    def load(self, actions_config: dict):

        def fill_menu_fields(add_button: aqt.qt.QToolButton):
            for note_type in mw.col.models.all():
                sub_menu = add_button.menu().addMenu(f'{note_type["name"]}')
                for field in mw.col.models.field_names(note_type):
                    action = QAction(f'{field}', self)
                    action.setData(note_type['id'])
                    sub_menu.addAction(action)

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
                self.add_edit_field(mid, field_name, item_data[1], item_data[2], item_data[3])
            redraw_list(self.ui.editFieldsList, max_fields_height)

            fill_menu_fields(self.ui.editAddFieldButton)

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
                note_type_id = list(note_dict)[0]
                for field_ord in list(note_dict.values()):
                    note = mw.col.models.get(NotetypeId(int(note_type_id)))
                    self.add_excluded_field(note_type_id, mw.col.models.field_names(note)[field_ord])
            self.ui.queueExcludedFieldList.sortItems()
            redraw_list(self.ui.queueExcludedFieldList)

            fill_menu_fields(self.ui.queueAddFieldButton)

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

    def save(self, actions_config: dict):
        def save_flag():
            actions_config[Action.FLAG][Action.ENABLED] = self.ui.flagCheckbox.isChecked()
            actions_config[Action.FLAG][Action.INPUT] = self.ui.flagDropdown.currentIndex()

        def save_suspend():
            actions_config[Action.SUSPEND][Action.ENABLED] = self.ui.suspendCheckbox.isChecked()
            actions_config[Action.SUSPEND][Action.INPUT] = self.ui.suspendOnButton.isChecked()

        def save_add_tags():
            actions_config[Action.ADD_TAGS][Action.ENABLED] = self.ui.addTagsCheckbox.isChecked()
            actions_config[Action.ADD_TAGS][Action.INPUT] = \
                mw.col.tags.join(mw.col.tags.split(self.ui.addTagsLine.text()))

        def save_remove_tags():
            actions_config[Action.REMOVE_TAGS][Action.ENABLED] = self.ui.removeTagsCheckbox.isChecked()
            actions_config[Action.REMOVE_TAGS][Action.INPUT] = \
                mw.col.tags.join(mw.col.tags.split(self.ui.removeTagsLine.text()))

        def save_forget():
            actions_config[Action.FORGET][Action.ENABLED] = self.ui.forgetCheckbox.isChecked()
            actions_config[Action.FORGET][Action.INPUT][0] = self.ui.forgetOnRadio.isChecked()
            actions_config[Action.FORGET][Action.INPUT][1] = self.ui.forgetRestorePosCheckbox.isChecked()
            actions_config[Action.FORGET][Action.INPUT][2] = self.ui.forgetResetCheckbox.isChecked()

        # def save_edit_fields():
        #     actions_config[Action.EDIT_FIELDS][Action.ENABLED] = self.ui.editFieldsCheckbox.isChecked()
        #     actions_config[Action.EDIT_FIELDS][Action.INPUT] = {}
        #
        #     def get_same_notes_count(nid):
        #         filtered_nids = actions_config[Action.EDIT_FIELDS][Action.INPUT]
        #         return len([filtered_nid for filtered_nid in filtered_nids if str(filtered_nid).find(str(nid)) >= 0])
        #
        #     for i in range(self.ui.editFieldsList.count()):
        #         item = EditFieldItem.from_list_widget(self.ui.editFieldsList, self.ui.editFieldsList.item(i))
        #         note_id = str(item.note['id'])
        #         if note_id in actions_config[Action.EDIT_FIELDS][Action.INPUT]:
        #             note_id += f'.{get_same_notes_count(note_id)}'
        #         actions_config[Action.EDIT_FIELDS][Action.INPUT][note_id] = item.get_data()

        def save_deck_move():
            actions_config[Action.MOVE_TO_DECK][Action.ENABLED] = self.ui.deckMoveCheckbox.isChecked()
            stored_did = self.ui.deckMoveLine.text()
            actions_config[Action.MOVE_TO_DECK][Action.INPUT] = mw.col.decks.id(stored_did) if stored_did else None

        def save_reschedule():
            actions_config[Action.RESCHEDULE][Action.ENABLED] = self.ui.rescheduleCheckbox.isChecked()
            reschedule_input = actions_config[Action.RESCHEDULE][Action.INPUT]
            reschedule_input[RescheduleAction.FROM] = self.ui.rescheduleFromDays.value()
            reschedule_input[RescheduleAction.TO] = self.ui.rescheduleToDays.value()
            reschedule_input[RescheduleAction.RESET] = self.ui.rescheduleResetCheckbox.isChecked()

        def save_add_to_queue():
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
                field_dict = field_item.get_model_field_dict()
                queue_input[QueueAction.FILTERED_FIELDS].append(field_dict)

            queue_input[QueueAction.EXCLUDED_TEXT] = self.ui.queueExcludeTextEdit.toPlainText()
            queue_input[QueueAction.SIMILAR_RATIO] = self.ui.queueRatioSlider.value() / 100

        # A little easier to read/debug
        save_flag()
        save_suspend()
        save_add_tags()
        save_remove_tags()
        save_forget()
        # save_edit_fields()
        save_deck_move()
        save_reschedule()
        save_add_to_queue()

    def toggle_expando(self, button: aqt.qt.QToolButton, toggle: bool = None):
        toggle = not self.ui.actionsFrame.isVisible() if toggle is None else toggle
        button.setArrowType(arrow_types[toggle])
        if button == self.ui.expandoButton:
            self.ui.actionsFrame.setVisible(toggle)

    def add_edit_field(self, mid: int, field_name: str, method_idx=EditAction.EditMethod(0), repl='', text=''):
        edit_item = EditFieldItem(self.ui.editFieldsList, mid, field_name, method_idx, repl, text)

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
            exclude_item = ExcludeFieldItem.from_list_widget(self.ui.queueExcludedFieldList, item)
            fields_names = mw.col.models.field_names(mw.col.models.get(mid))
            if exclude_item.get_model_field_dict() == {f'{mid}': fields_names.index(text)}:
                return

        exclude_item = ExcludeFieldItem(self, mid=mid, field_name=text)

        list_item = ExcludeFieldItem.ExcludedFieldListItem(self.ui.queueExcludedFieldList)
        list_item.setSizeHint(exclude_item.sizeHint())
        list_item.setFlags(Qt.NoItemFlags)

        self.ui.queueExcludedFieldList.addItem(list_item)
        self.ui.queueExcludedFieldList.setItemWidget(list_item, exclude_item)


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
            this_item = ExcludeFieldItem.from_list_widget(self.listWidget(), self)
            other_item = ExcludeFieldItem.from_list_widget(other.listWidget(), other)
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
        self.list_widget = edit_list

        self.mid = mid
        self.note_type_dict = mw.col.models.get(NotetypeId(self.mid))
        self.model_name = self.note_type_dict["name"] if self.note_type_dict else ''

        self.field_name = field_name
        self.method_idx = method_idx
        self.repl = repl
        self.text = text

        self.widget = Ui_EditFieldItem()
        self.widget.setupUi(EditFieldItem=self)

        self.widget.removeButton.setIcon(QIcon(f'{Path(__file__).parent.resolve()}\\{REMOVE_ICON_PATH}'))

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
        self.widget.methodDropdown.currentIndexChanged.connect(self.update_method_dropdown)
        self.widget.fieldButtonLabel.clicked.connect()

        self._load()

    def _load(self):
        self.widget.fieldButtonLabel.setText(self.field_name)
        self.widget.fieldButtonLabel.setToolTip(self.model_name)
        self.update_method_dropdown(self.method_idx)
        self.widget.replaceEdit.setText(self.repl)
        self.widget.inputEdit.setText(self.text)

    def update_method_dropdown(self, method_idx: int):
        if method_idx >= 0:
            replace_selected = method_idx in (EditAction.REPLACE_METHOD, EditAction.REGEX_METHOD)
            self.widget.methodDropdown.setCurrentIndex(method_idx)
            self.widget.replaceEdit.setVisible(replace_selected)
            self.widget.inputEdit.setPlaceholderText(String.REPLACE_WITH if replace_selected else String.OUTPUT_TEXT)

    def get_model_field_dict(self):
        if self.note_type_dict:
            fields_names = mw.col.models.field_names(self.note_type_dict)
            return {f'{self.mid}': fields_names.index(self.widget.fieldButtonLabel.text())}
        else:
            return {f'{self.mid}': 0}
