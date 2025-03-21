# SPDX-FileCopyrightText: 2025 Contributors to the Fedora Project
#
# SPDX-License-Identifier: LGPL-3.0-or-later

import json
import re
import typing

from fedora_messaging import message

from .base import JOURNAL_SCHEMA, SCHEMA_URL


IPA_JOURNAL_FIELDS = (
    "IPA_API_ACTOR",
    "IPA_API_COMMAND",
    "IPA_API_PARAMS",
    "IPA_API_RESULT",
)
IPA_SCHEMA = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "object",
    "properties": {
        **JOURNAL_SCHEMA["properties"],
        **{field: {"type": "string"} for field in IPA_JOURNAL_FIELDS},
    },
    "required": [*JOURNAL_SCHEMA["required"], *IPA_JOURNAL_FIELDS],
}

REDACT_FIELDS = ("MESSAGE", "IPA_API_PARAMS")
REDACT_EXPRS = (re.compile(r", \"mail\": \[[^\]]*\]"),)


class IpaMessage(message.Message):
    """
    A sub-class of a Fedora message that defines a message schema for messages
    published by IPA.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in REDACT_FIELDS:
            for expr in REDACT_EXPRS:
                self.body[field] = expr.sub("", self.body[field])
        self._params = json.loads(self.body["IPA_API_PARAMS"])

    @property
    def app_name(self):
        return "IPA"

    @property
    def app_icon(self):
        return "https://apps.fedoraproject.org/img/icons/ipa.png"

    @property
    def agent_name(self):
        """The username of the user who initiated the action that generated this message."""
        return self.body["IPA_API_ACTOR"].partition("@")[0]

    @property
    def result(self):
        return self.body["IPA_API_RESULT"]


class IpaUserAddV1(IpaMessage):
    """
    A sub-class of a Fedora message that defines a message schema for messages
    published by IPA when a new user is created.
    """

    topic = "ipa.user_add.v1"
    body_schema: typing.ClassVar = {
        "id": SCHEMA_URL + topic,
        "description": "Schema for messages sent when a new user is created",
        **IPA_SCHEMA,
    }

    @property
    def username(self):
        """The username that was created."""
        return self._params["uid"]

    def __str__(self):
        """Return a complete human-readable representation of the message."""
        return f"A new user has been created: {self.username}\nBy: {self.agent_name}\n"

    @property
    def summary(self):
        """Return a summary of the message."""
        return f'{self.agent_name} created user "{self.username}"'
