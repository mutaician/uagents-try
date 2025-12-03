from uagents import Agent, Context, Model

class Message(Model):
    message: str

ReceiverAgent = Agent(
    name="ReceiverAgent",port=8001, seed="ReceiverAgent changed secret phrase",
    endpoint=["http://127.0.0.1:8001/submit"]
)

print(ReceiverAgent.address)

@ReceiverAgent.on_message(model=Message)
async def message_handler(ctx: Context, sender: str, msg: Message):
    ctx.logger.info(f"Received message from {sender}: {msg.message}")
    
    await ctx.send(sender, Message(message="Cool! Let's get started"))
    
if __name__ == "__main__":
    ReceiverAgent.run()