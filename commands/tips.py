from telegram import Update
from telegram.ext import ContextTypes
from utils.parser import parse_args

async def tips(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = parse_args(context.args, expected=2)
    if not args:
        return await update.message.reply_text("Usage: /tips <current_kd> <target_kd>")
    current, target = args
    try:
        cur = float(current)
        tgt = float(target)
    except ValueError:
        return await update.message.reply_text("Please provide numeric K/D values.")
    diff = tgt - cur
    advice = []
    if diff <= 0:
        advice.append("You are already at or above your target K/D! Keep refining your skills.")
    else:
        advice = [
            "Focus on positioning: aim for head glitches and cover.",
            "Use time-to-kill drills: engage bots in training mode with short intervals.",
            "Review gameplay clips to identify mistakes.",
            "Play with a consistent loadout to build muscle memory."
        ]
    text = f"**Tips to go from {cur} to {tgt} K/D**\n" + "\n".join(advice)
    await update.message.reply_text(text)
