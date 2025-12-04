from uagents import Agent, Model, Context

class Message(Model):
    message: str

slaanesh = Agent(
    name="Slaneesh agent",
    port=8001,
    seed="Slaneesh agent seed phrase",
    endpoint=["http://localhost:8001/submit"],
    network="testnet"
)

@slaanesh.on_message(model=Message)
async def slaneesh_message_handler(ctx: Context, sender: str, msg: Message):
    ctx.logger.info(f"Received message from {sender}: {msg.message}")
    await ctx.send(sender, Message(message="hello there slaanesh"))

if __name__ == "__main__":
    slaanesh.run()