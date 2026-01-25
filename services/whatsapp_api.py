import httpx

whatsapp_graph_url = "https://graph.facebook.com/v22.0/"
whatsapp_graph_message_api_path = "/messages"

async def send_whatsapp_textonly_message(whatsapp_business_id: str, whatsapp_authtoken: str, user_phone_number: str, message: str):
    url = f"{whatsapp_graph_url}{whatsapp_business_id}{whatsapp_graph_message_api_path}"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {whatsapp_authtoken}"
    }

    data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": user_phone_number,
        "type": "text",
        "text": {
            "preview_url": False,
            "body": message
        }
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=data)
        print(response.status_code)
        print(response.json())