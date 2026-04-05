# ===================== IMPORTS =====================
import discord
from discord.ext import commands
from datetime import datetime

# ===================== CONFIG =====================
TOKEN = "MTQ4NzQwNTYyMzYwMjg0Mzc2OA.G5QncR.4KobiRZayA8cB3aqwdUh5K2irHhhF0za-uHb_8"

PREFIX = "gmrp!"

CONTROL_SERVER_ID = 1251579223962026044
LOG_CHANNEL_ID = 1467241410615840842

TIER1_ROLE_ID = 1443711597477367910

# ===================== INTENTS =====================
intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# ===================== DATA =====================
server_bans = {}

# ===================== HELPERS =====================
def has_tier1(member: discord.Member):
    return any(role.id == TIER1_ROLE_ID for role in member.roles)

# ===================== READY =====================
@bot.event
async def on_ready():
    print(f"🛡️ Server Ban Bot logged in as {bot.user}")

# ===================== SERVER BAN =====================
@bot.command()
async def sban(ctx, user_id: int, *, reason: str):
    if ctx.guild.id != CONTROL_SERVER_ID:
        return

    if not has_tier1(ctx.author):
        return await ctx.send("❌ You need the **Tier 1** role to use this command.")

    server_bans[user_id] = {
        "by": ctx.author.id,
        "reason": reason,
        "time": datetime.utcnow()
    }

    log_channel = bot.get_channel(LOG_CHANNEL_ID)

    embed = discord.Embed(
        title="🔨 Server Ban Issued",
        color=0xff0000,
        timestamp=datetime.utcnow()
    )
    embed.add_field(name="User ID", value=str(user_id), inline=False)
    embed.add_field(
        name="Banned By",
        value=f"{ctx.author} ({ctx.author.id})",
        inline=False
    )
    embed.add_field(name="Reason", value=reason, inline=False)

    if log_channel:
        await log_channel.send(embed=embed)

    await ctx.send(f"✅ User `{user_id}` has been **server banned**.")

# ===================== SERVER UNBAN =====================
@bot.command()
async def sunban(ctx, user_id: int):
    if ctx.guild.id != CONTROL_SERVER_ID:
        return

    if not has_tier1(ctx.author):
        return await ctx.send("❌ You need the **Tier 1** role to use this command.")

    if user_id not in server_bans:
        return await ctx.send("ℹ️ That user is not server banned.")

    server_bans.pop(user_id)

    log_channel = bot.get_channel(LOG_CHANNEL_ID)

    embed = discord.Embed(
        title="♻️ Server Ban Removed",
        color=0x00ff00,
        timestamp=datetime.utcnow()
    )
    embed.add_field(name="User ID", value=str(user_id), inline=False)
    embed.add_field(
        name="Unbanned By",
        value=f"{ctx.author} ({ctx.author.id})",
        inline=False
    )

    if log_channel:
        await log_channel.send(embed=embed)

    await ctx.send(f"✅ User `{user_id}` has been **server unbanned**.")

# ===================== BAN LOOKUP =====================
@bot.command()
async def sbanlookup(ctx, user_id: int):
    ban = server_bans.get(user_id)

    if not ban:
        return await ctx.send("✅ User is **not** server banned.")

    embed = discord.Embed(
        title="🔍 Server Ban Lookup",
        color=0xffaa00,
        timestamp=ban["time"]
    )
    embed.add_field(name="User ID", value=str(user_id), inline=False)
    embed.add_field(name="Banned By", value=f"<@{ban['by']}>", inline=False)
    embed.add_field(name="Reason", value=ban["reason"], inline=False)

    await ctx.send(embed=embed)

# ===================== COMMAND LIST =====================
@bot.command()
async def cmd(ctx):
    await ctx.send("""
🛡️ **Server Ban Bot Commands**

gmrp sban <user_id> <reason>
→ Server ban a user (Tier 1 only)

gmrp sunban <user_id>
→ Remove a server ban

gmrp sbanlookup <user_id>
→ Check server ban status

gmrp cmd
→ Show this menu
""")

# ===================== RUN =====================
bot.run(TOKEN)

