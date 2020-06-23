import discord
import okbasis
import mexbasis
import huobasis

client = discord.Client()
channel_id = 723559287116267610
token = "NzIzNTU4MzY1MjYzMDM2NDI4.XuzYyA.BTc4m4fXVOlM4RSOm1r5wWWjNHQ"

@client.event
async def on_ready():
    print("connected")

@client.event
async def on_message(message):
    channel = client.get_channel(channel_id)
    if message.author == client.user:
       return

    if message.content.startswith("$okbasis"):
        contracts, basis = await okbasis.get_contracts_basis()
        msg = "**Okex Contracts**\n"
        for i in range(len(contracts)):
            msg += contracts[i] + ":`"
            msg+= str(basis[i]) + "`\n"
        await channel.send(msg)

    if message.content.startswith("$mexbasis"):
        contracts, basis = await mexbasis.get_contracts_basis()
        msg = "**Btimex Contracts**\n"
        for i in range(len(contracts)):
            msg += contracts[i] + ":`"
            msg+= str(basis[i]) + "`\n"
        await channel.send(msg)

    if message.content.startswith("$huobasis"):
        contracts = ["current week", "next week", "quarterly"]
        basis = await huobasis.get_basis()
        msg = "**Huobi Contracts**\n"
        for i in range(len(contracts)):
            msg += contracts[i] + ":`"
            msg+= str(basis[i]) + "`\n"
        await channel.send(msg)

client.run(token)
