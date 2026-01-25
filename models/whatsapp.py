from typing import List, Optional
from pydantic import BaseModel, Field


class Metadata(BaseModel):
    display_phone_number: Optional[str]
    phone_number_id: Optional[str]


class Profile(BaseModel):
    name: Optional[str]


class Contact(BaseModel):
    profile: Optional[Profile]
    wa_id: Optional[str]


class TextContent(BaseModel):
    body: Optional[str]


class MessageItem(BaseModel):
    # `from` is a reserved word in Python; use from_ and map it to JSON `from`
    from_: Optional[str] = Field(None, alias="from")
    id: Optional[str]
    timestamp: Optional[str]
    type: Optional[str]
    text: Optional[TextContent]


class Value(BaseModel):
    messaging_product: Optional[str]
    metadata: Optional[Metadata]
    contacts: Optional[List[Contact]]
    messages: Optional[List[MessageItem]]


class ChangeItem(BaseModel):
    field: Optional[str]
    value: Optional[Value]


class EntryItem(BaseModel):
    id: Optional[str]
    changes: Optional[List[ChangeItem]]


class WhatsAppWebhook(BaseModel):
    object: Optional[str]
    entry: Optional[List[EntryItem]]

    class ConfigDict:
        validate_by_name = True


# Backwards-compatible alias used elsewhere in codebase
WhatsAppWebhook_Message = WhatsAppWebhook