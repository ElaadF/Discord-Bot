import asyncio
import discord
import sys
from discord.ext import commands

from games.Quizz import Quizz, Status

Client = discord.Client()
client = commands.Bot(command_prefix="!")


@client.event
async def on_ready():
    print("Bot is online and connected to Discord")  # This will be called when the bot connects to the server


quizz = Quizz(Status.QUIZZ_SLEEP)


async def stop_quizz():
    if quizz.status == Status.QUIZZ_ACTIVE:
        client.close()
        quizz.status = Status.QUIZZ_SLEEP
        await client.send_message(quizz.channel, "---- Quizz Terminé ----")


async def start_quizz():
    if quizz.status == Status.QUIZZ_SLEEP:
        quizz.status = Status.QUIZZ_ACTIVE
        await client.send_message(quizz.channel, "Début du quizz dans 5s...")
        await asyncio.sleep(5)
        quizz.generate_question_answer()
        await client.send_message(quizz.channel, "```" + quizz.question + "```")


def test_answer(answer, message):
    if answer == message:
        return True
    return False


def test_message_channel(channel):
    if channel == client.get_channel("405665341977395211"):
        return True
    return False


async def new_question():
    quizz.generate_question_answer()
    await client.send_message(quizz.channel, "```" + quizz.question + "```")


async def right_answer(message):
    await client.add_reaction(message, u"\u2705")
    await client.send_message(quizz.channel, "Prochaine question dans 5s...")
    await asyncio.sleep(5)
    await new_question()


async def my_background_task():
    global quizz
    await client.wait_until_ready()
    channel = discord.Object(id='405665341977395211')
    while not client.is_closed:
        await asyncio.sleep(25)  # task runs every 60 seconds
        await client.send_message(channel, "Nouvelle question : ")
        quizz.generate_question_answer()
        await client.send_message(quizz.channel,
                                  "```NOUVELLE QUESTION:" + quizz.question + "```")


@client.event
async def on_message(message):
    global quizz

    if message.content.startswith("!stop"):
        await stop_quizz()

    if message.content.startswith("!quizz"):

        await start_quizz()

    if quizz.status == Status.QUIZZ_ACTIVE:
        # Righ answer process
        if test_answer(quizz.answer_question, message.content.upper()) and test_message_channel(message.channel):
            await right_answer(message)

        # Bad answer process
        elif not test_answer(quizz.answer_question, message.content.upper()) \
                and test_message_channel(message.channel) \
                and message.author.name != "Quizz"\
                and message.content != "!quizz":
            await client.add_reaction(message, u"\u274C")


#client.loop.create_task(my_background_task())
client.run(str(sys.argv[1]))  # Replace token with your bots token
