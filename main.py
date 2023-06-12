import discord
import os
from dotenv import load_dotenv, find_dotenv
from discord.ext import commands
from censorship import get, add_word, delete_word

intents = discord.Intents.all()
client = commands.Bot(command_prefix='^', intents=intents)

load_dotenv("/home/sunny/SuneBot/data/text.env")

token = os.getenv('TOKEN')
owner_id = int(os.getenv('ID'))

censorship_list = []


@client.event
async def on_ready():
    get(censorship_list)
    print('We have logged in as {0.user}'.format(client))


@client.command()
async def boo(ctx):
    if ctx.author.bot:
        await ctx.send("You're not a user :P")
        return
    await ctx.send("Oi")


@client.command()
async def add(ctx, arg):
    if ctx.author.bot:
        await ctx.send("You're not a user :P")
        return
    if ctx.author.id != owner_id:
        await ctx.send("Only the owner of the bot can amend the 1984 list!")
        return
    if len(arg) == 1:
        await ctx.send("That's... a letter, are you sure?")
        return
    add_word(arg, censorship_list)


@client.command()
async def words(ctx):
    if ctx.author.bot:
        await ctx.send("You're not a user :P")
        return
    res = "The words are: "
    for i in range(len(censorship_list)):
        res += censorship_list[i]
        if i < len(censorship_list) - 1:
            res += ", "
    await ctx.send(res)


@client.listen('on_message')
async def on_message(message):
    if message.author.bot:
        return
    name = message.author.nick
    if name is None:
        name = message.author.name
    text = message.content
    count = 0
    for thing in censorship_list:
        if thing in message.content:
            replaced = ""
            for i in range(len(thing)):
                replaced = replaced + "-"
            text = text.replace(thing, replaced)
            count += 1
    if count != 0:
        await message.delete()
        await message.channel.send(
            f"Beep boop I've removed curse word(s) from the message.\n"
            f"The message sent by {name} was \"{text}\".")


client.run(token)
