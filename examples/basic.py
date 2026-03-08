"""Basic example - a simple info panel with a button."""

import discord
from discord import app_commands
from dpy_layout_builder import LayoutViewBuilder


bot = discord.Client(intents=discord.Intents.default())
tree = app_commands.CommandTree(bot)


@tree.command(name="info", description="Show an info panel")
async def info_command(interaction: discord.Interaction):
    async def on_click(btn_interaction: discord.Interaction):
        await btn_interaction.response.send_message("You clicked it!", ephemeral=True)

    view = (
        LayoutViewBuilder()
        .set_accent_color(discord.Color.blurple())
        .add_header("# Welcome to the Server!")
        .add_separator()
        .add_text("We're glad to have you here. Check out the rules and have fun!")
        .add_separator()
        .add_button("Got it!", style=discord.ButtonStyle.primary, callback=on_click)
        .build()
    )

    await interaction.response.send_message(view=view)
