"""
MIT License: Copyright (c) 2022 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
Full license text available in "LICENSE" file packaged with the program.
"""
from aqt import AnkiQt

from .consts import Config


def _init_default_fields(config: dict, default_config: dict):
    """
    Recursively initializes config variables using the default config. If a field exists but also has subfields,
    does subsequent checks through each subfield as well.
    :param default_config: base config to compare against
    :param config: config to initialize with the default config
    """
    for field in default_config:
        if field not in config:
            print(f'\nField not found: {field}')
            config[field] = default_config[field]
        elif isinstance(default_config[field], dict):
            _init_default_fields(config[field], default_config[field])


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
        _init_default_fields(self.config, Config.DEFAULT_CONFIG)

        self._meta['config'] = self.config

    def write_config(self):
        """
Writes the config manager's current values to the addon meta file.
        """
        self._mw.addonManager.writeAddonMeta(self._addon, self._meta)

    def config_for_did(self, did: int, init=True):
        config_id = self._mw.col.decks.config_dict_for_deck_id(did)['id']

        config = self.config.get(str(config_id), {})

        if init:
            default_config = Config.DEFAULT_CONFIG
            default_config[Config.REVERSE_ENABLED] = False
            _init_default_fields(config, default_config)

        self.config[str(config_id)] = config
        return config
