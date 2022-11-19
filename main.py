import discord
import os
from discord.ext import commands
import requests
import asyncio
import json
import base64

client=commands.Bot(command_prefix='avc.', self_bot=True, help_command=None)

GUILD_ID = 755793441287438469
CHANNEL_ID = 1040222043058208849

rtoken = os.getenv("RTOKEN")
header = {"Authorization": "Bearer {}".format(rtoken)}
link="https://api.github.com/repos/shtnk1250/MainAcc-1/contents/"

@client.event
async def on_ready():
    os.system('clear')
    print(f'Logged in as {client.user} ({client.user.id})')
    client.dispatch("call")
    await asyncio.sleep(21500)
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
    while True:
        await asyncio.sleep(1)
        vc = discord.utils.get(client.get_guild(GUILD_ID).channels, id = CHANNEL_ID)
        if client.get_guild(GUILD_ID).get_member(client.user.id).voice is None:
            await vc.connect()
            print(f"Successfully joined {vc.name} ({vc.id})")
            
@client.command()
async def join():
    client.dispatch("call")

client.run(os.getenv("TOKEN"))
