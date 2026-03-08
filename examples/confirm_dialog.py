"""Confirmation dialog example - ask the user before proceeding."""

import discord
from discord import app_commands
from dpy_layout_builder import quick_confirm_view


bot = discord.Client(intents=discord.Intents.default())
tree = app_commands.CommandTree(bot)


@tree.command(name="reset", description="Reset your progress")
async def reset_command(interaction: discord.Interaction):
    async def on_confirm(btn_interaction: discord.Interaction):
        await btn_interaction.response.edit_message(
            content="Progress has been reset.", view=None
        )

    async def on_cancel(btn_interaction: discord.Interaction):
        await btn_interaction.response.edit_message(
            content="Cancelled.", view=None
        )

    view = quick_confirm_view(
        "Are you sure you want to reset all your progress? This cannot be undone.",
        on_confirm=on_confirm,
        on_cancel=on_cancel,
        color=discord.Color.red(),
    )

    await interaction.response.send_message(view=view, ephemeral=True)
