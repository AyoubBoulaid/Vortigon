import os, json, logging
from dotenv import load_dotenv
from telegram import Update, BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ----------------------------------
# Load .env and show debug info
# ----------------------------------
load_dotenv()
print("DEBUG cwd:", os.getcwd())
print("DEBUG files:", os.listdir())
print("DEBUG OPENAI_API_KEY =", os.getenv("OPENAI_API_KEY"))
print("DEBUG SERPAPI_KEY   =", os.getenv("SERPAPI_KEY"))

# ----------------------------------
# Import command modules
# ----------------------------------
from commands.loadout import loadout
from commands.sensitivity import sensitivity
from commands.strategy import strategy
from commands.drills import drills
from commands.tips import tips
from commands.ai_loadout import ai_loadout

# ----------------------------------
# Logging setup
# ----------------------------------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ----------------------------------
# Handlers
# ----------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to CODM Assistant Bot! Use /help to see available commands."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cmds = [
        ("loadout", "Suggest a meta loadout: /loadout <weapon> <mode>"),
        ("sensitivity", "Recommend sensitivity: /sensitivity <device>"),
        ("strategy", "Tactical advice: /strategy <mode> <map>"),
        ("drills", "Training drills: /drills <role> <goal>"),
        ("tips", "Improvement tips: /tips <current_kd> <target_kd>"),
        ("ai_loadout", "AI-powered meta loadout")
    ]
    text = "Available commands:\n" + "\n".join(f"/{c} – {d}" for c, d in cmds)
    await update.message.reply_text(text)

# Set command list after bot starts
async def _set_commands(app):
    await app.bot.set_my_commands([
        BotCommand("ai_loadout", "AI-powered meta loadout"),
        BotCommand("start", "Start the bot"),
        BotCommand("help", "Show help"),
        BotCommand("loadout", "Meta loadout suggestions"),
        BotCommand("sensitivity", "Sensitivity settings"),
        BotCommand("strategy", "Tactical advice"),
        BotCommand("drills", "Training routines"),
        BotCommand("tips", "Improvement tips"),
    ])

# ----------------------------------
# Main entry
# ----------------------------------
if __name__ == "__main__":
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        raise ValueError("TELEGRAM_TOKEN not found in environment variables")

    # Build Application
    app = (
        ApplicationBuilder()
        .token(token)
        .post_init(_set_commands)  # <-- runs once, awaits properly
        .build()
    )

    # Register command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("loadout", loadout))
    app.add_handler(CommandHandler("sensitivity", sensitivity))
    app.add_handler(CommandHandler("strategy", strategy))
    app.add_handler(CommandHandler("drills", drills))
    app.add_handler(CommandHandler("tips", tips))
    app.add_handler(CommandHandler("ai_loadout", ai_loadout))

    logger.info("Starting CODM Bot…")
    app.run_polling()
