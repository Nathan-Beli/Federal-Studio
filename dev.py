import os
import discord
from discord import app_commands
from discord.ext import commands

# 1. Configuration des Intents
intents = discord.Intents.default()
intents.message_content = True 

# 2. Définition de la classe du bot
class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # Synchronise les commandes avec Discord
        await self.tree.sync()
        print(f"Commandes synchronisées pour {self.user}")

bot = MyBot()

# 3. Commande de création de salon
@bot.tree.command(name="salon", description="Crée un salon avec un nom et un emoji")
@app_commands.describe(
    nom="Le nom du salon (ex: general)",
    emoji="L'emoji du salon (ex: 💬)",
    categorie="La catégorie où placer le salon"
)
async def salon(interaction: discord.Interaction, nom: str, emoji: str, categorie: discord.CategoryChannel):
    # Formater le nom
    salon_nom = f"{emoji}-{nom.lower().replace(' ', '-')}"
    
    # Créer le salon
    nouveau_salon = await interaction.guild.create_text_channel(
        name=salon_nom,
        category=categorie
    )
    
    await interaction.response.send_message(f"Le salon {nouveau_salon.mention} a été créé avec succès !", ephemeral=True)

# 4. Lancement du bot
# On utilise directement la variable d'environnement ici
token = os.environ.get("DISCORD_TOKEN")
if token:
    bot.run(token)
else:
    print("Erreur : La variable d'environnement DISCORD_TOKEN est introuvable.")