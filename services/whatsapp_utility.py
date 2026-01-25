def strip_whatsapp_token(token: str):
    if (token == None):
        return token
    if (not token.startswith("WHATSAPP_TOKEN")):
        return token
    stripped_token = token.removeprefix("WHATSAPP_TOKEN='").removesuffix("'")
    return stripped_token