import discord
from discord import app_commands
from discord.ext import tasks, commands
import speedtest
import asyncio
import datetime
import json
import os
from dotenv import load_dotenv # <--- ΝΕΑ ΒΙΒΛΙΟΘΗΚΗ

# Φόρτωση του .env αρχείου
load_config = load_dotenv()

# Τραβάμε το Token από το .env (ΑΣΦΑΛΕΙΑ)
TOKEN = os.getenv('DISCORD_TOKEN')

# Όνομα αρχείου ρυθμίσεων
CONFIG_FILE = "config.json"

# Bot Setup
intents = discord.Intents.default()
client = commands.Bot(command_prefix="!", intents=intents)

# Φόρτωση ρυθμίσεων
def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}

def save_config(data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f)

# Global Config Variable
config = load_config()

@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    try:
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} commands.")
    except Exception as e:
        print(f"Error syncing commands: {e}")

    # Έλεγχος αν υπάρχει ήδη ρύθμιση για να ξεκινήσει το loop
    if "channel_id" in config and "interval" in config:
        if not measure_speed.is_running():
            measure_speed.change_interval(minutes=config["interval"])
            measure_speed.start()
            print(f"Resumed task: Channel {config['channel_id']} every {config['interval']} minutes.")

# --- SLASH COMMAND: SETUP ---
@client.tree.command(name="setup", description="Configure the Speed Monitor channel and interval.")
@app_commands.describe(channel="Select the channel for reports", interval="Minutes between tests (e.g. 60 for 1 hour)")
async def setup(interaction: discord.Interaction, channel: discord.TextChannel, interval: int):
    # Έλεγχος δικαιωμάτων (μόνο Admin)
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ You need Administrator permissions to use this.", ephemeral=True)
        return

    if interval < 5:
        await interaction.response.send_message("⚠️ Interval must be at least 5 minutes to avoid lag.", ephemeral=True)
        return

    # Αποθήκευση Ρυθμίσεων
    config["channel_id"] = channel.id
    config["interval"] = interval
    save_config(config)

    # Επανεκκίνηση του Loop με τον νέο χρόνο
    measure_speed.change_interval(minutes=interval)
    if not measure_speed.is_running():
        measure_speed.start()
    else:
        measure_speed.restart()

    await interaction.response.send_message(f"✅ **Setup Complete!**\n📡 Channel: {channel.mention}\n⏱️ Interval: Every **{interval}** minutes.\n🚀 First test starting soon...", ephemeral=True)

# --- SLASH COMMAND: FORCE TEST ---
@client.tree.command(name="testnow", description="Force a speedtest immediately.")
async def testnow(interaction: discord.Interaction):
    await interaction.response.send_message("⏳ Running manual speedtest... This takes about 30s.", ephemeral=True)
    
    # Τρέχουμε τη λογική του speedtest
    await run_speedtest_logic(interaction.channel)

# --- THE LOOP ---
@tasks.loop(minutes=60) # Default, αλλάζει από το setup
async def measure_speed():
    if "channel_id" not in config:
        return # Δεν έχει ρυθμιστεί ακόμα

    channel_id = config["channel_id"]
    channel = client.get_channel(channel_id)
    
    if channel:
        await run_speedtest_logic(channel)
    else:
        print("Channel not found/deleted.")

async def run_speedtest_logic(channel):
    print("Running speedtest...")
    try:
        # Status update
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Speedtest..."))

        # Εκτέλεση Speedtest σε thread (για να μην κολλήσει το bot)
        loop = asyncio.get_event_loop()
        st = await loop.run_in_executor(None, speedtest.Speedtest)
        await loop.run_in_executor(None, st.get_best_server)
        
        download_speed = await loop.run_in_executor(None, st.download)
        upload_speed = await loop.run_in_executor(None, st.upload)
        ping = st.results.ping

        down_mbps = round(download_speed / 10**6, 2)
        up_mbps = round(upload_speed / 10**6, 2)

        # Χρώμα ανάλογα την ταχύτητα (παράδειγμα: κάτω από 50Mbps κόκκινο)
        embed_color = 0x00ff41 if down_mbps > 50 else 0xff0000

        embed = discord.Embed(
            title="📡 Network Speed Report",
            description=f"Automated Monitor running on **Raspberry Pi**",
            color=embed_color,
            timestamp=datetime.datetime.now()
        )
        
        embed.add_field(name="⬇️ Download", value=f"**{down_mbps}** Mbps", inline=True)
        embed.add_field(name="⬆️ Upload", value=f"**{up_mbps}** Mbps", inline=True)
        embed.add_field(name="📶 Ping", value=f"**{ping}** ms", inline=True)
        embed.set_footer(text="Net-Speed-Monitor | Universal Bot")

        await channel.send(embed=embed)
        
        # Επαναφορά Status
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"Traffic | Every {config.get('interval', '?')}m"))

    except Exception as e:
        print(f"Error: {e}")
        await channel.send(f"⚠️ **Speedtest Error:** {e}")

@measure_speed.before_loop
async def before_measure_speed():
    await client.wait_until_ready()

client.run(TOKEN)