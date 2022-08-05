"""
MIT License: Copyright (c) 2022 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
Full license text available in "LICENSE" file packaged with the program.
"""
import re
from datetime import date
from typing import Any

import anki.cards
import aqt.reviewer
from anki.consts import QUEUE_TYPE_SUSPENDED, QUEUE_TYPE_REV, QUEUE_TYPE_NEW

from .consts import Config, Action, Macro, LEECH_TAG, CARD_TYPE_STR


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

    def __init__(self, reviewer: aqt.reviewer.Reviewer, deck_id: int, user_conf: dict[str, Any]):
        # Deck Conf = (Config for Deck's Options Group or None)
        self.reviewer = reviewer
        # self.deck_config = _
        self.user_config = user_conf

    # Leech actions json: action: {enabled: bool, key: val}
    def leech_update(self, card: anki.cards.Card, debug=False):
        updated_card = card.col.get_card(card.id)
        leech_actions = self.user_config[Config.LEECH_ACTIONS]

        if leech_actions[Action.FLAG][Action.ENABLED]:
            updated_card.set_user_flag(leech_actions[Action.FLAG][Action.INPUT])

        if leech_actions[Action.SUSPEND][Action.ENABLED]:
            updated_card.queue = QUEUE_TYPE_SUSPENDED if leech_actions[Action.SUSPEND][Action.INPUT] else QUEUE_TYPE_REV

        if leech_actions[Action.ADD_TAGS][Action.ENABLED]:
            for tag in str(leech_actions[Action.ADD_TAGS][Action.INPUT]).split(' '):
                updated_card.note().add_tag(get_formatted_tag(updated_card, tag))

        if leech_actions[Action.REMOVE_TAGS][Action.ENABLED]:
            for tag in leech_actions[Action.REMOVE_TAGS][Action.INPUT].split(' '):
                # Formats the tag's macros then retrieves the regex pattern and replaces it from the tags string
                formatted_tag = get_formatted_tag(updated_card, tag)
                if re.search(f'(?<!%){Macro.REGEX}:.*', formatted_tag):
                    reg_cmd = formatted_tag.replace(f'{Macro.REGEX}:', '', 1)
                    reg_match = re.search(f'((?<=^\")(.*)(?=\"$))|(^(?!\")(.*))', reg_cmd)
                    reg_string = reg_match.group(0).replace(f'.', r'\S')
                    result_tags = re.sub(fr'(?<!\S){reg_string}(?!\S)', '', updated_card.note().string_tags()).strip()
                    updated_card.note().set_tags_from_str(result_tags)
                else:
                    updated_card.note().remove_tag(formatted_tag)

        forget_input = leech_actions[Action.FORGET][Action.INPUT]
        if leech_actions[Action.FORGET][Action.ENABLED] and forget_input[0]:
            updated_card.odid = 0 if updated_card.odid else updated_card.odid
            updated_card.odue = 0 if forget_input[1] else updated_card.odue
            updated_card.reps, updated_card.lapses = (0, 0) if forget_input[2] else (updated_card.reps, updated_card.lapses)

        # if leech_actions[Action.EDIT_FIELDS][Action.ENABLED]:
        #     inputs: list[str] = leech_actions[Action.EDIT_FIELDS][Action.INPUT]
        #     for filtered_nid in inputs:
        #         nid = int(filtered_nid.split('.')[0])
        #         if card.note_type()['id'] == nid:
        #             print(f'note_meta: {leech_actions[Action.EDIT_FIELDS][Action.INPUT][filtered_nid]}')
        #             note_meta = leech_actions[Action.EDIT_FIELDS][Action.INPUT][filtered_nid]
        #             card_fields = card.note().fields
        #
        #             if note_meta[Action.Fields.METHOD] == Action.Fields.APPEND:
        #                 card_fields[note_meta[Action.Fields.FIELD]] += (note_meta[Action.Fields.TEXT])
        #             if note_meta[Action.Fields.METHOD] == Action.Fields.PREPEND:
        #                 pass
        #             if note_meta[Action.Fields.METHOD] == Action.Fields.REPLACE:
        #                 pass
        #             if note_meta[Action.Fields.METHOD] == Action.Fields.REGEX:
        #                 pass

        return updated_card


def forget_card(card: anki.cards.Card, reset_pos=False, reset_reviews=False):
    """
Forgets the card via a database call. Mimics Anki's methods without using its generated code.
    :param card: card to forget
    :param reset_pos: if the card's position should try to be reset to its original import position
    :param reset_reviews: if the card's lapse/review count should try to be reset back to 0
    """
