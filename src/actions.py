"""
MIT License: Copyright (c) 2022 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
Full license text available in "LICENSE" file packaged with the program.
"""
import datetime
import random
import re
from datetime import date
from difflib import SequenceMatcher

import anki.cards
from anki.consts import QUEUE_TYPE_SUSPENDED, QUEUE_TYPE_NEW, CARD_TYPE_NEW

from .consts import Action, Macro, EditAction, RescheduleAction, QueueAction


def get_formatted_tag(card: anki.cards.Card, tag: str):
    result = tag

    macro = Macro.DATE
    if re.search(fr'(?<!%){macro}', tag):
        result = result.replace(macro, str(date.today()))

    macro = Macro.REVIEWS
    if re.search(fr'(?<!%){macro}', tag):
        cmd = f'SELECT reps FROM cards WHERE id is {card.id}'
        result = result.replace(macro, str(card.col.db.scalar(cmd)))

    macro = r'%%'
    if re.search(macro, tag):
        result = result.replace(macro, '%')

    return result


# Actions format: actionName: {enabled: bool, key: val}
def run_actions(card: anki.cards.Card, actions_conf: dict, reload=True):
    updated_card = card.col.get_card(card.id) if reload else card

    if actions_conf[Action.FLAG][Action.ENABLED]:
        updated_card.set_user_flag(actions_conf[Action.FLAG][Action.INPUT])

    if actions_conf[Action.SUSPEND][Action.ENABLED] and actions_conf[Action.SUSPEND][Action.INPUT]:
        updated_card.queue = QUEUE_TYPE_SUSPENDED

    if actions_conf[Action.ADD_TAGS][Action.ENABLED]:
        for tag in str(actions_conf[Action.ADD_TAGS][Action.INPUT]).split(' '):
            updated_card.note().add_tag(get_formatted_tag(updated_card, tag))

    if actions_conf[Action.REMOVE_TAGS][Action.ENABLED]:
        for tag in actions_conf[Action.REMOVE_TAGS][Action.INPUT].split(' '):

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

    if actions_conf[Action.FORGET][Action.ENABLED] and actions_conf[Action.FORGET][Action.INPUT][0]:
        if updated_card.odid:
            updated_card.odid = 0
        if actions_conf[Action.FORGET][Action.INPUT][1]:
            updated_card.odue = 0
        if actions_conf[Action.FORGET][Action.INPUT][2]:
            updated_card.reps = 0
            updated_card.lapses = 0

    if actions_conf[Action.EDIT_FIELDS][Action.ENABLED]:
        inputs: list[str] = actions_conf[Action.EDIT_FIELDS][Action.INPUT]

        for filtered_nid in inputs:
            nid = int(filtered_nid.split('.')[0])
            if updated_card.note_type()['id'] == nid:
                conf_meta = actions_conf[Action.EDIT_FIELDS][Action.INPUT][filtered_nid]

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

    if actions_conf[Action.MOVE_DECK][Action.ENABLED]:
        # If the card was also in a cram/custom study deck, set it back to its original deck and due date:
        updated_card.odid = 0
        if updated_card.odue:
            updated_card.due = updated_card.odue
            updated_card.odue = 0

        if actions_conf[Action.MOVE_DECK][Action.INPUT]:
            updated_card.did = int(actions_conf[Action.MOVE_DECK][Action.INPUT])

    if actions_conf[Action.RESCHEDULE][Action.ENABLED]:
        from_days = actions_conf[Action.RESCHEDULE][Action.INPUT][RescheduleAction.FROM]
        to_days = actions_conf[Action.RESCHEDULE][Action.INPUT][RescheduleAction.TO]
        days = random.randrange(from_days, to_days) if from_days < to_days else random.randrange(to_days, from_days)
        delta = datetime.timedelta(days=days)
        updated_card.due = int((datetime.datetime.now() + delta).timestamp())

        if actions_conf[Action.RESCHEDULE][Action.INPUT][RescheduleAction.RESET]:
            updated_card.ivl = delta.days

    if actions_conf[Action.ADD_TO_QUEUE][Action.ENABLED]:
        queue_inputs = actions_conf[Action.ADD_TO_QUEUE][Action.INPUT]

        def get_inserted_pos(insert_type, input_pos):
            """
        Retrieves the position for the given insert type.
            :param insert_type: type of insertion to use to determine the position output
            :param input_pos: extra position value to add to/insert with the position value returned
            :return: retrieved position number
            """
            if insert_type != QueueAction.POS:
                queue_cmd = f'SELECT min(due), max(due) from cards where type={CARD_TYPE_NEW} and odid=0'
                top, bottom = card.col.db.first(queue_cmd)
                queue_pos = top if insert_type == QueueAction.TOP else bottom
                return queue_pos + input_pos if (queue_pos + input_pos > 0) else queue_pos
            return input_pos

        from_pos = get_inserted_pos(queue_inputs[QueueAction.FROM_INDEX], queue_inputs[QueueAction.FROM_VAL])
        to_pos = get_inserted_pos(queue_inputs[QueueAction.TO_INDEX], queue_inputs[QueueAction.TO_VAL])

        # Swap positions if value range non-positive
        from_pos, to_pos = (to_pos, from_pos) if from_pos > to_pos else (from_pos, to_pos)

        filtered_ids, filtered_positions = [], []
        if queue_inputs[QueueAction.NEAR_SIBLING] or queue_inputs[QueueAction.NEAR_SIMILAR]:

            cmd = f'''
                SELECT {{get}} FROM cards
                WHERE id != {updated_card.id}
                AND did == {updated_card.did}
                AND due BETWEEN {from_pos} AND {to_pos}
            '''

            if queue_inputs[QueueAction.NEAR_SIBLING]:
                cmd += f'    AND nid = {updated_card.nid} AND queue = {QUEUE_TYPE_NEW}'
            else:
                cmd += f'    AND nid != {updated_card.nid}'

            filtered_ids = card.col.db.list(cmd.format(get='id'))
            filtered_positions = card.col.db.list(cmd.format(get='due'))

            # Gets the string output of each card's data currently in the new queue and compares to the leech
            #  using ratios/fuzzy comparison.
            if queue_inputs[QueueAction.NEAR_SIMILAR]:
                excluded_inputs_str: str = queue_inputs[QueueAction.EXCLUDED_TEXT]
                excluded_inputs = re.sub('  +', ' ', excluded_inputs_str).replace('\n', ' ').split(' ')

                min_ratio = queue_inputs[QueueAction.SIMILAR_RATIO]

                filtered_field_ords: list[int] = []
                for note_dict in queue_inputs[QueueAction.FILTERED_FIELDS]:
                    note_type_id = int(list(note_dict)[0])

                    if note_type_id == updated_card.note().mid:
                        [filtered_field_ords.append(int(note_dict[key])) for key in list(note_dict.keys())]

                def get_filtered_card_data(items: list[(str, str)]):
                    # for item in items:
                    filtered_items = []
                    # INCLUDE
                    if queue_inputs[QueueAction.INCLUSIVE_FIELDS]:
                        for field_ord in filtered_field_ords:
                            filtered_items.append(items[field_ord][1])
                    # EXCLUDE
                    if not queue_inputs[QueueAction.INCLUSIVE_FIELDS]:
                        for item in items:
                            if item[0] not in filtered_field_ords:
                                filtered_items.append(item[1])

                    filtered_str = ''.join(filtered_items)
                    for excluded_str in excluded_inputs:
                        excluded_str = ' ' if excluded_str == '\\s' else excluded_str
                        filtered_str = filtered_str.replace(excluded_str, '')

                    return filtered_str

                leech_data_str = get_filtered_card_data(updated_card.note().items())

                for cid in filtered_ids:
                    new_card = card.col.get_card(cid)
                    is_similar_card = False

                    if new_card.note_type()['id'] == updated_card.note().mid:
                        new_data_str = get_filtered_card_data(new_card.note().items())

                        if SequenceMatcher(None, leech_data_str, new_data_str).ratio() >= min_ratio:
                            is_similar_card = True

                    if not is_similar_card:
                        filtered_positions.remove(new_card.due)

        updated_card.queue = QUEUE_TYPE_NEW
        updated_card.type = CARD_TYPE_NEW
        if len(filtered_positions) > 0:
            updated_card.due = random.choice(filtered_positions)
        else:
            updated_card.due = random.randrange(from_pos, to_pos) if from_pos != to_pos else from_pos

    return updated_card
