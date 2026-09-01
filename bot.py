"""
Solana Discord Bot - Receives SOL payments
"""

import discord
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv
from solana.rpc.api import Client
from solana.rpc.types import TokenAccountOpts
from solders.pubkey import Pubkey
import asyncio
import json
from datetime import datetime

# Load environment variables
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
SOLANA_WALLET = os.getenv("SOLANA_WALLET_ADDRESS")
SOLANA_RPC = os.getenv("SOLANA_RPC_URL", "https://api.devnet.solana.com")
MIN_SOL = float(os.getenv("MIN_SOL_AMOUNT", "0.1"))
NOTIFICATION_CHANNEL = int(os.getenv("NOTIFICATION_CHANNEL_ID", "0"))

# Initialize Solana client
solana_client = Client(SOLANA_RPC)

# Initialize Discord bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Store last checked transaction signature
last_signature = None
transactions_log = "transactions.json"

def load_transactions():
    """Load transaction history from file"""
    if os.path.exists(transactions_log):
        with open(transactions_log, 'r') as f:
            return json.load(f)
    return {}

def save_transactions(data):
    """Save transaction history to file"""
    with open(transactions_log, 'w') as f:
        json.dump(data, f, indent=2)

@bot.event
async def on_ready():
    """Bot is ready"""
    print(f"✅ Bot prijungtas kaip {bot.user}")
    print(f"💰 Klausau Solana wallet: {SOLANA_WALLET}")
    check_solana_payments.start()

@bot.command(name="wallet")
async def get_wallet(ctx):
    """Get Solana wallet address to send SOL"""
    embed = discord.Embed(
        title="💰 Solana Wallet Adresas",
        description=f"Siųsk SOL pinigus čia:",
        color=discord.Color.green()
    )
    embed.add_field(
        name="📍 Adresas",
        value=f"`{SOLANA_WALLET}`",
        inline=False
    )
    embed.add_field(
        name="⚠️ Minimalus kiekis",
        value=f"{MIN_SOL} SOL",
        inline=False
    )
    embed.set_footer(text="Spustelėk norėdamas nukopijuoti adresą")
    await ctx.send(embed=embed)

@bot.command(name="balance")
async def check_balance(ctx):
    """Check wallet balance"""
    try:
        wallet_pubkey = Pubkey(SOLANA_WALLET)
        response = solana_client.get_balance(wallet_pubkey)
        balance_lamports = response.value
        balance_sol = balance_lamports / 1e9  # Convert lamports to SOL
        
        embed = discord.Embed(
            title="💰 Wallet Balansas",
            description=f"**{balance_sol:.4f} SOL**",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Klaida: {str(e)}")

@bot.command(name="transactions")
async def get_transactions(ctx):
    """Show recent transactions"""
    transactions = load_transactions()
    
    if not transactions:
        await ctx.send("📭 Dar nėra transakcijų")
        return
    
    embed = discord.Embed(
        title="📋 Transakcijų Istorija",
        color=discord.Color.purple()
    )
    
    # Show last 10 transactions
    for i, (tx_id, data) in enumerate(list(transactions.items())[-10:], 1):
        embed.add_field(
            name=f"#{i} - {data.get('timestamp', 'Unknown')}",
            value=f"💰 {data.get('amount', 0)} SOL\n🔗 {tx_id[:20]}...",
            inline=False
        )
    
    await ctx.send(embed=embed)

@tasks.loop(minutes=1)
async def check_solana_payments():
    """Check for incoming Solana payments every minute"""
    global last_signature
    
    try:
        wallet_pubkey = Pubkey(SOLANA_WALLET)
        
        # Get transaction signatures
        signatures = solana_client.get_signatures_for_address(
            wallet_pubkey,
            limit=10
        )
        
        if not signatures.value:
            return
        
        transactions = load_transactions()
        channel = bot.get_channel(NOTIFICATION_CHANNEL) if NOTIFICATION_CHANNEL else None
        
        for sig_info in signatures.value:
            sig = sig_info.signature
            
            # Skip if we already processed this
            if sig in transactions:
                continue
            
            try:
                # Get transaction details
                tx_data = solana_client.get_transaction(sig)
                
                if tx_data.value is None:
                    continue
                
                # Check if transaction was successful
                if tx_data.value.transaction.meta.err is not None:
                    continue
                
                # Get pre and post balances
                pre_balance = tx_data.value.transaction.meta.pre_balances
                post_balance = tx_data.value.transaction.meta.post_balances
                
                # Find the account index for our wallet
                account_keys = [str(key) for key in tx_data.value.transaction.message.account_keys]
                
                if str(wallet_pubkey) not in account_keys:
                    continue
                
                wallet_idx = account_keys.index(str(wallet_pubkey))
                
                # Calculate SOL received
                balance_change = (post_balance[wallet_idx] - pre_balance[wallet_idx]) / 1e9
                
                # Only log positive changes (received SOL)
                if balance_change > 0:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    # Save transaction
                    transactions[sig] = {
                        "amount": round(balance_change, 4),
                        "timestamp": timestamp,
                        "status": "success"
                    }
                    save_transactions(transactions)
                    
                    # Send notification to Discord
                    if channel:
                        embed = discord.Embed(
                            title="✅ Gauta SOL Transakcija!",
                            color=discord.Color.green()
                        )
                        embed.add_field(name="💰 Suma", value=f"{balance_change:.4f} SOL", inline=False)
                        embed.add_field(name="⏰ Laikas", value=timestamp, inline=False)
                        embed.add_field(name="🔗 TX ID", value=f"`{sig[:20]}...`", inline=False)
                        
                        await channel.send(embed=embed)
                    
                    print(f"✅ Gauta: {balance_change} SOL - {sig}")
            
            except Exception as e:
                print(f"⚠️ Klaida apdorojant transakcija {sig}: {str(e)}")
                continue
    
    except Exception as e:
        print(f"❌ Klaida tikrinant pagrindinį wallet: {str(e)}")

@bot.event
async def on_command_error(ctx, error):
    """Handle command errors"""
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Klaida: Trūksta parametro")
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send(f"❌ Komanda nerasta. Naudok `!help`")
    else:
        await ctx.send(f"❌ Klaida: {str(error)}")

# Run bot
if __name__ == "__main__":
    if not DISCORD_TOKEN:
        print("❌ KLAIDA: Nėra DISCORD_TOKEN .env faile!")
        exit(1)
    if not SOLANA_WALLET:
        print("❌ KLAIDA: Nėra SOLANA_WALLET_ADDRESS .env faile!")
        exit(1)
    
    print("🚀 Discord Solana Bot pradedamas...")
    bot.run(DISCORD_TOKEN)
