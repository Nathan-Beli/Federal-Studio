import os
import discord
from discord import app_commands
from discord.ext import commands
from flask import Flask
from threading import Thread

# --- 1. PARTIE SITE WEB (Flask) ---
app = Flask('')

@app.route('/')
def home():
    return "Le serveur Federal Studio est en ligne !"

def run_web_server():
    # Utilise le port fourni par Render ou 8080 par défaut
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- 2. PARTIE BOT DISCORD ---
intents = discord.Intents.default()
intents.message_content = True 

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await self.tree.sync()
        print(f"Bot connecté et commandes synchronisées : {self.user}")

bot = MyBot()

@bot.tree.command(name="salon", description="Crée un salon avec un nom et un emoji")
@app_commands.describe(
    nom="Le nom du salon",
    emoji="L'emoji du salon",
    categorie="La catégorie où placer le salon"
)
async def salon(interaction: discord.Interaction, nom: str, emoji: str, categorie: discord.CategoryChannel):
    salon_nom = f"{emoji}-{nom.lower().replace(' ', '-')}"
    nouveau_salon = await interaction.guild.create_text_channel(name=salon_nom, category=categorie)
    await interaction.response.send_message(f"Le salon {nouveau_salon.mention} a été créé !", ephemeral=True)

# --- 3. LANCEMENT SIMULTANÉ ---
if __name__ == "__main__":
    # Lancement du serveur web dans un fil séparé
    web_thread = Thread(target=run_web_server)
    web_thread.start()
    
    # Lancement du bot Discord
    token = os.environ.get("DISCORD_TOKEN")
    if token:
        bot.run(token)
    else:
        print("Erreur : DISCORD_TOKEN manquant.")