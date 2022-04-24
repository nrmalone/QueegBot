import time
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
            await ctx.send('WARNING: In testing phase, nothing you see below is entirely final.\nAlso, "Dealer is bouncing on his thumb"\n')
            deck = list()
            suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
            suits_dict = {x[0]: x for x in suits}
            suitsyms = {'H':'♡', 'D':'♢', 'C':'♧', 'S':'♤'}
            num_dict = {'1': 'Ace', '10': 'X', '11': 'Jack', '12': 'Queen', '13': 'King'}
            snum_dict = {key: num_dict[key][0] for key in num_dict.keys()}
            rnum_dict = {num_dict[key]: int(key) for key in num_dict}
            for suit in suits:
                for n in range(1,14):
                    deck.append(suit + str(n))
            dealer = []
            player = []
            
            def printout(hand:str, *args) -> str:
                """
                Helper function to printout a player's hand
                
                :param hand: str text 'dealer' or 'player' to determine text color
                :*args: accepts any number of cards to print out in a row

                returns string (7 lines long) of a dealer/player's hand in ASCII text
                """
                if type(args[0]) is list:
                    args = args[0]
                cards = {str(i): {} for i in range(len(args))}
                hand_total = 0
                for cardidx in cards:
                    cards[cardidx]['num'] = args[int(cardidx)][len(suits_dict[args[int(cardidx)][0]]):]
                    
                    if int(cards[cardidx]['num']) in (1, 10, 11, 12, 13):
                        if int(cards[cardidx]['num']) != '1':
                            hand_total += 10
                        else:
                            hand_total += 11
                        cards[cardidx]['num'] = snum_dict[cards[cardidx]['num']]
                        cards[cardidx]['suit'] = suitsyms[args[int(cardidx)][0]]
                    else:
                        hand_total += int(cards[cardidx]['num'])
                        cards[cardidx]['suit'] = suitsyms[args[int(cardidx)][0]]
                # final = f"+---+\n {suit}      \n    {num}    \n      {suit} \n+---+"
                iter_range = len(args) if len(args) <= 6 else 6
                final = ("+---+" + "    ") * iter_range + '\n'
                for cardidx in range(iter_range):
                    final += (f" {cards[str(cardidx)]['suit']}" + ' '*7) if cardidx not in (1,5) else (f" {cards[str(cardidx)]['suit']}" + ' '*6)
                final += '\n'
                for cardidx in range(iter_range):
                    # final += "  {:<3}    ".format(cards[str(cardidx)]['num']) if (cardidx % 2) == 0 else "  {:^3}   ".format(cards[str(cardidx)]['num'])
                    final += "  {:<3}    ".format(cards[str(cardidx)]['num'])
                final += '\n'
                for cardidx in range(iter_range):
                    final += (f"   {cards[str(cardidx)]['suit']}" + ' '*5) if cardidx not in (1,5) else (f"   {cards[str(cardidx)]['suit']}" + ' '*4)
                final = '\n' + final + '\n' + ("+---+" + "    ") * iter_range
                hand_total_print = f"Hand total of {hand_total}" if len(args) <= 6 else f"Hand total of {hand_total} (extra cards not shown)"
                return ('```yaml\nDealer\'s Hand\n' + final + f'\n\n{hand_total_print}\n```') if hand == 'dealer' else ('```fix\nYour Hand\n' + final + f'\n\n{hand_total_print}\n```')
            
            for i in range(2):
                card = random.choice(deck)
                dealer.append(card)
            welcome_str = f"Blackjack --- {ctx.message.author.display_name} vs. the House"
            game_msg = await ctx.send(welcome_str, delete_after=120)
            for i in range(4):
                while card in dealer or card in player:
                    card = random.choice(deck)
                player.append(card)
            await game_msg.edit(suppress=False, content=str(game_msg.content + "\n{}".format(printout('dealer', dealer))), delete_after=120)
            await game_msg.edit(suppress=False, content=str(game_msg.content + "\n{}".format(printout('player', player))), delete_after=120)
            async def fullprint():
                nonlocal game_msg, welcome_str, dealer, player
                await game_msg.edit(suppress=False, content=welcome_str+str("\n{}".format(printout('dealer', dealer)))+str("\n{}".format(printout('player', player))), delete_after=120)
            # TESTING fullprint FUNCTIONALITY BELOW
            #
            # time.sleep(2)
            # for i in range(5):
            #     card = random.choice(deck)
            #     dealer.append(card)
            # await fullprint()
            # time.sleep(2)
            # card = random.choice(deck)
            # player.append(card)
            # await fullprint()
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