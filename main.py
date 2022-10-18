from lib2to3.pgen2 import token
import os
from pydoc import describe
from dotenv import load_dotenv

load_dotenv()

DISCORD_BOT_TOKEN = os.environ['APP_BOT_TOKEN']
DISCORD_CLIENT_ID = os.environ['CLIENT_ID']
NOTICE_CH_ID = int(os.environ['NOTICE_CH_ID'])
UNITE_TX_ID = int(os.environ['UNITE_TX_ID'])
UNITE_VC_ID = int(os.environ['UNITE_VC_ID'])
GENSHIN_TX_ID = int(os.environ['GENSHIN_TX_ID'])
GENSHIN_VC_ID = int(os.environ['GENSHIN_VC_ID'])
GUILD_ID = [int(os.environ['GUILD_ID'])]

import discord

intents=discord.Intents.all() # after

bot = discord.Bot(intents = intents)

@bot.event
async def on_message(message):
    msg = message.content
    res = ""

    if msg == "ping":
        res = "pong"
    if msg == "hong":
        res = "kong"
    if msg == "bang":
        res = "kok"
    if msg == "にゃが":
        res = "にゃがにゃが"
    
    if res != "":
        await message.channel.send(res)
    
@bot.event
async def on_ready():
    print("listening...")

@bot.event # 通話検知
async def on_voice_state_update(member, before, after):
    bf_cnt = -1
    af_cnt = -1

    if before.channel is not None:
        bf_cnt = len(before.channel.voice_states.keys())
    if after.channel is not None:
        af_cnt = len(after.channel.voice_states.keys())

    is_different_ch = True # voice state update の前後で参加チャンネルが異なる
    if bf_cnt != -1 and af_cnt != -1:
        is_different_ch = (before.channel.id != after.channel.id)
    
    if af_cnt != -1:
        if af_cnt == 1: # 通話開始
            bot.dispatch("vc_start", member, after.channel)
        if af_cnt > 3 and is_different_ch: # 大人数参加
            bot.dispatch("vc_many", member, after.channel)
    
    if bf_cnt == 0: # 通話終了
        bot.dispatch("vc_end", before.channel)

@bot.event # 通話開始
async def on_vc_start(member, channel):
    emb = discord.Embed(title=f"{channel.name} で通話が開始されました！", description=f"{member.display_name}")

    chid = NOTICE_CH_ID

    if str(channel.id) == str(UNITE_VC_ID): # UNITE部
        chid = UNITE_TX_ID
    if str(channel.id) == str(GENSHIN_VC_ID): # 原神部
        chid = GENSHIN_TX_ID
    
    print(f"通話開始: {channel.name} {member.display_name}")
    await bot.get_channel(int(chid)).send(embed=emb)

@bot.event # 大人数参加
async def on_vc_many(member, channel):
    cnt = len(bot.get_channel(channel.id).voice_states.keys())

    emb = discord.Embed(title=f"{channel.name} に {cnt}人目の参加者がきました！", description=f"来た人: {member.display_name}")

    chid = NOTICE_CH_ID

    if str(channel.id) == str(UNITE_VC_ID): # UNITE部
        chid = UNITE_TX_ID
    if str(channel.id) == str(GENSHIN_VC_ID): # 原神部
        chid = GENSHIN_TX_ID
    
    print(f"大人数参加: {channel.name}")
    await bot.get_channel(int(chid)).send(embed=emb)

@bot.event
async def on_vc_end(channel):
    emb = discord.Embed(title=f"{channel.name} の通話は終了しました")

    chid = NOTICE_CH_ID

    if str(channel.id) == str(UNITE_VC_ID): # UNITE部
        chid = UNITE_TX_ID
    if str(channel.id) == str(GENSHIN_VC_ID): # 原神部
        chid = GENSHIN_TX_ID

    print(f"通話終了: {channel.name}")
    await bot.get_channel(int(chid)).send(embed=emb)

@bot.slash_command(description="指定のユーザーに援護ピンを立てます。")
async def engo(ctx, user : discord.User):
    msg = f"{user.mention}を援護！"
    print(msg)
    await ctx.respond(msg)

bot.run(DISCORD_BOT_TOKEN)