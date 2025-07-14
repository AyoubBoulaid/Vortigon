import json
import os
from telegram import Update
from telegram.ext import ContextTypes
from utils.parser import parse_args

# Compute where data lives, relative to this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')
WEAPONS_FILE = os.path.join(DATA_DIR, 'weapons.json')

# Load once at import‐time
with open(WEAPONS_FILE, 'r', encoding='utf-8') as f:
    WEAPONS = json.load(f)

async def loadout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = parse_args(context.args, expected=2)
    if not args:
        return await update.message.reply_text("Usage: /loadout <weapon> <mode>")

    weapon, mode = args
    weapon_data = WEAPONS.get(weapon.lower())
    if not weapon_data:
        return await update.message.reply_text(f"🔍 Couldn’t find a weapon named “{weapon}.”")

    cfg = weapon_data.get(mode.lower())
    if not cfg:
        return await update.message.reply_text(f"⚙️ No loadout configured for “{mode}” with “{weapon}.”")

    text = f"**Meta {weapon.upper()} Loadout for {mode.title()}**\n"
    for attachment, name in cfg.items():
        # e.g. "rear_grip" → "Rear Grip"
        label = attachment.replace('_', ' ').title()
        text += f"- {label}: {name}\n"

    await update.message.reply_text(text)
