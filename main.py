import os
import copy
import logging
from uvicorn.config import LOGGING_CONFIG as UVICORN_LOGGING_CONFIG
from urllib import response
from dotenv  import load_dotenv
from fastapi import FastAPI, Query, Response, Request
from typing import Annotated

load_dotenv()

from models.utility_models import Message  
from services.agent import agent_service
from models.whatsapp import WhatsAppWebhook_Message
from models.hub import Hub
from services.whatsapp_utility import strip_whatsapp_token
from services.whatsapp_api import send_whatsapp_textonly_message
import services.sql
from models.welcome_message import welcome_message

whatsapp_token = os.environ.get('WHATSAPP_TOKEN')
whatsapp_business_phone_number_id = os.environ.get('WHATSAPP_BUSINESS_PHONE_NUMBER_ID')
log_level = int(os.environ.get('LOG_LEVEL',"40"))

LOGGING = copy.deepcopy(UVICORN_LOGGING_CONFIG)
LOGGING.setdefault("disable_existing_loggers", False)
# add your app logger using Uvicorn's default handler name
LOGGING["loggers"]["resolveautomata"] = {
    "handlers": ["default"],
    "level": log_level,
    "propagate": False
}

logging.config.dictConfig(LOGGING)
logger = logging.getLogger("resolveautomata")

logger.info("Starting FastAPI app :)")

app = FastAPI()

@app.get("/")
async def root():
    logger.debug("Root endpoint called")
    return {"message": "Hello World"}

@app.post("/activity")
async def activity(message: Message):
    if message.auth_token != whatsapp_token:
        logger.warning("Unauthorized access attempt with invalid auth token")
        return Response(status_code=403, content="Forbidden")

    logger.debug(f"Processing activity message: {message}")

    response = await agent_service.process_message(message.user, message.message)

    return {"message": response.content, "user": message.user}

@app.get("/health")
async def health(response: Response):
    logger.debug("Health check endpoint called")

    response.status_code = 200
    return {"status": "healthy"}


@app.get("/api/whatsapp/", status_code=200)
def token_verify(
        hub: Annotated[Hub, Query()],
        response: Response
    ):
        logger.info(hub)
        
        if hub.hub_mode == "None":
            response.status_code = 200
            return response

        stripped_hub_verify_token = strip_whatsapp_token(hub.hub_verify_token)

        if stripped_hub_verify_token == None:
            response.status_code = 200
            return response

        if hub.hub_mode == "subscribe" and stripped_hub_verify_token == whatsapp_token:
            logger.info("Webhook verified")
            return Response(content=hub.hub_challenge or "", media_type="text/plain")

        response.status_code = 403
        return {"status": "forbidden"}


@app.post("/api/whatsapp/", status_code=200)
async def post_message(request: Request, response: Response):
    # Log a small summary (timestamp is not present at top level in this payload)
    logger.debug("\n\nWebhook received payload:\n")

    # Return 200 with no body to match the original JS behaviour
    body = await request.body()
    converted_body = None

    try: 
        converted_body = WhatsAppWebhook_Message.model_validate_json(json_data=body, strict=False)
    except Exception as e:
        logger.warning(f"Failed to parse WhatsAppWebhook_Message")
        logger.debug(e)
        logger.debug(body)

        response.status_code = 500
        return response

    if converted_body is None:
        response.status_code = 400
        return response
    
    if converted_body.entry[0].changes[0].value.statuses is not None:
        logger.debug(converted_body.entry[0].changes[0].value.statuses[0])
        
        status = converted_body.entry[0].changes[0].value.statuses[0]
        if status.pricing is not None and status.pricing.billable:
            logger.info("Message was billable")
            logger.info(status.pricing)
            
        logger.debug("Received status update - ignoring")
        response.status_code = 200
        return response


    message = converted_body.entry[0].changes[0].value.messages[0]
    customer = message.from_

    logger.debug("Received message:")
    logger.debug(message)
    logger.debug(message.text.body)

    
    if_user_exists = await services.sql.does_user_exist(customer)

    if not if_user_exists:
        logger.info(f"User {customer} does not exist in database, creating new user")
        await services.sql.create_user(customer, customer)

        logger.debug(f"New user created in database - {customer}")

        await send_whatsapp_textonly_message(
        whatsapp_business_id=whatsapp_business_phone_number_id,
        whatsapp_authtoken=whatsapp_token, 
        user_phone_number=customer, 
        message=welcome_message)

        response.status_code = 200
        return response


    response = await agent_service.process_message(customer, message.text.body)

    logger.debug(f"Response message: {response.content}")

    await send_whatsapp_textonly_message(
        whatsapp_business_id=whatsapp_business_phone_number_id,
        whatsapp_authtoken=whatsapp_token, 
        user_phone_number=customer, 
        message=response.content)

    response.status_code = 200
    return response