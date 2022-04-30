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
            # print("Poker game starting...")
            await ctx.send("I'm not ready for that, MAN!", delete_after=10)
            pass


        async def blackjack(self, ctx):
            print("Blackjack game starting...")
            deck = list()
            suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
            suits_dict = {x[0]: x for x in suits}
            suitsyms = {'H':'♡', 'D':'♢', 'C':'♧', 'S':'♤'}
            num_dict = {'1': 'Ace', '10': 'X', '11': 'Jack', '12': 'Queen', '13': 'King'}
            snum_dict = {key: num_dict[key][0] for key in num_dict.keys()}
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
                    args = list(args[0])
                else:
                    args = list(args)
                cards = {str(i): {} for i in range(len(args))}
                hand_total = 0
                hidden = False
                for cardidx in cards:
                    cards[cardidx]['num'] = args[int(cardidx)][len(suits_dict[args[int(cardidx)][0]]):]
                    
                    if int(cards[cardidx]['num']) in (1, 10, 11, 12, 13):
                        if cards[cardidx]['num'] != '1':
                            hand_total += 10
                        else:
                            hand_total += 11
                        cards[cardidx]['num'] = snum_dict[cards[cardidx]['num']]
                        cards[cardidx]['suit'] = suitsyms[args[int(cardidx)][0]]
                    else:
                        hand_total += int(cards[cardidx]['num'])
                        cards[cardidx]['suit'] = suitsyms[args[int(cardidx)][0]]
                if hand_total != 21 and hand == 'dealer' and len(cards) == 2:
                    hidden = True
                    if cards['1']['num'] in ('J', 'Q', 'K'):
                        hand_total -= 10
                    elif cards['1']['num'] == 'A':
                        hand_total -= 11
                    else:
                        hand_total -= int(cards['1']['num'])
                    cards['1']['num'] = '?'
                    cards['1']['suit'] = '?'
                iter_range = len(args) if len(args) <= 6 else 6
                final = ("+---+" + "    ") * iter_range + '\n'
                for cardidx in range(iter_range):
                    final += (f" {cards[str(cardidx)]['suit']}" + ' '*7) if cardidx not in (1,5) else (f" {cards[str(cardidx)]['suit']}" + ' '*6)
                final += '\n'
                for cardidx in range(iter_range):
                    final += "  {:<3}    ".format(cards[str(cardidx)]['num'])
                final += '\n'
                for cardidx in range(iter_range):
                    final += (f"   {cards[str(cardidx)]['suit']}" + ' '*5) if cardidx not in (1,5) else (f"   {cards[str(cardidx)]['suit']}" + ' '*4)
                final = '\n' + final + '\n' + ("+---+" + "    ") * iter_range
                if hand_total > 21:
                    for cardidx in range(len(cards)):
                        if cards[str(cardidx)]['num'] == 'A':
                            hand_total -= 10
                if hidden:
                    hand_total = str(hand_total) + " (?)"
                hand_total_print = f"Hand total of {hand_total}" if len(args) <= 6 else f"Hand total of {hand_total} (extra cards not shown)"
                if hidden:
                    hand_total = int(hand_total[:-4])
                return ('```yaml\nDealer\'s Hand\n' + final + f'\n\n{hand_total_print}\n```', hand_total) if hand in ('dealer', 'dealerT') else ('```fix\nYour Hand\n' + final + f'\n\n{hand_total_print}\n```', hand_total)
            
            welcome_str = f"Blackjack --- {ctx.message.author.display_name} vs. the House"
            game_msg = await ctx.send(welcome_str, delete_after=120)
            for i in range (2):
                card = random.choice(deck)
                dealer.append(card)
            for i in range (2):
                card = random.choice(deck)
                player.append(card)
            async def fullprint(show_true: bool=False):
                """
                Helper function to automatically fill printout parameters
                for seamless message editing (updates Discord message to
                reflect current game state)

                returns (<dealer hand value: int>, <player hand value: int>)
                """
                nonlocal game_msg, welcome_str, dealer, player
                dealer_print = printout('dealerT', dealer) if show_true else printout('dealer', dealer)
                player_print = printout('player', player)
                await game_msg.edit(suppress=False, content=welcome_str+str("\n{}".format(dealer_print[0]))+str("\n{}".format(player_print[0])), delete_after=120)
                return (dealer_print[1], player_print[1])
            
            dealer_total, player_total = await fullprint()
            if dealer_total == 21:
                await game_msg.edit(content=(game_msg.content + "\n" + "You already lost man, I had BLACKJACK, MAAANNNN!!!"), delete_after=60)
                return
            if player_total == 21:
                await game_msg.edit(content=(game_msg.content + "\n" + "I guess you win, maannnn..."), delete_after=60)
                return
            while player_total < 21:
                choice_inp = await ctx.send("What are you gonna do now, MAN?", delete_after=10)
                def check(msg):
                    """
                    Checks that the original user is responding, 
                    in the same channel, and with a valid choice
                    from "s", "stand", "h", "hit"
                    """
                    return msg.content.lower() in ("s", "h", "stand", "hit") and msg.channel == og_channel and msg.author == og_author
                try:
                    choice = await self.client.wait_for('message', timeout=10, check=check)
                    await choice_inp.delete()
                except TE:
                    await ctx.send("I guess you're just gonna stand then, MAN!!!", delete_after=10)
                    break
                if choice.content in ("stand", "s"):
                    await choice.delete()
                    break
                await choice.delete()
                card = random.choice(deck)
                player.append(card)
                dealer_total, player_total = await fullprint()
            if player_total > 21:
                await game_msg.edit(content=(game_msg.content + "\n" + "You bust, you LOSE, MAN!!!"), delete_after=60)
                return
            dealer_total, player_total = await fullprint(True)
            while dealer_total < 17:
                card = random.choice(deck)
                dealer.append(card)
                dealer_total, player_total = await fullprint()
            if dealer_total > 21:
                await game_msg.edit(content=(game_msg.content + "\n" + "I bust, you win, man..."), delete_after=60)
                return
            if dealer_total > player_total:
                await game_msg.edit(content=(game_msg.content + "\n" + "You've got a shit hand, and therefore I win, MAN!!!"), delete_after=60)
                return
            elif player_total > dealer_total:
                await game_msg.edit(content=(game_msg.content + "\n" + "This game fucking sucks anyway, man!"), delete_after=60)
                return
            if len(dealer) == len(player):
                await game_msg.edit(content=(game_msg.content + "\n" + "Why are you just COPYING me, MAN???"), delete_after=60)
                return
            else:
                await game_msg.edit(content=(game_msg.content + "\n" + "Looks like we're the same, MAN!"), delete_after=60)


        async def speed(self, ctx):
            # print("Speed game starting...")
            await ctx.send("I'm not ready for that, MAN!", delete_after=10)
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