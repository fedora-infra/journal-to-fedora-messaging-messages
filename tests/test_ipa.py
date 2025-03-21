# SPDX-FileCopyrightText: 2025 Contributors to the Fedora Project
#
# SPDX-License-Identifier: LGPL-3.0-or-later

"""Unit tests for the message schema."""

from itertools import chain

import pytest

from journal_to_fedora_messaging_messages.ipa import IpaUserAddV1


@pytest.fixture
def ipa_message_user_add():
    return {
        "_BOOT_ID": "7cf5624e8b3e487986fbd6c1763b8b72",
        "CODE_LINE": "495",
        "CODE_FUNC": "__audit_to_journal",
        "IPA_API_RESULT": "SUCCESS",
        "_SELINUX_CONTEXT": "system_u:system_r:httpd_t:s0",
        "_CAP_EFFECTIVE": "0",
        "_HOSTNAME": "ipa.example.com",
        "_TRANSPORT": "journal",
        "_EXE": "/usr/sbin/httpd",
        "_SYSTEMD_UNIT": "httpd.service",
        "MESSAGE": (
            "[IPA.API] noggin@FEDORAPROJECT.ORG: user_add: SUCCESS [ldap2_140525848914048] "
            '{"uid": "dummy", "givenname": "Dummy", "sn": "User", "cn": "Dummy User", '
            '"displayname": "Dummy User", "initials": "DU", "gecos": "Dummy User", "loginshell": '
            '"/bin/bash", "krbprincipalname": ["dummy@FEDORAPROJECT.ORG"], "mail": '
            '["dummy@example.com"], "random": false, "fastimezone": "UTC", "faslocale": "en-US", '
            '"fasstatusnote": "active", "fascreationtime": {"__datetime__": "20250320000000Z"}, '
            '"all": true, "raw": false, "version": "2.253", "no_members": false}'
        ),
        "_PID": "160139",
        "SYSLOG_IDENTIFIER": "/mod_wsgi",
        "_SYSTEMD_SLICE": "system.slice",
        "PRIORITY": "5",
        "IPA_API_PARAMS": (
            '{"uid": "dummy", "givenname": "Dummy", "sn": "User", "cn": "Dummy User", '
            '"displayname": "Dummy User", "initials": "DU", "gecos": "Dummy User", "loginshell": '
            '"/bin/bash", "krbprincipalname": ["dummy@FEDORAPROJECT.ORG"], "mail": '
            '["dummy@example.com"], "random": false, "fastimezone": "UTC", "faslocale": "en-US", '
            '"fasstatusnote": "active", "fascreationtime": {"__datetime__": "20250320000000Z"}, '
            '"all": true, "raw": false, "version": "2.253", "no_members": false}'
        ),
        "_GID": "387",
        "_MACHINE_ID": "b494e31dbf2749d7934819780b396d66",
        "__REALTIME_TIMESTAMP": "1742430579781629",
        "IPA_API_ACTOR": "noggin@FEDORAPROJECT.ORG",
        "CODE_FILE": "/usr/lib/python3.9/site-packages/ipalib/frontend.py",
        "_SOURCE_REALTIME_TIMESTAMP": "1742430579781599",
        "_CMDLINE": '"(wsgi:ipa)     " -DFOREGROUND',
        "_RUNTIME_SCOPE": "system",
        "IPA_API_COMMAND": "user_add",
        "_SYSTEMD_INVOCATION_ID": "d67f3e6ec1f1463cba99b2baf5a5cb63",
        "MESSAGE_ID": "6d70f1b493df36478bc3499257cd3b17",
        "_COMM": "httpd",
        "_UID": "387",
        "_SYSTEMD_CGROUP": "/system.slice/httpd.service",
    }


def test_user_add(ipa_message_user_add):
    """
    Assert the message schema validates a message with the required fields.
    """
    message = IpaUserAddV1(body=ipa_message_user_add)
    message.validate()
    assert message.app_name == "IPA"
    assert message.app_icon == "https://apps.fedoraproject.org/img/icons/ipa.png"
    assert message.url is None
    assert message.agent_name == "noggin"
    assert message.username == "dummy"
    assert message.result == "SUCCESS"
    assert message.summary == 'noggin created user "dummy"'
    assert str(message) == "A new user has been created: dummy\nBy: noggin\n"

    # Some data must be redacted
    for values in chain(message.body.values(), message._params):
        assert "dummy@example.com" not in values
