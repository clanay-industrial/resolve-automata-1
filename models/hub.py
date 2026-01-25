from typing import Union
from pydantic import BaseModel
from fastapi import Query


class Hub(BaseModel):
    hub_mode: Union[str, None] = Query(None, alias="hub.mode")
    hub_challenge: Union[str, None] = Query(None, alias="hub.challenge")
    hub_verify_token: Union[str, None] = Query(None, alias="hub.verify_token")
