# dpy-layout-builder

A fluent builder pattern for creating **Discord UI LayoutViews** with containers in [discord.py](https://github.com/Rapptz/discord.py).

Stop wrestling with nested `Container`, `ActionRow`, `Section`, and `TextDisplay` calls - chain a few methods and `.build()`.

[![PyPI](https://img.shields.io/pypi/v/dpy-layout-builder)](https://pypi.org/project/dpy-layout-builder/)
[![Python](https://img.shields.io/pypi/pyversions/dpy-layout-builder)](https://pypi.org/project/dpy-layout-builder/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![discord.py](https://img.shields.io/badge/discord.py-%E2%89%A52.6-5865F2)](https://github.com/Rapptz/discord.py)

## Installation

```bash
pip install dpy-layout-builder
```

## Quick Start

```python
import discord
from dpy_layout_builder import LayoutViewBuilder

async def my_callback(interaction: discord.Interaction):
    await interaction.response.send_message("Clicked!", ephemeral=True)

view = (
    LayoutViewBuilder()
    .set_accent_color(discord.Color.blurple())
    .add_header("# Welcome!")
    .add_separator()
    .add_text("Thanks for checking out the server.")
    .add_separator()
    .add_button("Get Started", style=discord.ButtonStyle.primary, callback=my_callback)
    .build()
)

await interaction.response.send_message(view=view)
```

## Features

| Method | Description |
|---|---|
| `.set_accent_color(color)` | Set the container accent color |
| `.set_spoiler(True)` | Mark the container as a spoiler |
| `.add_header(text)` | Add a heading (use `# markdown`) |
| `.add_text(text)` | Add a text block |
| `.add_separator()` | Add a visual divider |
| `.add_section(text, ...)` | Add a section with optional thumbnail or button accessory |
| `.add_button(label, ...)` | Add a button (auto-grouped into ActionRows, max 5 per row) |
| `.add_select(placeholder, options, ...)` | Add a dropdown select menu |
| `.add_media_gallery(*urls)` | Add an image gallery (up to 10) |
| `.add_file(url, ...)` | Add a file display |
| `.add_raw_item(item)` | Escape hatch - add any `discord.ui` component |
| `.build(timeout=180)` | Build the final `LayoutView` |

## Examples

### Section with Thumbnail

```python
view = (
    LayoutViewBuilder()
    .set_accent_color(discord.Color.green())
    .add_header("# User Profile")
    .add_separator()
    .add_section(
        "**Username:** Strasse\n**Level:** 42\n**Joined:** 2024",
        thumbnail_url="https://example.com/avatar.png",
    )
    .build()
)
```

### Section with Button Accessory

```python
from dpy_layout_builder import LayoutViewBuilder, ButtonConfig

view = (
    LayoutViewBuilder()
    .add_section(
        "Click the button to claim your reward!",
        button=ButtonConfig(
            label="Claim",
            style=discord.ButtonStyle.success,
            callback=claim_callback,
        ),
    )
    .build()
)
```

### Multiple Buttons

```python
view = (
    LayoutViewBuilder()
    .set_accent_color(discord.Color.red())
    .add_text("Choose an action:")
    .add_separator()
    .add_button("Approve", style=discord.ButtonStyle.success, callback=approve)
    .add_button("Deny", style=discord.ButtonStyle.danger, callback=deny)
    .add_button("Skip", style=discord.ButtonStyle.secondary, callback=skip)
    .build()
)
```

### Select Menu

```python
view = (
    LayoutViewBuilder()
    .add_text("Pick your favorite color:")
    .add_select(
        "Choose a color...",
        ["Red", "Green", "Blue", "Purple"],
        callback=color_chosen,
    )
    .build()
)
```

### Multiple Containers

```python
from dpy_layout_builder import LayoutViewBuilder, MultiContainerLayoutViewBuilder

view = (
    MultiContainerLayoutViewBuilder()
    .add_container(
        LayoutViewBuilder()
        .set_accent_color(discord.Color.red())
        .add_header("# Warnings")
        .add_text("You have 2 active warnings.")
    )
    .add_container(
        LayoutViewBuilder()
        .set_accent_color(discord.Color.green())
        .add_header("# Rewards")
        .add_text("You earned 500 XP today!")
    )
    .build()
)
```

### Quick Helpers

```python
from dpy_layout_builder import quick_info_view, quick_confirm_view

# Simple info display
info = quick_info_view(
    "# Server Rules",
    "1. Be respectful\n2. No spam\n3. Have fun!",
    color=discord.Color.gold(),
    footer="*Last updated: March 2026*",
)

# Confirmation dialog
confirm = quick_confirm_view(
    "Are you sure you want to reset your progress?",
    on_confirm=handle_confirm,
    on_cancel=handle_cancel,
)
```

## Build Safety

The builder is safe to call `.build()` multiple times - it snapshots internal state without mutating, so you can reuse a configured builder to produce multiple views.

## Requirements

- Python 3.10+
- discord.py 2.6+ (with LayoutView / Components V2 support)

## License

[MIT](LICENSE)
