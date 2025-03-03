import discord
import os
from discord.ext import commands
import requests
import asyncio
import json
import base64

client=commands.Bot(command_prefix=';::;', self_bot=True, help_command=None)

GUILD_ID = 997613016549957662
CHANNEL_ID = 1054055225754914921

rtoken = os.getenv("RTOKEN")
header = {"Authorization": "Bearer {}".format(rtoken)}
link="https://api.github.com/repos//MainAcc-1/contents/"

boton = {"status":True}

@client.event
async def on_ready():
    os.system('clear')
    print(f'Logged in as {client.user} ({client.user.id})')
    client.dispatch("call")
    await asyncio.sleep(21400)
    with open("rerun.json", "r") as f:
        rerun = json.load(f)
    if rerun["id"]==1:
        rerun["id"]=0
    elif rerun["id"]==0:
        rerun["id"]=1
    r = requests.get(link+"rerun.json",headers=header)
    sh=r.json()["sha"]
    base64S= base64.b64encode(bytes(json.dumps(rerun), "utf-8"))
    rjson = {"message":"cf", "content":base64S.decode("utf-8"),"sha":sh}
    response = requests.put(link+"rerun.json", data=json.dumps(rjson), headers=header)
    

@client.event
async def on_call():
    if client.get_guild(GUILD_ID).get_member(client.user.id).voice is None:
        check = True
        while check:
            if client.get_guild(GUILD_ID).get_member(client.user.id).voice is None:
                try:
                    vc = client.get_guild(GUILD_ID).get_channel(CHANNEL_ID)
                    await vc.connect()
                    check = False
                except:
                    await asyncio.sleep(1)
            else:
                check = False
                
@client.event
async def on_voice_state_update(member, before, after):
    if boton["status"]:
        if client.get_guild(GUILD_ID).get_member(client.user.id).voice is None:
            check = True
            while check:
                if client.get_guild(GUILD_ID).get_member(client.user.id).voice is None:
                    try:
                        vc = client.get_guild(GUILD_ID).get_channel(CHANNEL_ID)
                        await vc.connect()
                        break
                    except:
                        await asyncio.sleep(1)
                else:
                    break

@client.event
async def on_message(message):  
    if message.content == "bot off":
        boton["status"] = False
        await message.channel.send("Bot go offline!")
    elif message.content == "bot on":
        boton["status"] = True
        await message.channel.send("Bot go online!")
        client.dispatch("call")
            

client.run(os.getenv("TOKEN"))
