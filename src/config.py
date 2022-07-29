"""
MIT License: Copyright (c) 2022 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
Full license text available in "LICENSE" file packaged with the program.
"""
from aqt import AnkiQt
from .consts import Config


def _init_default_fields(default_config: dict, config: dict):
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
            _init_default_fields(default_config[field], config[field])


class LeechToolkitConfigManager:

    def __init__(self, mw: AnkiQt):
        """
Config manager for accessing and writing addon config values.

    :param mw: Anki window to retrieve addon config data from
        """
        super().__init__()
        self.mw = mw
        self._addon = self.mw.addonManager.addonFromModule(__name__)
        self._meta = self.mw.addonManager.addonMeta(self._addon)

        self.config = self._meta.get('config', Config.DEFAULT_CONFIG)
        self.decks = self.mw.col.decks if self.mw.col is not None else None

        _init_default_fields(Config.DEFAULT_CONFIG, self.config)

        self._meta['config'] = self.config

    def write_config(self):
        """
Writes the config manager's current values to the addon meta file.
        """
        self.mw.addonManager.writeAddonMeta(self._addon, self._meta)

    def refresh_config(self):
        """
Placeholder for config refreshes/rewrites per-updates, etc.
        """

