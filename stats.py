import json
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class Character:
    def __init__(self, name, damage, healing, totalRolls):
        self.name = name
        self.damage = damage
        self.healing = healing
        self.totalRolls = totalRolls

file = open('players-rolls.json')
data = json.load(file)
totalHealing = 0

Damage = [0, 0, 0, 0, 0, 0, 0, 0, 0]
Healing = [0, 0, 0, 0, 0, 0, 0, 0, 0]
Saves = [0, 0, 0, 0, 0, 0, 0, 0, 0]
Checks = [0, 0, 0, 0, 0, 0, 0, 0, 0]

abilities = ['Acrobatics', 'Animal Handling', 'Arcana', 'Athletics', 'Deception', 'History', 'Insight', 'Intimidation', 'Investigation', 'Medicine', 'Nature', 'Perception', 'Performance', 'Religion', 'Sleight of Hand', 'Stealth', 'Survival']

for roll in data:
    if "damage" in roll["embeds"][0]["title"]:
        rawValue = str(prop["value"])
        i = rawValue.index('t')
        val = rawValue[i:]
        damage = 0
        for char in val:
            if char.isdigit():
                damage += int(char)
        Damage[idx] += damage
        continue
    elif "Save" in roll["embeds"][0]["title"]:
        Saves[idx] += 1
        continue
    
    for prop in roll["embeds"][0]["fields"]:
        if "Damage" in prop["name"] and "Total" not in prop["name"]:
            # add to damage
            rawValue = str(prop["value"])
            i = rawValue.index('t')
            val = rawValue[i:]
            damage = 0
            for char in val:
                if char.isdigit():
                    damage += int(char)
            print("DAMAGE ", damage)
            Damage[idx] += damage
        elif "Total" in prop["name"]:
            print(prop["value"])
        elif "Healing" in prop["name"]:
            # add to healing
            rawValue = str(prop["value"])
            i = rawValue.index('t')
            val = rawValue[i:]
            healing = 0
            for char in val:
                if char.isdigit():
                    healing += int(char)
            Healing[idx] += healing
    
    abilityCheck = roll["embeds"][0]["title"].split('(')[0]
    if abilityCheck in abilities:
        Checks[idx] += 1
print(Damage)
print(Healing)
file.close()

characters = ["Player1", "Player2", "Gambler", "Klaus", "Mori", "Neuma", "Percy", "Stick", "Verdan"]

N = 9
ind = np.arange(N)
width = 0.2

fig, ax = plt.subplots()
fig.set_size_inches(12, 8)
dmg = plt.bar(ind, Checks, width=width, color='r', label='Ability Checks')
heal = plt.bar(ind+width, Saves, width=width, color='b', label='Saving Throws')
#saves = plt.bar(ind+width*2, Saves, width=width, color='g', label='Saving Throws')
#checks = plt.bar(ind+width*3, Checks, width=width, color='orange', label='Ability Checks')

plt.xlabel("Character")
plt.ylabel("Value")
plt.title("Variety Pack Abilitiy Checks / Saving Throws Distribution")
ax.set_xticks([0,1,2,3,4,5,6,7,8])
ax.set_xticklabels(characters)
ax.bar_label(dmg, padding=3)
ax.bar_label(heal, padding=3)
ax.legend()
plt.show()