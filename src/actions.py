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
        leech_actions = self.user_config[Config.LEECH_ACTIONS]
        for action in leech_actions:
            print(f'ACTION {action}: {leech_actions[action]}')
            if action == Action.FLAG:
                if leech_actions[Action.FLAG][Action.ENABLED]:
                    card.set_user_flag(leech_actions[Action.FLAG][Action.INPUT])
            if action == Action.SUSPEND:
                if leech_actions[Action.SUSPEND][Action.ENABLED]:
                    card.queue = -1
            if action == Action.ADD_TAGS:
                if leech_actions[Action.ADD_TAGS][Action.ENABLED]:
                    for tag in str(leech_actions[Action.ADD_TAGS][Action.INPUT]).split(', '):
                        card.note().add_tag(tag)

        card.flush()
        card.note().flush()
