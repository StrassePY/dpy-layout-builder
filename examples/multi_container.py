"""Multi-container example - a dashboard with separate panels."""

import discord
from discord import app_commands
from dpy_layout_builder import LayoutViewBuilder, MultiContainerLayoutViewBuilder


bot = discord.Client(intents=discord.Intents.default())
tree = app_commands.CommandTree(bot)


@tree.command(name="dashboard", description="Show a multi-panel dashboard")
async def dashboard_command(interaction: discord.Interaction):
    view = (
        MultiContainerLayoutViewBuilder()
        .add_container(
            LayoutViewBuilder()
            .set_accent_color(discord.Color.gold())
            .add_header("# Stats")
            .add_separator()
            .add_text("**Members:** 1,234\n**Online:** 567\n**Messages today:** 8,901")
        )
        .add_container(
            LayoutViewBuilder()
            .set_accent_color(discord.Color.green())
            .add_header("# Recent Activity")
            .add_separator()
            .add_text("- Strasse leveled up to **42**\n- New suggestion posted\n- 3 tickets resolved")
        )
        .build()
    )

    await interaction.response.send_message(view=view)
