import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from state_store import StateStore
from markdown_writer import MarkdownWriter

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

# ─── Intents ─────────────────────────────────────────────
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True              # allow reaction events
# ─────────────────────────────────────────────────────────

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅  Logged in as {bot.user} (ID: {bot.user.id})")

# ─── Keep your existing ping for testing ─────────────────
@bot.command()
async def ping(ctx):
    await ctx.send("Pong! 🏓")
# ─────────────────────────────────────────────────────────

# ─── New: listen for 📜 reactions ────────────────────────

# initialize once at module level
state = StateStore("state.json")
writer = MarkdownWriter("reports/")

@bot.event
async def on_raw_reaction_add(payload):
    # 1) Only react to 📜
    if payload.emoji.name != "📜":
        return

    # 2) Restrict to your target channel
    if payload.channel_id != CHANNEL_ID:
        return

    # 3) Fetch channel (cached or via API) and message
    channel = bot.get_channel(payload.channel_id) or await bot.fetch_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)

    # 4) Skip if already processed
    if state.is_processed(message.id):
        return

    # 5) Build Markdown file
    md_path = writer.build(message)
    print(f"→ Wrote report to {md_path}")

    # 6) Mark as processed and save state
    state.add(message.id)
    state.save()

    # 7) Acknowledge in Discord
    await channel.send(
        f"⚔️  Captured report from **{message.author.display_name}**!\n"
        f"Saved to `{md_path}`"
    )
# ─────────────────────────────────────────────────────────

bot.run(TOKEN)
