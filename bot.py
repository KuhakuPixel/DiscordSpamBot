import discord
from joblib import dump, load
from sklearn.naive_bayes import MultinomialNB
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import argparse
from model import get_model, ClassifierModelType, model_predict_is_spam

# ==================== load vectorizer ===========
VECTORIZER_FILE = "vect.joblib"
vect = load(VECTORIZER_FILE)
print(type(vect))


def is_bad_msg(model, msg: str) -> bool:
    is_spam = model_predict_is_spam(model=model, vect=vect, msg=msg)
    return is_spam


# ======================================
# string utils
def user_id_to_mention_str(user_id: str) -> str:
    return f"<@{user_id}>"


# ======================================
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


# will be loaded at start time
used_model = None


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    user_id = message.author.id
    mention_user_str = user_id_to_mention_str(user_id)
    if is_bad_msg(model=used_model, msg=message.content):
        await message.channel.send(
            f"{mention_user_str} Your message is deleted because it is a spam, Bing Chilllling !!!!"
        )
        await message.delete()
    else:
        await message.channel.send(f"{mention_user_str} Your message is good")


# ==================== CLI creation ==============
parser = argparse.ArgumentParser()
parser.add_argument("DISCORD_BOT_TOKEN", help="Your discord bot token", type=str)
parser.add_argument(
    "--model",
    help="Chosen Model",
    type=ClassifierModelType,
    choices=list(ClassifierModelType),
    default=str(ClassifierModelType.naiveBayes),
)
args = parser.parse_args()
# set model to use
print(f"model used for spam detection: {str(args.model)}") 
used_model = get_model(modelType = args.model)

# run the bot with the token
print(args.DISCORD_BOT_TOKEN)
client.run(args.DISCORD_BOT_TOKEN)
# ============================================
