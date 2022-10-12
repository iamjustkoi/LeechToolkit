"""
MIT License: Copyright (c) 2022 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
Full license text available in "LICENSE" file packaged with the program.
"""
import anki.cards
from aqt import mw

from .consts import ANKI_LEGACY_VER, CURRENT_ANKI_VER


def _try_check_filtered(did: int):
    if CURRENT_ANKI_VER > ANKI_LEGACY_VER:
        return mw.col.decks.is_filtered(mw.col.decks.get_current_id())
    else:
        return bool(mw.col.decks.get(did)["dyn"])


def _try_get_current_did(card: anki.cards.Card = None):
    col = mw.col if not card else card.col
    if CURRENT_ANKI_VER > ANKI_LEGACY_VER:
        return col.decks.get_current_id()
    else:
        return col.decks.current()["id"]


def _try_get_deck_and_child_ids(did: int):
    if CURRENT_ANKI_VER > ANKI_LEGACY_VER:
        return mw.col.decks.deck_and_child_ids(did)
    else:
        return [did] + mw.col.decks.childDids(did, mw.col.decks.childMap())


def _try_get_config_dict_for_did(did: int):
    if CURRENT_ANKI_VER > ANKI_LEGACY_VER:
        return mw.col.decks.config_dict_for_deck_id(did)
    else:
        deck = mw.col.decks.get(did, default=False)
        assert deck
        if "conf" in deck:
            conf = mw.col.decks.get_config(int(deck["conf"]))
            if not conf:
                # fall back on default
                conf = mw.col.decks.get_config("0")
            conf["dyn"] = False
            return conf
        # dynamic decks have embedded conf
        return deck
