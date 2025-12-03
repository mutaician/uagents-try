from uagents import Agent, Context, Model

class Message(Model):
    message: str

RECIPIENT_ADDRESS = (
    "test-agent://agent1q04ck8crsr5je3nkst0vw7nsz9c5lnf7m8hmm5hy4nfvdm9a4q43krzvt8u"
)

SenderAgent = Agent(
    name="SenderAgent",
    port=8000,
    seed="SenderAgent secret phrase",
    endpoint=["http://127.0.0.1:8000/submit"]
)

print(SenderAgent.address)

@SenderAgent.on_interval(period=2)
async def send_message(ctx: Context):
    await ctx.send(RECIPIENT_ADDRESS, Message(message="Hi there. Let's start our conversation"))

@SenderAgent.on_message(model=Message)
async def message_handler(ctx: Context, sender: str, msg: Message):
    ctx.logger.info(f"Received message from {sender}: {msg.message}")

if __name__ == "__main__":
    SenderAgent.run()