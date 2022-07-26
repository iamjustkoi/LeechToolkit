"""
MIT License: Copyright (c) 2022 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
Full license text available in "LICENSE" file packaged with the program.
"""
from typing import Any

import anki.cards
import aqt.reviewer

# actions object:

# init (Reviewer, Deck):
#     deck_conf = _
#       deck-specific
#     user_conf = _
#       general

# do_leech (Card):

# do_reverse (Card):
from .consts import Config, Action


class LeechActionManager:

    def __init__(self, reviewer: aqt.reviewer.Reviewer, deck_id: int, user_conf: dict[str, Any]):
        # Deck Conf = (Config for Deck's Options Group or None)
        self.reviewer = reviewer
        self.user_config = user_conf

    # Leech actions json: action: {enabled: bool, key: val}
    def run_leech_actions(self, card: anki.cards.Card):
        for action in self.user_config[Config.LEECH_ACTIONS]:
            if action == Action.FLAG:
                print(f'LEECH FLAG: {self.user_config[Config.LEECH_ACTIONS][Action.FLAG]}')
                flag_options = self.user_config[Config.LEECH_ACTIONS][Action.FLAG]
                if flag_options[Action.ENABLED]:
                    card.set_user_flag(flag_options[Action.FLAG_INDEX])

        card.flush()
