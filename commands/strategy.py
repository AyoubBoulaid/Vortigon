from telegram import Update
from telegram.ext import ContextTypes
from utils.parser import parse_args
import json

async def strategy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = parse_args(context.args, expected=2)
    if not args:
        return await update.message.reply_text("Usage: /strategy <mode> <map>")
    mode, map_name = args
    with open('data/maps.json') as f:
        data = json.load(f).get(mode.lower(), {})
    tips = data.get(map_name.lower())
    if not tips:
        return await update.message.reply_text(f"No strategy for {mode.title()} on {map_name.title()}.")
    text = f"**{mode.title()} on {map_name.title()} Strategy**\n" + "\n".join(tips)
    await update.message.reply_text(text)
