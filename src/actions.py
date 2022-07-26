"""
MIT License: Copyright (c) 2022 JustKoi (iamjustkoi) <https://github.com/iamjustkoi>
Full license text available in "LICENSE" file packaged with the program.
"""
from typing import Any

import aqt.reviewer

# actions object:

# init (Reviewer, Deck):
#     deck_conf = _
#       deck-specific
#     user_conf = _
#       general

# do_leech (Card):

# do_reverse (Card):


class ToolkitActions:

    def __init__(self, reviewer: aqt.reviewer.Reviewer, deck_id: int, user_conf: dict[str, Any]):
        # Deck Conf = (Config for Deck's Options Group or None)
        # User Conf = config
        self.reviewer = reviewer
        self.user_config = user_conf
