from typing import List, Optional
from pydantic import BaseModel, Field


class Metadata(BaseModel):
    display_phone_number: Optional[str] = None
    phone_number_id: Optional[str] = None


class Profile(BaseModel):
    name: Optional[str] = None


class Contact(BaseModel):
    profile: Optional[Profile] = None
    wa_id: Optional[str] = None


class TextContent(BaseModel):
    body: Optional[str] = None


class MessageItem(BaseModel):
    # `from` is a reserved word in Python; use from_ and map it to JSON `from`
    from_: Optional[str] = Field(None, alias="from")
    id: Optional[str] = None
    timestamp: Optional[str] = None
    type: Optional[str] = None
    text: Optional[TextContent] = None


class ConversationOrigin(BaseModel):
    type: Optional[str] = None


class Conversation(BaseModel):
    id: Optional[str] = None
    origin: Optional[ConversationOrigin] = None
    expiration_timestamp: Optional[str] = None


class Pricing(BaseModel):
    billable: Optional[bool] = None
    pricing_model: Optional[str] = None
    category: Optional[str] = None
    type: Optional[str] = None


class StatusItem(BaseModel):
    id: Optional[str] = None
    status: Optional[str] = None
    timestamp: Optional[str] = None
    recipient_id: Optional[str] = None
    recipient_logical_id: Optional[str] = None
    conversation: Optional[Conversation] = None
    pricing: Optional[Pricing] = None


class Value(BaseModel):
    messaging_product: Optional[str] = None
    metadata: Optional[Metadata] = None
    contacts: Optional[List[Contact]] = None
    messages: Optional[List[MessageItem]] = None
    statuses: Optional[List[StatusItem]] = None


class ChangeItem(BaseModel):
    field: Optional[str] = None
    value: Optional[Value] = None


class EntryItem(BaseModel):
    id: Optional[str] = None
    changes: Optional[List[ChangeItem]] = None


class WhatsAppWebhook(BaseModel):
    object: Optional[str] = None
    entry: Optional[List[EntryItem]] = None

    class ConfigDict:
        populate_by_name = True


# Backwards-compatible alias used elsewhere in codebase
WhatsAppWebhook_Message = WhatsAppWebhook