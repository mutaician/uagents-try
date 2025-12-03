from uagents import Agent, Model, Context, Field, Protocol
from pydantic import BaseModel, Field

agent = Agent(
    name="nano test agent",
    seed="small seed to use",
    port=8001,
    endpoint=["http://localhost:8001/submit"]
)

OTHER_AGENT_ADDRESS = "agent1q0jz0qr3dsm0ve2f6wtjq0fwwznszr9kr6k4s2z42t47w9lfrljqz4mzm8u"

QUESTION = "Is the meaning of life to find the meaning of life"

class AIRequest(BaseModel):
    question: str = Field(description="The question that the user wants to have an opinion on")

class AIResponse(BaseModel):
    answer: str = Field(description="The answer from AI agent to the user agent")

@agent.on_event("startup")
async def ask_question(ctx: Context):
    ctx.logger.info(f"Asking AI agent to answer {QUESTION}")
    await ctx.send(OTHER_AGENT_ADDRESS, AIRequest(question=QUESTION))
    
@agent.on_message(model=AIResponse)
async def handle_data(ctx: Context, sender: str, data: AIResponse):
    ctx.logger.info(f"Got response from AI agent: {data.answer}")
    
agent.run()