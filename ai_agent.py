from uagents import Agent, Context, Protocol, Model
from pydantic import BaseModel, Field
from openai import OpenAI

CHAT_MODEL = "gpt-5-mini"

agent = Agent(
    name="open_ai_agent",
    seed="NEW PHRASE SEED1",
    port=8000,
    endpoint=["http://localhost:8000/submit"],
)

class AIRequest(BaseModel):
    question: str = Field(
        description="The question that the user wants to have an opinion on"
    )

class AIResponse(BaseModel):
    answer: str = Field(
        description="The answer from AI agent to the user agent"
    )

PROMPT_TEMPLATE = """
Whats your opinion on the following question/statement
{question}
"""

# define periodic task
# @agent.on_interval(period=2)
# async def say_hello(ctx: Context):
#     ctx.logger.info(f"Hello, my name is {agent.name}")


@agent.on_event("startup")
async def introduce_agent(ctx: Context):
    ctx.logger.info(f"{agent.address}")

def query_openai_chat(prompt: str):
    client = OpenAI()
    
    response = client.responses.create(
        model= CHAT_MODEL,
        input= prompt,  # prompt
    )
    
    return response.output_text # text

@agent.on_message(model=AIRequest, replies=AIResponse)
async def give_opinion(ctx: Context, sender: str, msg: AIRequest):
    ctx.logger.info(f"Received question from {sender}: {msg.question}")
    prompt = PROMPT_TEMPLATE.format(question=msg.question)
    response = query_openai_chat(prompt)
    ctx.logger.info(f"Response: {response}")
    await ctx.send(
        sender, AIResponse(answer=response)
    )

if __name__ == "__main__":
    agent.run()
