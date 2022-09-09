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
    pyqtBoundSignal,
    QLayout,
    QGridLayout,
    QBoxLayout,
)

from .config import LeechToolkitConfigManager
from .consts import (
    String, Config, Action, Macro, REMOVE_ICON_PATH, EditAction, RescheduleAction, QueueAction,
    RESTORE_ICON_PATH,
)
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
    fields_list.currentRowChanged.emit(fields_list.currentRow())  # Used for updating any change receivers


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

        self.leech_form = ActionsWidget(Config.LEECH_ACTIONS)
        self.ui.actionsScrollLayout.addWidget(self.leech_form)

        self.unleech_form = ActionsWidget(Config.UN_LEECH_ACTIONS)
        self.ui.actionsScrollLayout.addWidget(self.unleech_form)

        set_default_button(self.ui.showMarkerCheckbox, self.ui.enableMarkLayout)
        set_default_button(self.ui.browseButtonCheckbox, self.ui.browseButtonLayout)

        self._load()

        # Just in case
        self.ui.tabWidget.setCurrentIndex(0)

    def load_defaults(self, config: dict, default_config: dict):
        marker_signals = [
            self.ui.showMarkerCheckbox.stateChanged,
            self.ui.almostCheckbox.stateChanged,
            self.ui.almostPosDropdown.currentIndexChanged,
            self.ui.almostBackCheckbox.stateChanged,
        ]
        load_default_button(
            self.ui.showMarkerCheckbox.button,
            marker_signals,
            self.write_marker,
            self.load_marker,
            self.config[Config.MARKER_OPTIONS],
            Config.DEFAULT_CONFIG[Config.MARKER_OPTIONS]
        )

        button_signals = [
            self.ui.browseButtonCheckbox.stateChanged,
            self.ui.browseButtonBrowserCheckbox.stateChanged,
            self.ui.browseButtonOverviewCheckbox.stateChanged,
        ]
        load_default_button(
            self.ui.browseButtonCheckbox.button,
            button_signals,
            self.write_button,
            self.load_button,
            self.config[Config.BUTTON_OPTIONS],
            Config.DEFAULT_CONFIG[Config.BUTTON_OPTIONS]
        )

        self.reverse_form.load_default(config[Config.REVERSE_OPTIONS], default_config[Config.REVERSE_OPTIONS])

    def load_marker(self, marker_conf: dict):
        self.ui.showMarkerCheckbox.setChecked(marker_conf[Config.SHOW_LEECH_MARKER])
        self.ui.almostCheckbox.setChecked(marker_conf[Config.USE_ALMOST_MARKER])
        self.ui.almostPosDropdown.setCurrentIndex(marker_conf[Config.MARKER_POSITION])
        self.ui.almostBackCheckbox.setChecked(marker_conf[Config.ONLY_SHOW_BACK_MARKER])

    def load_button(self, button_conf: dict):
        self.ui.browseButtonCheckbox.setChecked(button_conf[Config.SHOW_BUTTON])
        self.ui.browseButtonBrowserCheckbox.setChecked(button_conf[Config.SHOW_BROWSER_BUTTON])
        self.ui.browseButtonOverviewCheckbox.setChecked(button_conf[Config.SHOW_OVERVIEW_BUTTON])

    def _load(self):
        self.ui.toolsOptionsCheckBox.setChecked(self.config[Config.TOOLBAR_ENABLED])

        self.load_marker(self.config[Config.MARKER_OPTIONS])
        self.load_button(self.config[Config.BUTTON_OPTIONS])

        self.leech_form.load_all(self.config[Config.LEECH_ACTIONS], Config.DEFAULT_ACTIONS)
        self.unleech_form.load_all(self.config[Config.UN_LEECH_ACTIONS], Config.DEFAULT_ACTIONS)
        self.reverse_form.load_ui(self.config[Config.REVERSE_OPTIONS])

        self.load_defaults(self.config, Config.DEFAULT_CONFIG)

    def write_marker(self, marker_conf: dict):
        marker_conf[Config.SHOW_LEECH_MARKER] = self.ui.showMarkerCheckbox.isChecked()
        marker_conf[Config.USE_ALMOST_MARKER] = self.ui.almostCheckbox.isChecked()
        marker_conf[Config.MARKER_POSITION] = self.ui.almostPosDropdown.currentIndex()
        marker_conf[Config.ONLY_SHOW_BACK_MARKER] = self.ui.almostBackCheckbox.isChecked()

    def write_button(self, button_conf: dict):
        button_conf[Config.SHOW_BUTTON] = self.ui.browseButtonCheckbox.isChecked()
        button_conf[Config.SHOW_BROWSER_BUTTON] = self.ui.browseButtonBrowserCheckbox.isChecked()
        button_conf[Config.SHOW_OVERVIEW_BUTTON] = self.ui.browseButtonOverviewCheckbox.isChecked()

    def _write(self):
        self.config[Config.TOOLBAR_ENABLED] = self.ui.toolsOptionsCheckBox.isChecked()
        self.write_marker(self.config[Config.MARKER_OPTIONS])
        self.write_button(self.config[Config.BUTTON_OPTIONS])

        self.leech_form.write_all(self.config[Config.LEECH_ACTIONS])
        self.unleech_form.write_all(self.config[Config.UN_LEECH_ACTIONS])
        self.reverse_form.write(self.config[Config.REVERSE_OPTIONS])

        # Save config
        self.manager.save_config()

    def accept(self) -> None:
        self._write()
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

        set_default_button(self.ui.reverseCheckbox, self.ui.reverse_enable_layout.layout())

    def load_default(self, reverse_conf: dict, default_conf: dict):
        reverse_signals = [
            self.ui.reverseCheckbox.stateChanged,
            self.ui.useLeechThresholdCheckbox.stateChanged,
            self.ui.reverseMethodDropdown.currentIndexChanged,
            self.ui.reverseThresholdSpinbox.valueChanged,
            self.ui.consAnswerSpinbox.valueChanged,
        ]
        load_default_button(
            button=self.ui.reverseCheckbox.button,
            signals=reverse_signals,
            write_callback=self.write,
            load_callback=self.load_ui,
            scoped_conf=reverse_conf,
            default_scoped_conf=default_conf,
        )

    def load_ui(self, reverse_config: dict):
        self.ui.reverseCheckbox.setChecked(reverse_config[Config.REVERSE_ENABLED])
        self.ui.useLeechThresholdCheckbox.setChecked(reverse_config[Config.REVERSE_USE_LEECH_THRESHOLD])
        self.ui.reverseMethodDropdown.setCurrentIndex(reverse_config[Config.REVERSE_METHOD])
        self.ui.reverseThresholdSpinbox.setValue(reverse_config[Config.REVERSE_THRESHOLD])
        self.ui.consAnswerSpinbox.setValue(reverse_config[Config.REVERSE_CONS_ANS])

    def write(self, reverse_config: dict):
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


def set_default_button(main_widget: QWidget, layout: QLayout, insert_col=4):
    main_widget.button = aqt.qt.QPushButton(main_widget)
    main_widget.button.setMaximumSize(QSize(16, 16))
    main_widget.button.setFlat(True)
    main_widget.button.setToolTip(String.RESTORE_DEFAULT_SETTING)
    main_widget.button.setIcon(QIcon(f'{Path(__file__).parent.resolve()}\\{RESTORE_ICON_PATH}'))

    size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    size_policy.setHorizontalStretch(0)
    size_policy.setVerticalStretch(0)
    size_policy.setHeightForWidth(main_widget.button.sizePolicy().hasHeightForWidth())

    main_widget.button.setSizePolicy(size_policy)

    if layout is not None:
        if isinstance(layout, QGridLayout):
            widget_index = layout.indexOf(main_widget)
            widget_row = layout.getItemPosition(widget_index)[0]
            layout.addWidget(main_widget.button, widget_row, insert_col)
        elif isinstance(layout, QBoxLayout):
            layout.addWidget(main_widget.button, alignment=layout.alignment())
        else:
            layout.addWidget(main_widget.button)


def load_default_button(
    button,
    signals: list[pyqtBoundSignal],
    write_callback,
    load_callback,
    scoped_conf: dict,
    default_scoped_conf: dict = Config.DEFAULT_CONFIG
):
    default_copy = default_scoped_conf.copy()

    for signal in signals:
        def refresh_default_button(*args):
            write_callback(scoped_conf)
            button.setVisible(scoped_conf != default_copy)
        signal.connect(refresh_default_button)

    def restore_defaults(*args):
        load_callback(default_copy)
        refresh_default_button()
    button.clicked.connect(restore_defaults)

    # Initial update
    button.setVisible(scoped_conf != default_copy)


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

        layout = self.ui.actionsFrame.layout()
        set_default_button(self.ui.flagCheckbox, layout)
        set_default_button(self.ui.suspendCheckbox, layout)
        set_default_button(self.ui.addTagsCheckbox, layout)
        set_default_button(self.ui.removeTagsCheckbox, layout)
        set_default_button(self.ui.forgetCheckbox, layout)
        set_default_button(self.ui.editFieldsCheckbox, layout)
        set_default_button(self.ui.deckMoveCheckbox, layout)
        set_default_button(self.ui.rescheduleCheckbox, layout)
        set_default_button(self.ui.queueCheckbox, layout)

    # FLAG
    def load_flag(self, action_conf: dict):
        self.ui.flagCheckbox.setChecked(action_conf[Action.ENABLED])
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
        self.ui.suspendCheckbox.setChecked(action_conf[Action.ENABLED])
        self.ui.suspendOnButton.setChecked(action_conf[Action.INPUT])
        self.ui.suspendOffButton.setChecked(not action_conf[Action.INPUT])

    # ADD TAGS
    def load_add_tags(self, action_conf: dict):
        # TAGS
        tag_suggestions = mw.col.weakref().tags.all() + list(Macro.MACROS)

        self.add_completer.set_list([suggestion for suggestion in tag_suggestions if suggestion != Macro.REGEX])
        self.ui.addTagsCheckbox.setChecked(action_conf[Action.ENABLED])
        self.ui.addTagsLine.setText(action_conf[Action.INPUT])
        self.ui.addTagsLine.setCompleter(self.add_completer)

    # REMOVE TAGS
    def load_remove_tags(self, action_conf: dict):
        # TAGS
        tag_suggestions = mw.col.weakref().tags.all() + list(Macro.MACROS)
        self.remove_completer.set_list(tag_suggestions)
        self.ui.removeTagsCheckbox.setChecked(action_conf[Action.ENABLED])
        self.ui.removeTagsLine.setText(action_conf[Action.INPUT])
        self.ui.removeTagsLine.setCompleter(self.remove_completer)

    # FORGET
    def load_forget(self, action_conf: dict):
        self.ui.forgetCheckbox.setChecked(action_conf[Action.ENABLED])
        self.ui.forgetOnRadio.setChecked(action_conf[Action.INPUT][0])
        self.ui.forgetOffRadio.setChecked(not action_conf[Action.INPUT][0])
        self.ui.forgetRestorePosCheckbox.setChecked(action_conf[Action.INPUT][1])
        self.ui.forgetResetCheckbox.setChecked(action_conf[Action.INPUT][2])

    # EDIT FIELD
    def load_edit_fields(self, action_conf: dict):
        self.ui.editFieldsCheckbox.setChecked(action_conf[Action.ENABLED])
        self.ui.editFieldsList.clear()
        for field_item in action_conf[Action.INPUT]:
            mid, item_data = list(field_item.items())[0]
            note_dict = mw.col.models.get(NotetypeId(mid))
            field_name = mw.col.models.field_names(note_dict)[item_data[0]] if note_dict else String.NOTE_NOT_FOUND

            add_edit_field(self.ui.editFieldsList, mid, field_name, item_data[1], item_data[2], item_data[3])

        redraw_list(self.ui.editFieldsList, max_fields_height)

    # DECK MOVE
    def load_move_deck(self, action_conf: dict):
        self.ui.deckMoveCheckbox.setChecked(action_conf[Action.ENABLED])
        deck_names = [dnid.name for dnid in mw.col.decks.all_names_and_ids()]
        deck_name = mw.col.decks.name_if_exists(action_conf[Action.INPUT])
        self.deck_completer.set_list(deck_names)
        self.ui.deckMoveLine.setCompleter(self.deck_completer)
        self.ui.deckMoveLine.setText(deck_name)

    # RESCHEDULE
    def load_reschedule(self, action_conf: dict):
        reschedule_input = action_conf[Action.INPUT]
        self.ui.rescheduleCheckbox.setChecked(action_conf[Action.ENABLED])
        self.ui.rescheduleFromDays.setValue(reschedule_input[RescheduleAction.FROM])
        self.ui.rescheduleToDays.setValue(reschedule_input[RescheduleAction.TO])
        self.ui.rescheduleResetCheckbox.setChecked(reschedule_input[RescheduleAction.RESET])

    # ADD TO QUEUE
    def load_add_to_queue(self, action_conf: dict):
        queue_input = action_conf[Action.INPUT]
        self.ui.queueCheckbox.setChecked(action_conf[Action.ENABLED])

        self.ui.queueFromDropdown.setCurrentIndex(queue_input[QueueAction.FROM_INDEX])
        self.ui.queueToDropdown.setCurrentIndex(queue_input[QueueAction.TO_INDEX])
        self.ui.queueFromSpinbox.setValue(queue_input[QueueAction.FROM_VAL])
        self.ui.queueToSpinbox.setValue(queue_input[QueueAction.TO_VAL])

        cmd = f"select min(due), max(due) from cards where type={CARD_TYPE_NEW} and odid=0"
        top, bottom = mw.col.db.first(cmd)
        self.ui.queueLabelTopPos.setText(str(top))
        self.ui.queueLabelBottomPos.setText(str(bottom))

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
        redraw_list(self.ui.queueExcludedFieldList)

        self.ui.queueSiblingCheckbox.setChecked(queue_input[QueueAction.NEAR_SIBLING])

    def load_defaults(self, actions_config: dict, default_config):
        # Remove any re-assignment potential issues

        flag_signals = [
            self.ui.flagCheckbox.stateChanged,
            self.ui.flagDropdown.currentTextChanged,
        ]
        load_default_button(
            button=self.ui.flagCheckbox.button,
            signals=flag_signals,
            write_callback=self.write_flag,
            load_callback=self.load_flag,
            scoped_conf=actions_config[Action.FLAG],
            default_scoped_conf=default_config[Action.FLAG],
        )

        suspend_signals = [
            self.ui.suspendCheckbox.stateChanged,
            self.ui.suspendOnButton.toggled,
            self.ui.suspendOffButton.toggled,
        ]
        load_default_button(
            button=self.ui.suspendCheckbox.button,
            signals=suspend_signals,
            write_callback=self.write_suspend,
            load_callback=self.load_suspend,
            scoped_conf=actions_config[Action.SUSPEND],
            default_scoped_conf=default_config[Action.SUSPEND],
        )

        add_tags_signals = [
            self.ui.addTagsCheckbox.stateChanged,
            self.ui.addTagsLine.textChanged,
        ]
        load_default_button(
            button=self.ui.addTagsCheckbox.button,
            signals=add_tags_signals,
            write_callback=self.write_add_tags,
            load_callback=self.load_add_tags,
            scoped_conf=actions_config[Action.ADD_TAGS],
            default_scoped_conf=default_config[Action.ADD_TAGS],
        )

        remove_tags_signals = [
            self.ui.removeTagsCheckbox.stateChanged,
            self.ui.removeTagsLine.textChanged,
        ]
        load_default_button(
            button=self.ui.removeTagsCheckbox.button,
            signals=remove_tags_signals,
            write_callback=self.write_remove_tags,
            load_callback=self.load_remove_tags,
            scoped_conf=actions_config[Action.REMOVE_TAGS],
            default_scoped_conf=default_config[Action.REMOVE_TAGS],
        )

        forget_signals = [
            self.ui.forgetCheckbox.stateChanged,
            self.ui.forgetOnRadio.toggled,
            self.ui.forgetOffRadio.toggled,
            self.ui.forgetResetCheckbox.stateChanged,
            self.ui.forgetRestorePosCheckbox.stateChanged,
        ]
        load_default_button(
            button=self.ui.forgetCheckbox.button,
            signals=forget_signals,
            write_callback=self.write_forget,
            load_callback=self.load_forget,
            scoped_conf=actions_config[Action.FORGET],
            default_scoped_conf=default_config[Action.FORGET],
        )

        edit_fields_signals = [
            self.ui.editFieldsCheckbox.stateChanged,
            self.ui.editFieldsList.currentRowChanged,
        ]
        load_default_button(
            button=self.ui.editFieldsCheckbox.button,
            signals=edit_fields_signals,
            write_callback=self.write_edit_fields,
            load_callback=self.load_edit_fields,
            scoped_conf=actions_config[Action.EDIT_FIELDS],
            default_scoped_conf=default_config[Action.EDIT_FIELDS],
        )

        deck_move_signals = [
            self.ui.deckMoveCheckbox.stateChanged,
            self.ui.deckMoveLine.textChanged,
        ]
        load_default_button(
            button=self.ui.deckMoveCheckbox.button,
            signals=deck_move_signals,
            write_callback=self.write_move_deck,
            load_callback=self.load_move_deck,
            scoped_conf=actions_config[Action.MOVE_DECK],
            default_scoped_conf=default_config[Action.MOVE_DECK],
        )

        reschedule_signals = [
            self.ui.rescheduleCheckbox.stateChanged,
            self.ui.rescheduleFromDays.valueChanged,
            self.ui.rescheduleToDays.valueChanged,
            self.ui.rescheduleResetCheckbox.stateChanged,
        ]
        load_default_button(
            button=self.ui.rescheduleCheckbox.button,
            signals=reschedule_signals,
            write_callback=self.write_reschedule,
            load_callback=self.load_reschedule,
            scoped_conf=actions_config[Action.RESCHEDULE],
            default_scoped_conf=default_config[Action.RESCHEDULE],
        )

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
        load_default_button(
            button=self.ui.queueCheckbox.button,
            signals=queue_signals,
            write_callback=self.write_add_to_queue,
            load_callback=self.load_add_to_queue,
            scoped_conf=actions_config[Action.ADD_TO_QUEUE],
            default_scoped_conf=default_config[Action.ADD_TO_QUEUE],
        )

    def load_all(self, actions_conf: dict, default_conf: dict):
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
        self.load_defaults(actions_conf, default_conf)

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
        actions_config[Action.ENABLED] = self.ui.flagCheckbox.isChecked()
        actions_config[Action.INPUT] = self.ui.flagDropdown.currentIndex()

    def write_suspend(self, actions_config: dict):
        actions_config[Action.ENABLED] = self.ui.suspendCheckbox.isChecked()
        actions_config[Action.INPUT] = self.ui.suspendOnButton.isChecked()

    def write_add_tags(self, actions_config: dict):
        actions_config[Action.ENABLED] = self.ui.addTagsCheckbox.isChecked()
        actions_config[Action.INPUT] = \
            mw.col.tags.join(mw.col.tags.split(self.ui.addTagsLine.text()))

    def write_remove_tags(self, actions_config: dict):
        actions_config[Action.ENABLED] = self.ui.removeTagsCheckbox.isChecked()
        actions_config[Action.INPUT] = \
            mw.col.tags.join(mw.col.tags.split(self.ui.removeTagsLine.text()))

    def write_forget(self, actions_config: dict):
        actions_config[Action.ENABLED] = self.ui.forgetCheckbox.isChecked()
        actions_config[Action.INPUT][0] = self.ui.forgetOnRadio.isChecked()
        actions_config[Action.INPUT][1] = self.ui.forgetRestorePosCheckbox.isChecked()
        actions_config[Action.INPUT][2] = self.ui.forgetResetCheckbox.isChecked()

    def write_edit_fields(self, actions_config: dict):
        actions_config[Action.ENABLED] = self.ui.editFieldsCheckbox.isChecked()
        edit_input: list = actions_config[Action.INPUT]

        edit_input.clear()
        for i in range(self.ui.editFieldsList.count()):
            item = EditFieldItem.from_list_widget(self.ui.editFieldsList, self.ui.editFieldsList.item(i))
            edit_input.append(item.get_field_edit_dict()) if item is not None else None

    def write_move_deck(self, actions_config: dict):
        actions_config[Action.ENABLED] = self.ui.deckMoveCheckbox.isChecked()
        stored_did = self.ui.deckMoveLine.text()
        actions_config[Action.INPUT] = mw.col.decks.id(stored_did) if stored_did else ''

    def write_reschedule(self, actions_config: dict):
        actions_config[Action.ENABLED] = self.ui.rescheduleCheckbox.isChecked()
        reschedule_input = actions_config[Action.INPUT]
        reschedule_input[RescheduleAction.FROM] = self.ui.rescheduleFromDays.value()
        reschedule_input[RescheduleAction.TO] = self.ui.rescheduleToDays.value()
        reschedule_input[RescheduleAction.RESET] = self.ui.rescheduleResetCheckbox.isChecked()

    def write_add_to_queue(self, actions_config: dict):
        actions_config[Action.ENABLED] = self.ui.queueCheckbox.isChecked()

        queue_input = actions_config[Action.INPUT]
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
                    redraw_list(self.list_widget)

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
