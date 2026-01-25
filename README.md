# Resolve Automata

Entry for Encode Hackathon: 

Midway Checkpoint: 
- 

### Description 
Resolve Automata is an agentic application which helps users keep track of and complete their new years resolutions.

It's primary interface is through a messaging tool that the majority of people have access to - Whatsapp. 

Resolve Automate will log your activity for you and will help you keep going. 

### Progress
An poc version of the application has been created. 

### Live Version
Landing Page: 
WhatsApp: 

### Tech Stack 
- Frontend: 
    - WhatsApp Business
    - Landing Page

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
Opik monitoring and tracking will be implemented this week. 

### Get Started - Dev Environment

- To run the solution locally, you will need:
    - Microsoft Foundry with Project and gpt-nano-5 enabled
    - Azure SQL DB - Free tier with connected Service Principle

.env file
```

```

```bash
pip install -r requirements.txt

fastapi dev main.py

# You can then open a swagger Openapi page to test the api calls directly. 
# http://localhost:8000/docs

```

TODO: 
1. Finish off SQL DB Integration 
2. Hosting for API in Azure - App Service? 
    - how to deploy - manually 
3. Quick web page with: 
    - Intro
    - Chat web page
    - Database 
4. README.md integration 
4. WhatsApp Integration 
5. Opik Integration 
6. Improve features. 
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
7. Additional Features
    - Github Actions deploy 
    - 
