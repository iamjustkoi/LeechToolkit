"""
MIT License: Copyright (c) 2022 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
Full license text available in "LICENSE" file packaged with the program.
"""
import datetime
import random
import re
from datetime import date
from difflib import SequenceMatcher
from typing import Any

import anki.cards
import aqt.reviewer
from anki.consts import QUEUE_TYPE_SUSPENDED, QUEUE_TYPE_NEW, CARD_TYPE_NEW

from .consts import Config, Action, Macro, EditAction, RescheduleAction, QueueAction


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
    def leech_update(self, card: anki.cards.Card):
        updated_card = card.col.get_card(card.id)
        leech_actions = self.user_config[Config.LEECH_ACTIONS]

        if leech_actions[Action.FLAG][Action.ENABLED]:
            updated_card.set_user_flag(leech_actions[Action.FLAG][Action.INPUT])

        if leech_actions[Action.SUSPEND][Action.ENABLED] and leech_actions[Action.SUSPEND][Action.INPUT]:
            updated_card.queue = QUEUE_TYPE_SUSPENDED

        if leech_actions[Action.ADD_TAGS][Action.ENABLED]:
            for tag in str(leech_actions[Action.ADD_TAGS][Action.INPUT]).split(' '):
                updated_card.note().add_tag(get_formatted_tag(updated_card, tag))

        if leech_actions[Action.REMOVE_TAGS][Action.ENABLED]:
            for tag in leech_actions[Action.REMOVE_TAGS][Action.INPUT].split(' '):

                # Formats the tag's macros then retrieves the regex pattern and replaces it from the tags string
                formatted_tag = get_formatted_tag(updated_card, tag)

                if re.search(f'(?<!%){Macro.REGEX}:.*', formatted_tag):
                    reg_cmd = formatted_tag.replace(f'{Macro.REGEX}:', '', 1)
                    # Replace "everything" character with the "no spaces" character
                    reg_match = re.search(f'((?<=^\")(.*)(?=\"$))|(^(?!\")(.*))', reg_cmd)
                    reg_string = reg_match.group(0).replace(f'.', r'\S')
                    # Remove tags from the tags string
                    result_tags = ''.join(re.split(reg_string, updated_card.note().string_tags())).strip()
                    updated_card.note().set_tags_from_str(result_tags)
                else:
                    updated_card.note().remove_tag(formatted_tag)

        if leech_actions[Action.FORGET][Action.ENABLED] and leech_actions[Action.FORGET][Action.INPUT][0]:
            if updated_card.odid:
                updated_card.odid = 0
            if leech_actions[Action.FORGET][Action.INPUT][1]:
                updated_card.odue = 0
            if leech_actions[Action.FORGET][Action.INPUT][2]:
                updated_card.reps = 0
                updated_card.lapses = 0

        if leech_actions[Action.EDIT_FIELDS][Action.ENABLED]:
            inputs: list[str] = leech_actions[Action.EDIT_FIELDS][Action.INPUT]

            for filtered_nid in inputs:
                nid = int(filtered_nid.split('.')[0])
                if updated_card.note_type()['id'] == nid:
                    conf_meta = leech_actions[Action.EDIT_FIELDS][Action.INPUT][filtered_nid]

                    new_text: str = conf_meta[EditAction.TEXT]
                    card_field = updated_card.note().fields[conf_meta[EditAction.FIELD]]

                    if conf_meta[EditAction.METHOD] == EditAction.APPEND_METHOD:
                        card_field += new_text
                    if conf_meta[EditAction.METHOD] == EditAction.PREPEND_METHOD:
                        card_field = new_text + card_field
                    if conf_meta[EditAction.METHOD] == EditAction.REPLACE_METHOD:
                        card_field = card_field.replace(conf_meta[EditAction.REPL], new_text)
                    if conf_meta[EditAction.METHOD] == EditAction.REGEX_METHOD:
                        card_field = new_text.join(re.split(conf_meta[EditAction.REPL], card_field))

                    updated_card.note().fields[conf_meta[EditAction.FIELD]] = card_field

        if leech_actions[Action.MOVE_TO_DECK][Action.ENABLED]:
            # If the card was also in a cram/custom study deck, set it back to its original deck and due date:
            updated_card.odid = 0
            if updated_card.odue:
                updated_card.due = updated_card.odue
                updated_card.odue = 0

            updated_card.did = int(leech_actions[Action.MOVE_TO_DECK][Action.INPUT])

        if leech_actions[Action.RESCHEDULE][Action.ENABLED]:
            from_days = leech_actions[Action.RESCHEDULE][Action.INPUT][RescheduleAction.FROM]
            to_days = leech_actions[Action.RESCHEDULE][Action.INPUT][RescheduleAction.TO]
            days = random.randrange(from_days, to_days) if from_days < to_days else random.randrange(to_days, from_days)
            delta = datetime.timedelta(days=days)
            updated_card.due = int((datetime.datetime.now() + delta).timestamp())

            if leech_actions[Action.RESCHEDULE][Action.INPUT][RescheduleAction.RESET]:
                updated_card.ivl = delta.days

        if leech_actions[Action.ADD_TO_QUEUE][Action.ENABLED]:
            queue_inputs = leech_actions[Action.ADD_TO_QUEUE][Action.INPUT]

            def get_inserted_pos(insert_type, input_pos):
                if insert_type != QueueAction.POS:
                    queue_cmd = f'SELECT min(due), max(due) from cards where type={CARD_TYPE_NEW} and odid=0'
                    top, bottom = card.col.db.first(queue_cmd)
                    queue_pos = top if insert_type == QueueAction.TOP else bottom
                    return queue_pos + input_pos if (queue_pos + input_pos > 0) else queue_pos
                return input_pos

            from_pos = get_inserted_pos(queue_inputs[QueueAction.FROM_INDEX], queue_inputs[QueueAction.FROM_VAL])
            to_pos = get_inserted_pos(queue_inputs[QueueAction.TO_INDEX], queue_inputs[QueueAction.TO_VAL])

            # Swap positions if values are inverted/will result in a non-positive range
            from_pos, to_pos = (to_pos, from_pos) if from_pos > to_pos else (from_pos, to_pos)

            filtered_ids, filtered_positions = [], []
            if queue_inputs[QueueAction.NEAR_SIBLING] or queue_inputs[QueueAction.NEAR_SIMILAR]:
                cmd = f'''
                    SELECT id, due FROM cards
                    WHERE id != {updated_card.id}
                    AND due BETWEEN {from_pos} AND {to_pos}
                '''

                if queue_inputs[QueueAction.NEAR_SIBLING]:
                    cmd += f'''    AND nid = {updated_card.nid} AND queue = {QUEUE_TYPE_NEW}'''

                filtered_data = card.col.db.all(cmd)
                for row in filtered_data:
                    filtered_ids.append(row[0])
                    filtered_positions.append(row[1])

                # Gets the string output of each card's data currently in the new queue and compares to the leech
                #  using a ratio/fuzzy comparison.
                if queue_inputs[QueueAction.NEAR_SIMILAR]:
                    to_strip = queue_inputs[QueueAction.EXCLUDED_TEXT]
                    similar_ratio = .5

                    excluded_fields: list[str] = []
                    for note_dict in queue_inputs[QueueAction.EXCLUDED_FIELDS]:
                        note_type_id = int(list(note_dict)[0])
                        if note_type_id == updated_card.note().mid:
                            excluded_fields += list(note_dict.keys())

                    leech_field_data = [item[1] for item in updated_card.note().items() if item[0] not in
                                        excluded_fields]

                    for cid in filtered_ids:
                        new_card = card.col.get_card(cid)
                        if new_card.note_type()['id'] != updated_card.note().mid:
                            filtered_positions.remove(new_card.due)
                        else:
                            new_field_data = [
                                item[1] for item in new_card.note().items() if item[0] not in excluded_fields
                            ]

                            leech_data_str = ''.join(char for char in str(leech_field_data) if char not in to_strip)
                            new_data_str = ''.join(char for char in str(new_field_data) if char not in to_strip)

                            # Not similar enough
                            if SequenceMatcher(None, leech_data_str, new_data_str).ratio() < similar_ratio:
                                filtered_positions.remove(new_card.due)

            updated_card.queue = QUEUE_TYPE_NEW
            updated_card.type = CARD_TYPE_NEW
            if len(filtered_positions) > 0:
                updated_card.due = random.choice(filtered_positions)
            else:
                updated_card.due = random.randrange(from_pos, to_pos) if from_pos != to_pos else from_pos

        return updated_card
