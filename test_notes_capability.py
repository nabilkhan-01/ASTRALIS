from astralis.capability.notes import NotesCapability

from tests.helpers.conversation_factory import (
    create_conversation,
)
from tests.helpers.interpretation_factory import (
    create_interpretation,
)
from tests.helpers.request_factory import (
    create_request,
)

capability = NotesCapability()

print(
    capability.execute(
        create_request("note Buy milk"),
        create_conversation(),
        create_interpretation(),
    ).text
)

print(
    capability.execute(
        create_request("note Complete DSA"),
        create_conversation(),
        create_interpretation(),
    ).text
)

print(
    capability.execute(
        create_request("notes"),
        create_conversation(),
        create_interpretation(),
    ).text
)

print(
    capability.execute(
        create_request("delete note 1"),
        create_conversation(),
        create_interpretation(),
    ).text
)

print(
    capability.execute(
        create_request("notes"),
        create_conversation(),
        create_interpretation(),
    ).text
)