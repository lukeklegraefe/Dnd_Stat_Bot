import discord
from discord.ext import commands
import pandas as pd
import csv
import re
import numpy as np
import matplotlib.pyplot as plt

API_TOKEN = 'API_TOKEN'

df = pd.DataFrame(columns=['player', 'type', 'value'])
characters = ["Player1", "Player2", "Player3", "Player4", "Player5", "Player6", "Player7", "Player8",]
Damage = [0, 0, 0, 0, 0, 0, 0, 0]
Healing = [0, 0, 0, 0, 0, 0, 0, 0]

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
cmd = commands.Bot(command_prefix=".", intents=intents)
guild = discord.Guild

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('.shutdown to terminate'))

@client.event
async def on_message(message):
    if message.content == ".shutdown":
        print("Closing...")
        displayStats()
        await client.close()
        exit()
    if str(message.channel) == "players-rolls":
        handleEmbed(message.embeds)

def handleEmbed(embeds):
    for embed in embeds:
        e = embed.to_dict()
        if "fields" not in e:
            continue
        player = e['author']['name']
        playerIdx = characters.index(player)

        if "damage" in str(e['title']).lower() or "smite" in str(e['title']).lower():
            raw = str(e['fields'][0]['value'])
            startPos = raw.index('t')
            val = raw[startPos:]
            values = [int(s) for s in re.findall(r'\b\d+\b', val)]
            Damage[playerIdx] += sum(values)
            print(player, " dealt ", sum(values), " damage.")
            continue

        for field in reversed(e['fields']):
            raw = str(field['value'])
            startPos = raw.index('t')
            val = raw[startPos:]
            values = [int(s) for s in re.findall(r'\b\d+\b', val)]
            if "total" in str(field['name']).lower() or "Damage" in field['name']:
                Damage[playerIdx] += sum(values)
                print(player, " dealt ", sum(values), " damage.")
                break
            elif "healing" in str(field['name']).lower():
                Healing[playerIdx] += sum(values)
                print(player, " healed ", sum(values), " hitpoints.")
                break

def displayStats():
    N = len(characters)
    ind = np.arange(N)
    width = 0.2

    fig, ax = plt.subplots()
    fig.set_size_inches(12, 8)
    dmg = plt.bar(ind, Damage, width=width, color='orange', label='Damage')
    heal = plt.bar(ind+width, Healing, width=width, color='b', label='Healing')

    plt.xlabel("Character")
    plt.ylabel("Value")
    plt.title("Damage / Healing Distribution")
    ax.set_xticks([0,1,2,3,4,5,6,7])
    ax.set_xticklabels(characters)
    ax.bar_label(dmg, padding=3)
    ax.bar_label(heal, padding=3)
    ax.legend()
    plt.show()

if __name__ == "__main__":
    client.run(API_TOKEN)