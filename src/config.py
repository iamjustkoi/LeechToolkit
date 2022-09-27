"""
MIT License: Copyright (c) 2022 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
Full license text available in "LICENSE" file packaged with the program.
"""
import traceback

from aqt import AnkiQt

from .consts import Config, ErrorMsg


def merge_fields(config: dict, default_config: dict):
    """
    Recursively initializes config variables using the default config. If a field exists but also has subfields,
    does subsequent checks through each subfield as well.

    :param default_config: base config to compare against
    :param config: config to initialize with the default config
    """
    default_copy = default_config.copy()
    for field in default_copy:
        if field not in config:
            config[field] = default_copy.get(field)
        elif isinstance(default_copy[field], dict):
            config[field] = merge_fields(config[field], default_copy[field])
    return config


class LeechToolkitConfigManager:
    def __init__(self, mw: AnkiQt):
        """
        Config manager for accessing and writing addon config values.

        :param mw: Anki window to retrieve addon config data from
        """
        super().__init__()
        self._mw = mw
        self._addon = self._mw.addonManager.addonFromModule(__name__)
        self._meta = self._mw.addonManager.addonMeta(self._addon)
        self._meta['config'] = self.config = merge_fields(self._meta.get('config', {}), Config.DEFAULT_CONFIG)

    def get_all_configs(self):
        """
        Retrieves a dictionary of deck configs with global defaults.
        """
        toolkit_configs: dict = {}
        for deck_name_id in self._mw.col.decks.all_names_and_ids():
            config_id = self._mw.col.decks.get(deck_name_id.id)['conf']
            toolkit_configs[f'{deck_name_id.id}'] = merge_fields(self.config.get(str(config_id), {}), self.config)
        return toolkit_configs

    def save_config(self):
        """
        Writes the config manager's current values to the addon meta file.
        """
        self._mw.addonManager.writeAddonMeta(self._addon, self._meta)

        # Refresh reviewer if currently active
        try:
            self._mw.reviewer.toolkit_manager.load_options() if self._mw.state == 'review' else None
        except AttributeError:
            print(f'{traceback.format_exc()}\n{ErrorMsg.TOOLKIT_MANAGER_NOT_FOUND}')

    def get_group_conf(self, config_id: str):
        """
        Retrieves a new, manager-linked deck config.

        :param config_id: a config/options group id
        :return: a new, instantiated deck-config reference
        """
        self.config[config_id] = merge_fields(self.config.get(config_id, {}), self.get_global_deck_conf())
        return self.config[config_id]

    def get_global_deck_conf(self):
        return {key: val for key, val in self.config.items() if key in Config.DECK_CATEGORIES}
