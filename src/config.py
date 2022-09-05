"""
MIT License: Copyright (c) 2022 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
Full license text available in "LICENSE" file packaged with the program.
"""
import traceback

from aqt import AnkiQt

from .consts import Config


def merge_fields(config: dict, default_config: dict):
    """
    Recursively initializes config variables using the default config. If a field exists but also has subfields,
    does subsequent checks through each subfield as well.
    :param default_config: base config to compare against
    :param config: config to initialize with the default config
    """
    for field in default_config:
        if field not in config:
            print(f'Default field added: {field}')
            config[field] = default_config.get(field)
        elif isinstance(default_config[field], dict):
            config[field] = merge_fields(config[field], default_config[field])
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

    def write_config(self):
        """
Writes the config manager's current values to the addon meta file.
        """
        self._mw.addonManager.writeAddonMeta(self._addon, self._meta)

        # Refresh reviewer if currently active
        try:
            self._mw.reviewer.toolkit_manager.load_options() if self._mw.state == 'review' else None
        except AttributeError:
            print(f'{traceback.format_exc()}\nToolkit Manager not found in the current Reviewer.')

    def get_conf_for_did(self, did: int, global_conf: dict = None):
        global_conf = self.get_global_deck_conf() if not global_conf else global_conf
        config_id = str(self._mw.col.decks.config_dict_for_deck_id(did)['id'])
        self.config[config_id] = merge_fields(self.config.get(config_id, {}), global_conf)
        return self.config[config_id]

    def get_global_deck_conf(self):
        return {key: val for key, val in self.config.items() if key in Config.DECK_DEFAULT_CATEGORIES}
