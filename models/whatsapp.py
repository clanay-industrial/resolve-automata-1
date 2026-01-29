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


class ConversationOrigin(BaseModel):
    type: Optional[str]


class Conversation(BaseModel):
    id: Optional[str]
    origin: Optional[ConversationOrigin]
    expiration_timestamp: Optional[str]


class Pricing(BaseModel):
    billable: Optional[bool]
    pricing_model: Optional[str]
    category: Optional[str]
    type: Optional[str]


class StatusItem(BaseModel):
    id: Optional[str]
    status: Optional[str]
    timestamp: Optional[str]
    recipient_id: Optional[str]
    recipient_logical_id: Optional[str]
    conversation: Optional[Conversation]
    pricing: Optional[Pricing]


class Value(BaseModel):
    messaging_product: Optional[str]
    metadata: Optional[Metadata]
    contacts: Optional[List[Contact]]
    messages: Optional[List[MessageItem]]
    statuses: Optional[List[StatusItem]]


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