import os
import sys
import logging
from langchain_azure_ai.chat_models import AzureAIChatCompletionsModel
from langchain.agents import create_agent
from langchain.messages import SystemMessage, HumanMessage
from services.database_tools import search_database_for_user_activity, log_activity_to_database, count_activity_for_user_this_month 
import opik
from opik.integrations.langchain import OpikTracer

logger = logging.getLogger("resolveautomata")

# Initialize Opik tracer for LangChain
opik_tracer = OpikTracer(tags=["resolveautomata", "whatsapp-agent"])

system_prompt = SystemMessage(
    content=[
        {
            "type": "text",
            "text": """
            You are a coach who helps people keep on track with their new year's resolutions. 
            You keep track of the user's progress and provide encouragement and advice.

            When responding to a user's message, keep the response short and concise. 
            Tell them that you have logged their progress and give them feedback on how they are doing that week.

            Upon receiving a message from the user search_database_for_user_activity to get their current activities.
            Then log_activity_to_database to log the new record for that user. If the activity the user mention is similar to what the user has in the database already, log that activity again.
            """,
        }
    ]
)

system_prompt2 = SystemMessage(
    content=[
        {
            "type": "text",
            "text": """
            You are a coach who helps people keep on track with their new year's resolutions. 
            You keep track of the user's progress and provide encouragement and advice.
            
            Upon receiving a message from the user search_database_for_user_activity to get their current activities.

            If the user has told you they have completed an activity, then log_activity_to_database to log the new record for that user. 
            If the activity the user mentions is similar to what the user has in the database already, then use the same activity name for the log.

            When responding to a user's message, keep the response short and concise. 
            If you logged their progress, then tell them that you have logged their progress and give them feedback on how they are doing that month using the count_activity_for_user_this_month tool.
            """,
        }
    ]
)


class AgentService: 
    def __init__(self):
        self.model = AzureAIChatCompletionsModel(
            endpoint=os.environ["AZURE_INFERENCE_ENDPOINT"],
            credential=os.environ["AZURE_INFERENCE_CREDENTIAL"],
            model="gpt-5-nano",
            client_kwargs={"logging_enable": True},
            temperature=1,
            timeout=10,
            max_completion_tokens=200
        )

        self.agent = create_agent(
            model=self.model,
            system_prompt=system_prompt2,
            tools=[search_database_for_user_activity, log_activity_to_database, count_activity_for_user_this_month]
        )
        
    @opik.track(name="process_message", tags=["agent"])
    async def process_message(self, user: str, message: str) -> str:
        """Process a message through the LangChain agent"""
        
        # Log metadata to Opik
        opik.track_metadata({"user": user, "message_length": len(message)})
        
        response = await self.agent.ainvoke(
            {"messages": [{"role": "user", "content": f"{message} from {user}"}]},
            config={"callbacks": [opik_tracer]}
        )

        logger.debug("Agent response:")
        logger.debug(response)
        
        return response['messages'][-1]
    
    # async def model_call(self, prompt: str) -> str:
    #     """Directly call the model with a prompt"""
    #     response = await self.model.ainvoke(prompt)
    #     print(response)

    #     return response.content
    
agent_service = AgentService()