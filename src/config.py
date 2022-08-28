"""
MIT License: Copyright (c) 2022 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
Full license text available in "LICENSE" file packaged with the program.
"""
from aqt import AnkiQt

from .consts import Config


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
            print(f'Default field added: {field}')
            config[field] = default_copy.get(field)
        elif isinstance(default_copy[field], dict):
            merge_fields(config[field], default_copy[field])


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

        self.config = self._meta.get('config', Config.DEFAULT_CONFIG)
        merge_fields(self.config, Config.DEFAULT_CONFIG)

        self._meta['config'] = self.config

    def write_config(self):
        """
Writes the config manager's current values to the addon meta file.
        """
        self._mw.addonManager.writeAddonMeta(self._addon, self._meta)

    def placeholder_config_for_did(self, did: int):
        config_id = str(self._mw.col.decks.config_dict_for_deck_id(did)['id'])

        deck_config = self.config.get(config_id, {Config.REVERSE_OPTIONS: {Config.REVERSE_ENABLED: False}})
        default_copy = Config.DEFAULT_CONFIG.copy()
        merge_fields(
            deck_config,
            {key: val for key, val in default_copy.items() if key in Config.DECK_DEFAULT_CATEGORIES}
        )

        self.config[config_id] = deck_config
        return deck_config
