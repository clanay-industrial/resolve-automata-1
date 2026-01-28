import os
from urllib import response
from dotenv  import load_dotenv
from fastapi import FastAPI, Query, Response, Request
from pydantic import BaseModel
from typing import Annotated

load_dotenv()

# from services.sql import engine
from services.agent import agent_service
from models.whatsapp import WhatsAppWebhook_Message
from models.hub import Hub
from services.whatsapp_utility import strip_whatsapp_token
from services.whatsapp_api import send_whatsapp_textonly_message
import services.sql

# import whatsapp_routes.py

whatsapp_token = os.environ.get('WHATSAPP_TOKEN')
whatsapp_business_phone_number_id = os.environ.get('WHATSAPP_BUSINESS_PHONE_NUMBER_ID')

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


class Message(BaseModel):
    user: str
    message: str

@app.post("/activity")
async def activity(message: Message):

    response = await agent_service.process_message(message.user, message.message)

    return {"message": response.content, "user": message.user}

@app.get("/health")
async def health(response: Response):
    response.status_code = 200
    return {"status": "healthy"}


@app.get("/api/whatsapp/", status_code=200)
def token_verify(
        hub: Annotated[Hub, Query()],
        response: Response
    ):
        # logger.info(hub)
        print(hub)
        
        if hub.hub_mode == "None":
            response.status_code = 200
            return response

        stripped_hub_verify_token = strip_whatsapp_token(hub.hub_verify_token)

        if stripped_hub_verify_token == None:
            response.status_code = 200
            return response

        if hub.hub_mode == "subscribe" and stripped_hub_verify_token == whatsapp_token:
            # logger.info("Webhook verified")
            print("Webhook verified")
            return Response(content=hub.hub_challenge or "", media_type="text/plain")

        response.status_code = 403
        return {"status": "forbidden"}


@app.post("/api/whatsapp/", status_code=200)
async def post_message(request: Request, response: Response):
    # Log a small summary (timestamp is not present at top level in this payload)
    # logger.debug("\n\nWebhook received payload:\n")
    print("\n\nWebhook received payload:\n")

    # Return 200 with no body to match the original JS behaviour
    body = await request.body()
    converted_body = None

    try: 
        converted_body = WhatsAppWebhook_Message.model_validate_json(json_data=body, strict=False)
    except Exception as e:
        # logger.warning(f"Failed to parse WhatsAppWebhook_Message")
        # logger.debug(e)
        # logger.debug(body)
        print(f"Failed to parse WhatsAppWebhook_Message")
        print(e)
        print(body)
        response.status_code = 500
        return response

    if converted_body is None:
        response.status_code = 400
        return response


    message = converted_body.entry[0].changes[0].value.messages[0]
    customer = message.from_

    # logger.debug("Received message:")
    # logger.debug(message.text.body)
    print("Received message:")
    print(message.text.body)

    # message = generate_response(message.text.body)

    # Replace with formatted Agent Response 
    message = "dummy message"

    # logger.debug(f"Response message:\n{message}")
    print(f"Response message:\n{message}")

    await send_whatsapp_textonly_message(
        whatsapp_business_id=whatsapp_business_phone_number_id,
        whatsapp_authtoken=whatsapp_token, 
        user_phone_number=customer, 
        message=message)

    response.status_code = 200
    return response