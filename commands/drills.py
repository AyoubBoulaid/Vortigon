from telegram import Update
from telegram.ext import ContextTypes
from utils.parser import parse_args
import json

async def drills(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = parse_args(context.args, expected=2)
    if not args:
        return await update.message.reply_text("Usage: /drills <role> <goal>")
    role, goal = args
    with open('data/drills.json') as f:
        data = json.load(f)
    drills = data.get(role.lower(), {}).get(goal.lower())
    if not drills:
        return await update.message.reply_text(f"No drills for role '{role}' with goal '{goal}'.")
    text = f"**Drills for {role.title()} to achieve {goal.title()}**\n" + "\n".join(drills)
    await update.message.reply_text(text)
