from enum import Enum


class EntityType(
    Enum,
):
    """Defines the types of entities known to ASTRALIS."""

    USER = "user"
    PROJECT = "project"

    NOTE = "note"
    CALENDAR_EVENT = "calendar_event"
    ALARM = "alarm"