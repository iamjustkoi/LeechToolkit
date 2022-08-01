"""
MIT License: Copyright (c) 2022 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
Full license text available in "LICENSE" file packaged with the program.
"""
import re
from datetime import date
from typing import Any

import anki.cards
import aqt.reviewer
from anki.consts import QUEUE_TYPE_SUSPENDED

from .consts import Config, Action, Macro


# do_leech (Card):
# do_reverse (Card):


def get_formatted_tag(card: anki.cards.Card, tag: str):
    result = tag

    macro = Macro.DATE
    if re.search(fr'(?<!%){macro}', tag):
        result = result.replace(macro, date.today().strftime('%x'))

    macro = Macro.REVIEWS
    if re.search(fr'(?<!%){macro}', tag):
        cmd = f'SELECT reps FROM cards WHERE id is {card.id}'
        result = result.replace(macro, str(card.col.db.scalar(cmd)))

    macro = r'%%'
    if re.search(macro, tag):
        result = result.replace(macro, '%')

    return result


class LeechActionManager:
    debug = False

    def __init__(self, reviewer: aqt.reviewer.Reviewer, deck_id: int, user_conf: dict[str, Any]):
        # Deck Conf = (Config for Deck's Options Group or None)
        self.reviewer = reviewer
        # self.deck_config = _
        self.user_config = user_conf

    # Leech actions json: action: {enabled: bool, key: val}
    def run_leech_actions(self, card: anki.cards.Card):
        leech_actions = self.user_config[Config.LEECH_ACTIONS]

        for action in leech_actions:

            if self.debug:
                print(f'ACTION {action}: {leech_actions[action]}')

            if action == Action.FLAG:
                if leech_actions[Action.FLAG][Action.ENABLED]:
                    card.set_user_flag(leech_actions[Action.FLAG][Action.INPUT])

            if action == Action.SUSPEND:
                if leech_actions[Action.SUSPEND][Action.ENABLED]:
                    card.queue = QUEUE_TYPE_SUSPENDED

            if action == Action.ADD_TAGS:
                if leech_actions[Action.ADD_TAGS][Action.ENABLED]:
                    for tag in str(leech_actions[Action.ADD_TAGS][Action.INPUT]).split(' '):
                        formatted_tag = get_formatted_tag(card, tag)
                        card.note().add_tag(formatted_tag)

            if action == Action.REMOVE_TAGS:
                if leech_actions[Action.REMOVE_TAGS][Action.ENABLED]:
                    for tag in leech_actions[Action.REMOVE_TAGS][Action.INPUT].split(' '):
                        # Formats the tag's macros then retrieves the regex pattern and replaces it from the tags string
                        formatted_tag = get_formatted_tag(card, tag)
                        if re.search(f'(?<!%){Macro.REGEX}:.*', formatted_tag):
                            reg_cmd = formatted_tag.replace(f'{Macro.REGEX}:', '', 1)
                            reg_match = re.search(f'((?<=^\")(.*)(?=\"$))|(^(?!\")(.*))', reg_cmd)
                            reg_string = reg_match.group(0).replace(f'.', r'\S')
                            result_tags = re.sub(fr'(?<!\S){reg_string}(?!\S)', '', card.note().string_tags()).strip()
                            card.note().set_tags_from_str(result_tags)
                        else:
                            card.note().remove_tag(formatted_tag)

        if not self.debug:
            card.flush()
            card.note().flush()
