# commands/ai_loadout.py
import os, traceback, requests, openai
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ContextTypes
from utils.parser import parse_args

# ── keys ─────────────────────────────────────────────────────────────
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
SERPAPI_KEY    = os.getenv("SERPAPI_KEY")

# ── helper: pull meta snippets via SerpApi ───────────────────────────
def search_meta(weapon: str, mode: str) -> str:
    if not SERPAPI_KEY:
        return ""
    try:
        params = {
            "engine": "google",
            "q": f"Call of Duty Mobile {weapon} {mode} meta loadout 2025",
            "api_key": SERPAPI_KEY,
            "num": 5,
        }
        r = requests.get("https://serpapi.com/search", params=params, timeout=10)
        r.raise_for_status()
        bullets = [
            f"- {res['snippet']}"
            for res in r.json().get("organic_results", [])[:5]
            if res.get("snippet")
        ]
        return "\n".join(bullets)
    except Exception as e:
        print("DEBUG SerpApi error:", e)
        return ""

# ── main handler ────────────────────────────────────────────────────
async def ai_loadout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        args = parse_args(context.args, expected=2)
        if not args:
            return await update.message.reply_text("Usage: /ai_loadout <weapon> <mode>")

        weapon, mode = args
        print(f"DEBUG ai_loadout: weapon={weapon}, mode={mode}")

        snippets = search_meta(weapon, mode)
        print("DEBUG snippets length:", len(snippets))

        prompt = f"""
You are an expert Call of Duty Mobile strategist. Using the following web snippets:
{snippets or '[no snippets found]'}

Provide an up-to-date meta loadout for '{weapon}' in '{mode}'.
List attachments (muzzle, barrel, optic, underbarrel, rear grip) and optimal perks.
"""

        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful CODM AI assistant."},
                {"role": "user",   "content": prompt},
            ],
            temperature=0.2,
            max_tokens=300,
        )

        answer = response.choices[0].message.content.strip()
        await update.message.reply_text(answer)

    except Exception as e:
        traceback.print_exc()
        await update.message.reply_text(f"❌ Error: {e}")
