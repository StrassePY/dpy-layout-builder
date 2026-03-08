"""Core builder classes for creating Discord UI LayoutViews."""

import discord
from discord import ui
from typing import Optional, Callable, List, Any, Union
from dataclasses import dataclass, field


@dataclass
class ButtonConfig:
    """Configuration for a button accessory on a Section."""

    label: str
    style: discord.ButtonStyle = discord.ButtonStyle.secondary
    emoji: Optional[str] = None
    callback: Optional[Callable] = None
    custom_id: Optional[str] = None
    disabled: bool = False
    url: Optional[str] = None


@dataclass
class SelectOptionConfig:
    """Configuration for a select menu option."""

    label: str
    value: str
    description: Optional[str] = None
    emoji: Optional[str] = None


@dataclass
class SelectConfig:
    """Configuration for a select menu."""

    placeholder: str
    options: List[SelectOptionConfig] = field(default_factory=list)
    callback: Optional[Callable] = None
    min_values: int = 1
    max_values: int = 1


class LayoutViewBuilder:
    """A fluent builder for creating Discord UI LayoutViews with containers.

    All ``add_*`` methods return ``self`` so calls can be chained.
    Call :meth:`build` to produce the final :class:`discord.ui.LayoutView`.

    Example::

        view = (
            LayoutViewBuilder()
            .set_accent_color(discord.Color.blurple())
            .add_header("# Welcome!")
            .add_separator()
            .add_section("Hello!", thumbnail_url="https://example.com/avatar.png")
            .add_button("Click", style=discord.ButtonStyle.primary, callback=my_func)
            .build()
        )
    """

    def __init__(self) -> None:
        self._items: List[Any] = []
        self._accent_color: Optional[discord.Color] = None
        self._spoiler: bool = False
        self._pending_buttons: List[ui.Button] = []
        self._callbacks: List[tuple] = []

    # -- Configuration --------------------------------------------------------

    def set_accent_color(self, color: discord.Color) -> "LayoutViewBuilder":
        """Set the accent color for the container."""
        self._accent_color = color
        return self

    def set_spoiler(self, spoiler: bool = True) -> "LayoutViewBuilder":
        """Set whether the container is a spoiler."""
        self._spoiler = spoiler
        return self

    # -- Content items --------------------------------------------------------

    def add_header(self, text: str) -> "LayoutViewBuilder":
        """Add a header text display (use markdown headings, e.g. ``# Title``)."""
        self._flush_buttons()
        self._items.append(ui.TextDisplay(text))
        return self

    def add_text(self, text: str) -> "LayoutViewBuilder":
        """Add a text display."""
        self._flush_buttons()
        self._items.append(ui.TextDisplay(text))
        return self

    def add_separator(self) -> "LayoutViewBuilder":
        """Add a visual separator line."""
        self._flush_buttons()
        self._items.append(ui.Separator())
        return self

    def add_section(
        self,
        text: Union[str, List[str]],
        *,
        thumbnail_url: Optional[str] = None,
        thumbnail_description: Optional[str] = None,
        button: Optional[ButtonConfig] = None,
    ) -> "LayoutViewBuilder":
        """Add a section with text and an optional thumbnail or button accessory.

        Parameters
        ----------
        text:
            Text content, or a list of lines to join with newlines.
        thumbnail_url:
            URL for a thumbnail accessory.
        thumbnail_description:
            Alt text for the thumbnail.
        button:
            A :class:`ButtonConfig` for a button accessory.
        """
        self._flush_buttons()

        if isinstance(text, list):
            text = "\n".join(text)

        text_display = ui.TextDisplay(text)

        accessory = None
        if thumbnail_url:
            accessory = ui.Thumbnail(
                media=thumbnail_url,
                description=thumbnail_description,
            )
        elif button:
            btn = ui.Button(
                label=button.label,
                style=button.style,
                emoji=button.emoji,
                custom_id=button.custom_id,
                disabled=button.disabled,
                url=button.url,
            )
            if button.callback:
                self._callbacks.append((btn, button.callback))
            accessory = btn

        if accessory:
            self._items.append(ui.Section(text_display, accessory=accessory))
        else:
            self._items.append(text_display)
        return self

    # -- Interactive items ----------------------------------------------------

    def add_button(
        self,
        label: str,
        *,
        style: discord.ButtonStyle = discord.ButtonStyle.secondary,
        emoji: Optional[str] = None,
        callback: Optional[Callable] = None,
        custom_id: Optional[str] = None,
        disabled: bool = False,
        url: Optional[str] = None,
    ) -> "LayoutViewBuilder":
        """Add a button. Consecutive buttons are grouped into ActionRows (max 5 per row).

        Parameters
        ----------
        label:
            Button label text.
        style:
            One of ``primary``, ``secondary``, ``success``, ``danger``, ``link``.
        emoji:
            Optional emoji shown on the button.
        callback:
            Async function called when the button is clicked.
        custom_id:
            Custom ID for persistent buttons.
        disabled:
            Whether the button is disabled.
        url:
            URL for link-style buttons.
        """
        btn = ui.Button(
            label=label,
            style=style,
            emoji=emoji,
            custom_id=custom_id,
            disabled=disabled,
            url=url,
        )
        if callback:
            self._callbacks.append((btn, callback))

        self._pending_buttons.append(btn)
        return self

    def add_select(
        self,
        placeholder: str,
        options: List[Union[SelectOptionConfig, str]],
        *,
        callback: Optional[Callable] = None,
        min_values: int = 1,
        max_values: int = 1,
        custom_id: Optional[str] = None,
        disabled: bool = False,
    ) -> "LayoutViewBuilder":
        """Add a select (dropdown) menu.

        Parameters
        ----------
        placeholder:
            Placeholder text shown when nothing is selected.
        options:
            A list of :class:`SelectOptionConfig` or plain strings.
        callback:
            Async function called when a selection is made.
        min_values:
            Minimum number of selections.
        max_values:
            Maximum number of selections.
        custom_id:
            Custom ID for persistent selects.
        disabled:
            Whether the select is disabled.
        """
        self._flush_buttons()

        select_options: List[discord.SelectOption] = []
        for opt in options:
            if isinstance(opt, str):
                select_options.append(discord.SelectOption(label=opt, value=opt))
            else:
                select_options.append(
                    discord.SelectOption(
                        label=opt.label,
                        value=opt.value,
                        description=opt.description,
                        emoji=opt.emoji,
                    )
                )

        select_kwargs = {
            "placeholder": placeholder,
            "options": select_options,
            "min_values": min_values,
            "max_values": max_values,
            "disabled": disabled,
        }
        if custom_id is not None:
            select_kwargs["custom_id"] = custom_id

        select = ui.Select(**select_kwargs)

        if callback:
            self._callbacks.append((select, callback))

        self._items.append(ui.ActionRow(select))
        return self

    # -- Media items ----------------------------------------------------------

    def add_media_gallery(self, *urls: str) -> "LayoutViewBuilder":
        """Add a media gallery with up to 10 images."""
        self._flush_buttons()
        items = [discord.MediaGalleryItem(media=url) for url in urls[:10]]
        self._items.append(ui.MediaGallery(*items))
        return self

    def add_file(
        self,
        url: str,
        *,
        filename: Optional[str] = None,
        spoiler: bool = False,
    ) -> "LayoutViewBuilder":
        """Add a file display."""
        self._flush_buttons()
        self._items.append(ui.File(media=url, filename=filename, spoiler=spoiler))
        return self

    # -- Escape hatch ---------------------------------------------------------

    def add_raw_item(self, item: Any) -> "LayoutViewBuilder":
        """Add any ``discord.ui`` component directly."""
        self._flush_buttons()
        self._items.append(item)
        return self

    # -- Internal helpers -----------------------------------------------------

    def _flush_buttons(self) -> None:
        """Flush pending buttons into ActionRows."""
        if self._pending_buttons:
            for i in range(0, len(self._pending_buttons), 5):
                batch = self._pending_buttons[i : i + 5]
                self._items.append(ui.ActionRow(*batch))
            self._pending_buttons = []

    def _build_items(self) -> List[Any]:
        """Return a snapshot of items with pending buttons flushed (non-mutating)."""
        items = list(self._items)
        if self._pending_buttons:
            for i in range(0, len(self._pending_buttons), 5):
                batch = self._pending_buttons[i : i + 5]
                items.append(ui.ActionRow(*batch))
        return items

    def _container_kwargs(self) -> dict:
        """Build keyword arguments for the Container."""
        kwargs: dict[str, Any] = {}
        if self._accent_color is not None:
            kwargs["accent_color"] = self._accent_color
        if self._spoiler:
            kwargs["spoiler"] = self._spoiler
        return kwargs

    @staticmethod
    def _apply_callbacks(callbacks: List[tuple]) -> None:
        """Bind async callbacks to components with proper closure scoping."""
        for component, callback in callbacks:

            async def _wrap(interaction: discord.Interaction, *, _cb=callback):
                await _cb(interaction)

            component.callback = _wrap

    # -- Build ----------------------------------------------------------------

    def build(self, timeout: float | None = 180.0) -> ui.LayoutView:
        """Build and return the :class:`~discord.ui.LayoutView`.

        Safe to call multiple times - builder state is not mutated.
        """
        items = self._build_items()
        callbacks = list(self._callbacks)

        view = ui.LayoutView(timeout=timeout)
        container = ui.Container(*items, **self._container_kwargs())
        view.add_item(container)

        self._apply_callbacks(callbacks)
        return view

    def build_container_only(self) -> ui.Container:
        """Build and return just the :class:`~discord.ui.Container`.

        Useful with :class:`MultiContainerLayoutViewBuilder`.
        """
        items = self._build_items()
        callbacks = list(self._callbacks)

        container = ui.Container(*items, **self._container_kwargs())
        self._apply_callbacks(callbacks)
        return container


class MultiContainerLayoutViewBuilder:
    """Builder for LayoutViews with multiple containers.

    Example::

        view = (
            MultiContainerLayoutViewBuilder()
            .add_container(
                LayoutViewBuilder()
                .set_accent_color(discord.Color.red())
                .add_header("# Container 1")
                .add_text("First container")
            )
            .add_container(
                LayoutViewBuilder()
                .set_accent_color(discord.Color.blue())
                .add_header("# Container 2")
                .add_text("Second container")
            )
            .build()
        )
    """

    def __init__(self) -> None:
        self._containers: List[ui.Container] = []

    def add_container(self, builder: LayoutViewBuilder) -> "MultiContainerLayoutViewBuilder":
        """Add a container built from a :class:`LayoutViewBuilder`."""
        self._containers.append(builder.build_container_only())
        return self

    def add_raw_container(self, container: ui.Container) -> "MultiContainerLayoutViewBuilder":
        """Add a pre-built :class:`~discord.ui.Container` directly."""
        self._containers.append(container)
        return self

    def build(self, timeout: float | None = 180.0) -> ui.LayoutView:
        """Build and return the LayoutView with all containers."""
        view = ui.LayoutView(timeout=timeout)
        for container in self._containers:
            view.add_item(container)
        return view


# -- Convenience functions ----------------------------------------------------


def quick_info_view(
    title: str,
    description: str,
    *,
    color: discord.Color = discord.Color.blurple(),
    thumbnail_url: Optional[str] = None,
    footer: Optional[str] = None,
) -> ui.LayoutView:
    """Create a simple info view with title, description, and optional footer.

    Example::

        view = quick_info_view(
            "# Announcement",
            "This is an important message!",
            color=discord.Color.gold(),
            footer="*Last updated: today*",
        )
    """
    builder = (
        LayoutViewBuilder()
        .set_accent_color(color)
        .add_header(title)
        .add_separator()
    )

    if thumbnail_url:
        builder.add_section(description, thumbnail_url=thumbnail_url)
    else:
        builder.add_text(description)

    if footer:
        builder.add_separator()
        builder.add_text(footer)

    return builder.build()


def quick_confirm_view(
    message: str,
    *,
    on_confirm: Optional[Callable] = None,
    on_cancel: Optional[Callable] = None,
    confirm_label: str = "Confirm",
    cancel_label: str = "Cancel",
    color: discord.Color = discord.Color.blurple(),
) -> ui.LayoutView:
    """Create a confirmation view with confirm/cancel buttons.

    Example::

        view = quick_confirm_view(
            "Are you sure you want to proceed?",
            on_confirm=handle_confirm,
            on_cancel=handle_cancel,
        )
    """
    return (
        LayoutViewBuilder()
        .set_accent_color(color)
        .add_text(message)
        .add_separator()
        .add_button(confirm_label, style=discord.ButtonStyle.success, emoji="\u2705", callback=on_confirm)
        .add_button(cancel_label, style=discord.ButtonStyle.danger, emoji="\u274c", callback=on_cancel)
        .build()
    )
