"""
dpy-layout-builder
===================
A fluent builder pattern for creating Discord UI LayoutViews with containers.

Quick start::

    from dpy_layout_builder import LayoutViewBuilder

    view = (
        LayoutViewBuilder()
        .set_accent_color(discord.Color.blurple())
        .add_header("# Welcome!")
        .add_separator()
        .add_text("Hello there!")
        .add_button("Click", style=discord.ButtonStyle.primary, callback=my_func)
        .build()
    )
    await interaction.response.send_message(view=view)
"""

from .builder import (
    ButtonConfig,
    SelectOptionConfig,
    SelectConfig,
    LayoutViewBuilder,
    MultiContainerLayoutViewBuilder,
    quick_info_view,
    quick_confirm_view,
)

__all__ = [
    "ButtonConfig",
    "SelectOptionConfig",
    "SelectConfig",
    "LayoutViewBuilder",
    "MultiContainerLayoutViewBuilder",
    "quick_info_view",
    "quick_confirm_view",
]

__version__ = "1.0.0"
