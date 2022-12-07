# Prepare discord instance
import discord
import env
import log
import ping_pong
import vc_funcs

intents = discord.Intents.all()
intents.members = True

bot = discord.Bot(intents = intents)

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    res = ping_pong.make_res(message.content)
    if res != "":
        log.logger.info(f"PingPong: {res}")
        await message.channel.send(res)
    
@bot.event
async def on_ready():
    log.logger.info("Listening...")

@bot.event # 通話検知
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    op = vc_funcs.detect_operation(before, after)
    if op == "start":
        bot.dispatch("vc_start", member, after.channel)
    if op == "end":
        bot.dispatch("vc_end", before.channel)
    if op == "many":
        bot.dispatch("vc_many", member, after.channel)

@bot.event # 通話開始
async def on_vc_start(mem: discord.Member, ch: discord.channel):
    log.logger.info(f"VC_Start: {ch.name} is started.")
    emb = discord.Embed(title=f"{ch.name} で通話が開始されました！", description=f"{mem.display_name}")
    chid = vc_funcs.detect_ch_id(ch.id)
    await bot.get_channel(int(chid)).send(embed=emb)

@bot.event # 大人数参加
async def on_vc_many(mem: discord.Member, ch: discord.channel):
    log.logger.info(f"VC_Many: {mem.display_name} is join to {ch.name}.")
    emb = discord.Embed(title=f"{ch.name} に {vc_funcs.count_people(ch)}人目の参加者がきました！", description=f"来た人: {mem.display_name}")
    chid = vc_funcs.detect_ch_id(ch.id)
    await bot.get_channel(int(chid)).send(embed=emb)

@bot.event # 通話終了
async def on_vc_end(ch: discord.channel):
    log.logger.info(f"VC_End: {ch.name} is ended.")
    emb = discord.Embed(title=f"{ch.name} の通話は終了しました")
    chid = vc_funcs.detect_ch_id(ch.id)
    await bot.get_channel(int(chid)).send(embed=emb)

@bot.slash_command(guild_ids=[env.GUILD_ID], description="指定のユーザーに援護ピンを立てます。") # 援護ピン
async def engo(ctx, user : discord.User):
    msg = f"{user.mention}を援護！"
    log.logger.info(f"Slash_Engo: {msg}")
    await ctx.respond(msg)

bot.run(env.DISCORD_BOT_TOKEN)