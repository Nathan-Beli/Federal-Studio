importimport os
import discord
from discord import app_commands
from discord.ext import commands

# 1. Configuration des permissions (Intents)
intents = discord.Intents.default()
intents.message_content = True 

# 2. Définition de la classe du Bot
class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # Synchronise les commandes slash avec Discord au démarrage
        await self.tree.sync()
        print(f"Bot connecté et commandes synchronisées : {self.user}")

# Instance du bot
bot = MyBot()

# 3. Commande /salon
@bot.tree.command(name="salon", description="Crée un salon avec un nom et un emoji")
@app_commands.describe(
    nom="Le nom du salon (ex: general)",
    emoji="L'emoji du salon (ex: 💬)",
    categorie="La catégorie où placer le salon"
)
async def salon(interaction: discord.Interaction, nom: str, emoji: str, categorie: discord.CategoryChannel):
    # Formater le nom du salon
    salon_nom = f"{emoji}-{nom.lower().replace(' ', '-')}"
    
    # Créer le salon
    nouveau_salon = await interaction.guild.create_text_channel(
        name=salon_nom,
        category=categorie
    )
    
    # Réponse confirmant la création
    await interaction.response.send_message(f"Le salon {nouveau_salon.mention} a été créé avec succès !", ephemeral=True)

# 4. Lancement sécurisé
token = os.environ.get("DISCORD_TOKEN")
if token:
    bot.run(token)
else:
    print("Erreur : La variable d'environnement DISCORD_TOKEN est introuvable sur Render.")