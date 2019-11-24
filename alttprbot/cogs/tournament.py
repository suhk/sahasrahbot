import discord
from discord.ext import commands
import pyz3r

from config import Config as c
from ..database import config

from ..util import checks, embed_formatter, http
from ..tournament import main

# this module was only intended for the Main Tournament 2019
# we will probably expand this later to support other tournaments in the future

class Tournament(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        if ctx.guild.id in c.Tournament:
            return True
        else:
            return False


    @commands.command()
    @checks.has_any_channel('testing','console','lobby','restreamers','sg-races')
    async def tourneyrace(self, ctx, episode_number: int):
        if c.Tournament[ctx.guild.id]['tournament'] == 'main':
            seed, game_number, players = await main.generate_game(episode_number, ctx.guild.id)

        embed = await embed_formatter.seed_embed(
            seed,
            name=f"{players[0]['displayName']} vs. {players[1]['displayName']}",
            emojis=self.bot.emojis
        )

        logging_channel = discord.utils.get(ctx.guild.text_channels, id=c.Tournament[ctx.guild.id]['logging_channel'])
        await logging_channel.send(embed=embed)

        converter = commands.MemberConverter()
        for player in players:
            try:
                member = await converter.convert(ctx, player['discordTag'])
                await member.send(embed=embed)
            except:
                await logging_channel.send(f"Unable to send DM to {player['discordTag']}")

def setup(bot):
    bot.add_cog(Tournament(bot))
