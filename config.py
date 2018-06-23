# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile.config import Key, Screen, Group, Drag, Click, Match, \
    ScratchPad, DropDown
from libqtile.command import lazy
from libqtile import layout, bar, widget
from Xlib.ext import randr
from keys import *
import re

import math

mod = "mod4"

keys = [
    # Switch between windows in current stack pane
    Key([mod], "k", lazy.layout.down()),
    Key([mod], "j", lazy.layout.up()),

    # Move windows up or down in current stack
    Key([mod, "control"], "k", lazy.layout.shuffle_down()),
    Key([mod, "control"], "j", lazy.layout.shuffle_up()),

    # Switch window focus to other pane(s) of stack
    Key([mod], "space", lazy.layout.next()),

    # Swap panes of split stack
    Key([mod, "shift"], "space", lazy.layout.rotate()),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split()),
    Key([mod], "Return", lazy.spawn("terminator")),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod], "w", lazy.window.kill()),

    Key([mod, "control"], "r", lazy.restart()),
    Key([mod, "control"], "q", lazy.shutdown()),
    Key([mod], "r", lazy.spawncmd()),

    Key([mod], "Left", lazy.screen.prev_group()),
    Key([mod], "Right", lazy.screen.next_group()),

    # Audio Keys
    Key([], "XF86AudioMute", lazy.spawn("pamixer -t")),
    Key([], "XF86AudioLowerVolume",
        lazy.spawn("pamixer -d 4 -u")),

    Key([], "XF86AudioRaiseVolume",
        lazy.spawn("pamixer -i 4 -u")),

    # Brightness Keys
    # Key([], "XF86MonBrightnessUp", lazy.spawn("acpilight -inc 10")),
    # Key([], "XF86MonBrightnessDown", lazy.spawn("acpilight -dec 10")),
]


group_configs = [
    {
        "name": "a",
        "label": "Chrome",
        "spawn": "google-chrome-stable",
        "exclusive": False,
        "matches": [Match(wm_class=["google-chrome"])],
    },
    {
        "name": "s",
        "label": "Slack",
        "spawn": "slack",
        "exclusive": True,
        "matches": [Match(wm_class=["slack"])],
    },
    {
        "name": "d",
        "label": "d",
    },
    {
        "name": "f",
        "label": "f",
    },
    {
        "name": "u",
        "label": "u",
    },
    {
        "name": "i",
        "label": "Gryphon",
        "spawn": "pycharm",
        "exclusive": True,
        "matches": [Match(title=[re.compile("gryphon .*")])],
    },
    {
        "name": "o",
        "label": "Codebooks",
        "exclusive": True,
        "matches": [Match(title=[re.compile("codebooks .*")])],
    },
    {
        "name": "p",
        "label": "p",
    },
]

groups = []

for gconf in group_configs:
    groups.append(Group(**gconf))

for i in groups[1:]:
    keys.extend([
        # mod1 + letter of group = switch to group
        Key([mod], i.name, lazy.group[i.name].toscreen()),

        # mod1 + shift + letter of group = switch to & move focused window to group
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name)),
    ])

layouts = [
    layout.Max(),
    layout.Stack(num_stacks=2),
    layout.VerticalTile()
]

widget_defaults = dict(
    font='sans',
    fontsize=36,
    padding=9,
)
extension_defaults = widget_defaults.copy()

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
])
auto_fullscreen = True
focus_on_window_activation = "smart"

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, github issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"


def new_bar(groups):
    default_bar = [
        (widget.GroupBox, [], {
            "highlight_method": "line",
            "highlight_color": ['000023', '215578'],
            "disable_drag": True,
            "borderwidth": 4,
            "other_screen_border": "87aabc",
            "other_current_screen_border": "87aabc",
            "visible_groups": groups,
        }),
        (widget.Spacer, [36], {}),
        (widget.Prompt, [], {}),
        (widget.TaskList, [], {
            "highlight_method": "line",
            "highlight_color": ['000023', '215578'],
            "rounded": False,
            "padding_y": 24,
            "padding_x": 18,
            "icon_size": 50,
            "urgent_border": "230000",
            "borderwidth": 0,
        }),
       (widget.Volume, [], {"step": 1}),
        (widget.Clock, [], {"format": '%a, %b %d %H:%M:%S'}),
    ]

    return list(map(lambda x: x[0](*x[1], **x[2]), default_bar))


PRIMARY_BAR = new_bar([i for i in "asdf"])
PRIMARY_BAR.insert(-1, widget.Systray(icon_size=86, padding=math.floor(widget_defaults.get("padding")*1.5)))
PRIMARY_BAR.insert(-1, widget.Spacer(24))

screens = [
    Screen(
        top=bar.Bar(
            PRIMARY_BAR,
            96,
        ),
    ),
    Screen(
        top=bar.Bar(
            new_bar([i for i in "uiop"]),
            96,
        ),
    ),
]

