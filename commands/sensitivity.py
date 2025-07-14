from telegram import Update
from telegram.ext import ContextTypes
from utils.parser import parse_args
import json

async def sensitivity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = parse_args(context.args, expected=1)
    if not args:
        return await update.message.reply_text("Usage: /sensitivity <device>")
    device = args[0].lower()
    with open('data/maps.json') as f:
        data = json.load(f).get('sensitivity', {})
    cfg = data.get(device)
    if not cfg:
        return await update.message.reply_text(f"No preset for device '{device}'.")
    text = f"**Sensitivity for {device.title()}**\n"
    for k, v in cfg.items():
        text += f"- {k.replace('_',' ').title()}: {v}\n"
    await update.message.reply_text(text)
