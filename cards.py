import random
import discord
from discord.ext import commands
from asyncio import TimeoutError as TE

class cards(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command()
    async def cards(self, ctx):
        """
        Provides the user a list of functional games to play (MANUALLY EDITED),
        takes a choice in that same channel, and calls that game's function to play
        """
        async def poker(self, ctx):
            print("Poker game starting...")
            pass


        async def blackjack(self, ctx):
            print("Blackjack game starting...")
            deck = list()
            suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
            suits_dict = {x[0]: x for x in suits}
            suitsyms = {'H':'♡', 'D':'♢', 'C':'♧', 'S':'♤'}
            num_dict = {'1': 'Ace', '11': 'Jack', '12': 'Queen', '13': 'King'}
            snum_dict = {key: num_dict[key][0] for key in num_dict.keys()}
            rnum_dict = {num_dict[key]: key for key in num_dict}
            for suit in suits:
                for n in range(1,14):
                    deck.append(suit + str(n))
            dealer = []
            hand = []
            def printout(card: str) -> str:
                num = card[len(suits_dict[card[0]]):]
                if int(num) in (1, 11, 12, 13):
                    num = num_dict[num]
                return num + ' of ' + suits_dict[card[0]]
            def printout2(hand:str, *args) -> str:
                """
                Helper function to printout a player's hand
                
                :param hand: str text 'dealer' or 'player' to determine text color
                :*args: accepts any number of cards to print out in a row

                returns string (5 lines long) of a player's hand in ASCII text
                """
                cards = {str(i): {} for i in range(len(args))}
                for cardidx in cards:
                    cards[cardidx]['num'] = args[int(cardidx)][len(suits_dict[args[int(cardidx)][0]]):]
                    if int(cards[cardidx]['num']) in (1, 11, 12, 13):
                        cards[cardidx]['num'] = snum_dict[cards[cardidx]['num']]
                    cards[cardidx]['suit'] = suitsyms[args[int(cardidx)][0]]
                for card in cards:
                    print(f'card num {card}: {cards[card]}')
                # final = f"+---+\n {suit}      \n    {num}    \n      {suit} \n+---+"
                final = ("+---+" + "    ") * len(args) + '\n'
                for cardidx in range(len(args)):
                    final += (f" {cards[str(cardidx)]['suit']}" + ' '*7) if (cardidx % 2) == 0 else (f" {cards[str(cardidx)]['suit']}" + ' '*6)
                final += '\n'
                for cardidx in range(len(args)):
                    final += "  {:<3}    ".format(cards[str(cardidx)]['num']) if (cardidx % 2) == 0 else "  {:^3}   ".format(cards[str(cardidx)]['num'])
                final += '\n'
                for cardidx in range(len(args)):
                    final += (f"   {cards[str(cardidx)]['suit']}" + ' '*5) if (cardidx % 2) == 0 else (f"   {cards[str(cardidx)]['suit']}" + ' '*4)
                final += '\n' + ("+---+" + "    ") * len(args)
                return '```' + final + '```'
            card = random.choice(deck)
            dealer.append(card)
            game_msg = await ctx.send("Dealer is bouncing on his thumb", delete_after=120)
            # game_msg = await ctx.send("Dealer starts with a " + printout(card), delete_after=120)
            while card in dealer or card in hand:
                card = random.choice(deck)
            hand.append(card)
            # await game_msg.edit(suppress=False, content=str(game_msg.content + "\nYou start with a " + printout(card)), delete_after=120)
            await game_msg.edit(suppress=False, content=str(game_msg.content + "\n{}".format(printout2('dealer', random.choice(deck), random.choice(deck), random.choice(deck), random.choice(deck)))), delete_after=120)
            print("Blackjack game finished!")


        async def speed(self, ctx):
            print("Speed game starting...")
            pass


        await ctx.message.delete()
        game_dict = {"Poker" : poker, "Blackjack": blackjack, "Speed": speed}
        choice_dict = {}
        msg = "Available games:\n"
        for i, game in enumerate(game_dict.keys()):
            msg += f"\t{i+1}.\t{game}\n"
            choice_dict[str(i+1)] = game
        msg += "Enter a # to make your choice."
        await ctx.send(msg, delete_after=10)
        og_author, og_channel = ctx.author, ctx.channel
        def check(msg):
            """
            Checks that the original user is responding, 
            in the same channel, and with a valid choice
            from the games listed
            """
            return msg.content in choice_dict.keys() and msg.channel == og_channel and msg.author == og_author
        try:
            choice = await self.client.wait_for('message', timeout=10, check=check)
        except TE:
            await ctx.send("You didn't even pick one, MAN!!!", delete_after=10)
            return
        await choice.delete()
        game = str(choice_dict[choice.content])
        await ctx.send("You chose: " + game, delete_after=5)
        await game_dict[game](self, ctx)


def setup(client):
    client.add_cog(cards(client))