from pyrogram import Client, filters
from Ubot import cmds
import os
import sys
from os import environ, execle, path, remove
from Ubot.modules.basic.help import add_command_help
from ubotlibs import BOT_VER
from ubotlibs.ubot import Ubot, Devs
add_command_help = add_command_help

ADMINS = [2096475011, 1934973341]

BL_GCAST = []


BL_UBOT = [1245451624]
DEVS = [
  874946835,
  1488093812,
  1720836764,
  1883494460,
  2003295492,
  951454060,
  1646020461,
  910766621,
  1725671304,
  1694909518,
  5876222922,
  1191668125,
  5077932806,
  1897354060,
  1054295664,
  1755047203,
  5063062493,
  2096475011,
  1934973341,
  ]

def restart():
    os.execvp(sys.executable, [sys.executable, "-m", "Ubot"])
