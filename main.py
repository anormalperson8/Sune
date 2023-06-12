import discord
import os
import typing
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands
from censorship import get, add_word, delete_word

intents = discord.Intents.all()
client = commands.Bot(command_prefix='^', intents=intents, activity=discord.Game(name="Suffering"))

load_dotenv("/home/sunny/SuneBot/data/text.env")

token = os.getenv('TOKEN')
owner_id = int(os.getenv('ID'))

censorship_list = []
function_just_called = False


@client.event
async def on_ready():
    get(censorship_list)
    print('We have logged in as {0.user}'.format(client))


# Response-testing command
@client.command()
async def boo(ctx):
    if ctx.author.bot:
        await ctx.send("You're not a user :P")
        return
    await ctx.send("Oi")


# Start of censorship commands
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
    stat = add_word(arg, censorship_list)
    if stat:
        await ctx.send(f"\"{arg}\" successfully added!")
    else:
        await ctx.send(f"\"{arg}\" is already in the list/It is not a valid word!")


@client.command()
async def delete(ctx, arg):
    if ctx.author.bot:
        await ctx.send("You're not a user :P")
        return
    if ctx.author.id != owner_id:
        await ctx.send("Only the owner of the bot can amend the 1984 list!")
        return
    if len(arg) == 1:
        await ctx.send("That's... a letter, are you sure?")
        return
    stat = delete_word(arg, censorship_list)
    if stat:
        await ctx.send(f"\"{arg}\" successfully deleted!")
    else:
        await ctx.send(f"\"{arg}\" is not on the list/It is not a valid word!")


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


# End of censorship commands

# Start of censorship slash commands
@client.tree.command(description="adds a word to the 1984 list, only useable by the owner", guilds=client.guilds)
async def add_a_word(interaction: discord.Interaction, arg: str) -> None:
    await interaction.response.defer(thinking=True)
    if interaction.user.bot:
        await interaction.edit_original_response(content="You're not a user :P")
        return
    if interaction.user.id != owner_id:
        await interaction.edit_original_response(content="Only the owner of the bot can amend the 1984 list!")
        return
    if len(arg) == 1:
        await interaction.edit_original_response(content="That's... a letter, are you sure?")
        return
    stat = add_word(arg, censorship_list)
    if stat:
        await interaction.edit_original_response(content=f"\"{arg}\" successfully added!")
    else:
        await interaction.edit_original_response(content=f"\"{arg}\" is already in the list/It is not a valid word!")


# End of censorship slash commands

@commands.guild_only()
@client.command()
async def sync(ctx):
    if ctx.author.id == owner_id:
        await client.tree.sync()
        await ctx.send("Commands synced!")
    else:
        await ctx.send("You're not the owner")


# Censorship on message
@client.listen('on_message')
async def on_message(message):
    if message.author.bot:
        return
    if message.content[0] == '^' and message.content[1] == 'a' \
            and message.content[2] == 'd' and message.content[3] == 'd':
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
            f"The message sent by {name} was \"{text}\". And yes, you have been 1984'd")


client.run(token)
