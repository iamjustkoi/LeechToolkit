"""
MIT License: Copyright (c) 2022 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
Full license text available in "LICENSE" file packaged with the program.
"""
from typing import Any

import anki.cards
import aqt.reviewer

# do_leech (Card):

# do_reverse (Card):
from .consts import Config, Action


class LeechActionManager:

    def __init__(self, reviewer: aqt.reviewer.Reviewer, deck_id: int, user_conf: dict[str, Any]):
        # Deck Conf = (Config for Deck's Options Group or None)
        self.reviewer = reviewer
        # self.deck_config = _
        self.user_config = user_conf

    # Leech actions json: action: {enabled: bool, key: val}
    def run_leech_actions(self, card: anki.cards.Card):
        for action in self.user_config[Config.LEECH_ACTIONS]:
            print(f'ACTION {action}: {self.user_config[Config.LEECH_ACTIONS][action]}')
            if action == Action.FLAG:
                flag_options = self.user_config[Config.LEECH_ACTIONS][Action.FLAG]
                if flag_options[Action.ENABLED]:
                    card.set_user_flag(flag_options[Action.FLAG_INDEX])
            if action == Action.SUSPEND:
                sus_options = self.user_config[Config.LEECH_ACTIONS][Action.SUSPEND]
                if sus_options[Action.ENABLED]:
                    card.queue = -1

        card.flush()
