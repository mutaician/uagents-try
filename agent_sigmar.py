from uagents import Agent, Model, Context

SLANESH_ADDRESS = "agent1qd98n3x367fmatmp0m3junj9nf47cw2mtkmjgcqtcxa68m6v8j2z5kefagf"

class Message(Model):
    message: str

sigmar = Agent(
    name="Sigmar agent",
    port=8000,
    seed="Seed for Sigmar agent",
    endpoint=["http://localhost:8000/submit"],
    network="testnet"
)

@sigmar.on_interval(period=3)
async def send_message(ctx: Context):
    await ctx.send(SLANESH_ADDRESS, Message(message="hello there sigmar"))

@sigmar.on_message(model=Message)
async def sigmar_message_handler(ctx: Context, sender: str, msg: Message):
    ctx.logger.info(f"Message Received from {sender}: {msg.message}")

if __name__ == "__main__":
    sigmar.run()