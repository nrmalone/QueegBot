import discord
from discord.ext import commands
import random

class bingo(commands.Cog):
    def __init__(self,client):
        self.client = client
    
    # bingocard
    @commands.command()
    async def bingo(self,ctx,cmd):
        if cmd == "card":
            bingoCard = []
            bingoCardString = "| B - I - N - G - O |\n"
            space = 1
            spaceValue = 0
            while space < 26:
                # B column (1-15)
                if space %5 == 1:
                    spaceValue = random.randint(1,15);
                    while bingoCard.count(spaceValue) > 0:
                        spaceValue = random.randint(1,15);
                    else:
                        bingoCard.append(spaceValue)
                        bingoCardString += "| " + str(spaceValue)
                        space +=1
                # I column (16-30)
                if space %5 == 2:
                    spaceValue = random.randint(16,30);
                    while bingoCard.count(spaceValue) > 0:
                        spaceValue = random.randint(16,30);
                    else:
                        bingoCardString += " " + str(spaceValue)
                        space +=1
                # N column (31-45)
                if (space %5 == 3) and (space != 13):
                    spaceValue = random.randint(31,45);
                    while bingoCard.count(spaceValue) > 0:
                        spaceValue = random.randint(31,45);
                    else:
                        bingoCardString += " " + str(spaceValue)
                        space +=1
                elif (space == 13):
                    bingoCardString += " x "
                    space +=1
                # G column (46-60)
                if (space %5 == 4):
                    spaceValue = random.randint(46,60);
                    while bingoCard.count(spaceValue) > 0:
                        spaceValue = random.randint(46,60);
                    else:
                        bingoCardString += " " + str(spaceValue)
                        space +=1
                # O column (61-75)
                if (space %5 == 0):
                    spaceValue = random.randint(61,75);
                    while bingoCard.count(spaceValue) > 0:
                        spaceValue = random.randint(61,75)
                    else:
                        bingoCardString += " " + str(spaceValue) + " |\n"
                        space +=1
            await ctx.author.send(str(bingoCardString))
            bingoCard.clear()

        elif cmd == "roll":
            pass

def setup(client):
    client.add_cog(bingo(client))