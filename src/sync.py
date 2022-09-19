from aqt import gui_hooks, mw

# from .actions import run_action_updates
from .config import LeechToolkitConfigManager
from .consts import Config


def build_hooks():
    gui_hooks.sync_did_finish.append(sync_collection)


def sync_collection():
    config = LeechToolkitConfigManager(mw).config
    if config[Config.SYNC_ENABLED]:
        print(f'Syncing...')
        #  get revlogs
        #
    pass
