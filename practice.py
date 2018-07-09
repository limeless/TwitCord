#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@desc:
@author: z3r0610ck
@contact: z3roblock@icloud.com
@software: Atom  @since:python 3.6.4 on 2018/4/23
"""
import os
import random
import asyncio
import aiohttp
from discord import Game
from discord.ext.commands import Bot
from flask import Flask


app = Flask(__name__)
@app.route("/") #Hey Heroku magic.
def monitoring():
    return "200"


BOT_PREFIX = ("?", "!", "!tc")
TOKEN = os.environ.get('TOKEN')

client = Bot(command_prefix=BOT_PREFIX)

@client.command(name='8ball',
                description="回應你的 是/非 問題。",
                brief="神秘力量的回應。",
                aliases=['eight_ball', 'eightball', '8-ball', '八號球'],
                pass_context=True)
async def eight_ball(context):
    possible_responses = [
        '最好是不要這麼做',
        '可能不會發生',
        '這不好說',
        '可能會發生哦',
        '絕對會的',
    ]
    await client.say(random.choice(possible_responses) + ", " + context.message.author.mention)


@client.command(name='square',
                aliases=['平方', '^2'],
                pass_context=True)
async def square(number):
    squared_value = int(number) * int(number)
    await client.say(str(number) + " 的平方是 " + str(squared_value))


@client.command(name='echo',
                description="回音功能",
                brief="山谷中的回音。",
                aliases=['學我', '回應', '鸚鵡', '回音'],
                pass_context=True)
async def echo(context):
    msg = " ".join(context.message.content.split()[1:]) #Split first and put it back to string.
    await client.say('好哦！ 我要學 ' + context.message.author.mention + ' 說：' + msg)


@client.command()
async def bitcoin():
    url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
    async with aiohttp.ClientSession() as session:  # Async HTTP request
        raw_response = await session.get(url)
        response = await raw_response.json()
        await client.say("比特幣目前的價錢為: $" + response['bpi']['USD']['rate'] + " USD")


@client.event
async def on_ready():
    await client.change_presence(game=Game(name="正在被人類調教中"))
    print("成功登入為：" + client.user.name)


@client.event
async def on_member_join(member):
    server = member.server
    fmt = '歡迎 {0.mention} 進入 {1.name}!'
    await client.send_message(server, fmt.format(member, server))


async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("目前伺服器列表:")
        for server in client.servers:
            print(server.name)
        await asyncio.sleep(600)


if __name__ == "__main__":
    client.loop.create_task(list_servers())
    client.run(TOKEN)
    app.jinja_env.cache = {}
    app.run()
