import os
import sys
import logging
from langchain_azure_ai.chat_models import AzureAIChatCompletionsModel
from langchain.agents import create_agent

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
            system_prompt="You are a helpful assistant",
        )
        
    async def process_message(self, message: str) -> str:
        """Process a message through the LangChain agent"""
        response = await self.agent.ainvoke({
            "messages": [{"role": "user", "content": message}]
        })

        print(response)
        return response['messages'][-1]
    
    # async def model_call(self, prompt: str) -> str:
    #     """Directly call the model with a prompt"""
    #     response = await self.model.ainvoke(prompt)
    #     print(response)

    #     return response.content
    
agent_service = AgentService()