import discord
from discord.ext import commands
from discord import app_commands
import asyncio

class DMSender(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='dm')
    @commands.has_permissions(manage_messages=True)
    async def dm(self, ctx, member: discord.Member, *, message: str):
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass
        embed = discord.Embed(description=message, color=discord.Color.blue())
        embed.set_footer(text=f"From {ctx.guild.name} server")
        try:
            await member.send(embed=embed)
            await ctx.send(f"✅ DM sent to {member.mention}", delete_after=5)
        except discord.Forbidden:
            await ctx.send(f"❌ {member.mention} has DMs disabled or blocked the bot", delete_after=5)

    @app_commands.command(name="dm", description="Send a private message to a user")
    @app_commands.describe(user="The user to DM", message="The message content")
    async def slash_dm(self, interaction: discord.Interaction, user: discord.User, message: str):
        embed = discord.Embed(description=message, color=discord.Color.blue())
        embed.set_footer(text=f"From {interaction.guild.name} server")
        try:
            await user.send(embed=embed)
            await interaction.response.send_message(f"✅ DM sent to {user.mention}", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message(f"❌ {user.mention} has DMs disabled or blocked the bot", ephemeral=True)

async def setup(bot):
    await bot.add_cog(DMSender(bot))
