# Resolve Automata

Entry for Encode Hackathon: 
- Commit To Change: An AI Agents Hackathon - 2026

### Description 
ResolveAutomata is your personal whatsapp buddy who helps you stay on track of your new years resolutions.  

It's primary interface is through a messaging tool that the majority of people have access to - Whatsapp. 

Resolve Automata using Agentic Reasoning will log your activity for you and will help you keep going. 

### Progress
An end to end version is live and working. 

### Live Version
Landing Page: 
WhatsApp - see presentation for number

### Tech Stack 
- Frontend: 
    - WhatsApp Business App

- Backend: 
    - Python FastAPI
    - Azure App Service

- Database: 
    - Azure SQL DB 

- Agentic Solution
    - Langchain (to build the agent chain)
    - Microsoft Foundry (for direct LLM Access)
    - Opik for agentic monitoring and evalution

### Opik 
Opik monitoring and tracking is being used to trace calls and evaluate agent effectiveness.

### Get Started - Dev Environment

- To run the solution locally, you will need:
    - Microsoft Foundry with Project and gpt-nano-5 enabled
    - Azure SQL DB - Free tier with connected Service Principle
    - Opik Cloud tool

- The whatsapp endpoints will be difficult to trigger from the swagger endpoint, so use the /activity endpoint to test the agent locally

- Create an .env file with following items
.env file
```txt
LOG_LEVEL=10

AZURE_INFERENCE_ENDPOINT=<Insert Microsoft Foundry URL Endpoint>
AZURE_INFERENCE_CREDENTIAL=<Insert Microsoft Foundry API Key>

AZURE_SERVICE_PRINCIPAL=<Insert Service principle APP ID>
AZURE_CLIENT_ID=<Insert Service Principle APP ID>
AZURE_CLIENT_TENANT_ID=<Insert service principle tenant id>
AZURE_CLIENT_SECRET=<Insert secret>

AZURE_SQL_SERVER_URL=<insert SQL Server URL>
AZURE_SQL_SERVER_NAME=<Insert SQL Server Name>
AZURE_SQLDB_NAME=<Insert SQL DB Name>

WHATSAPP_TOKEN=<Insert Whatsapp Token>
WHATSAPP_BUSINESS_ID=<insert whatsapp business ID>
WHATSAPP_BUSINESS_PHONE_NUMBER_ID=<Insert Whatsapp business phone id>
WHATSAPP_TEST_NUMBER=<Insert test number>


OPIK_API_KEY=<insert opik API key>
OPIK_WORKSPACE=<insert opik workspace name>
OPIK_URL_OVERRIDE=https://www.comet.com/opik/api 
```

```bash
pip install -r requirements.txt

fastapi dev main.py

# You can then open a swagger Openapi page to test the api calls directly. 
# http://localhost:8000/docs

```


#### Progress: 
DONE:
- Python FastAPI which contains Langchain agents and user interaction flows.
- Set up whatsapp business account to act as front end.
- Set up Microsoft Foundry as LLM API
- Set up Azure SQL DB to act as application database with agentic tools so Agent can interact properly. 
- Set up Opik to trace and evaluate agents. 
- Github Actions Deploy for Web App

TODO: 
- Improve features. 
    - Alembic SQL db Migrations
    - Sign up system 
    - User profile
    - Track model usage 
    - Migrate Database 
    - MCP server 
    - Authentication
    - Mock SQL Database calls and test out statements
    - Tools: 
        - Web Search find out specific useful things related to the activity. 
    - Reminder functionality 
    - Features to retain users with changing phone numbers
- Landing page with 
    - Intro
    - Chat web page
    - Database 
