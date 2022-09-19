from aqt import gui_hooks, mw


def build_hooks():
    gui_hooks.sync_did_finish.append(sync_collection)


def sync_collection():
    print(f'Syncing...')
    pass
