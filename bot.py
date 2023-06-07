import discord
from joblib import dump, load
from sklearn.naive_bayes import MultinomialNB
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import argparse
# ==================== load model ===========
MODEL_FILE = "nb_model.joblib"
VECTORIZER_FILE = "vect.joblib"

nb = load(MODEL_FILE)
vect = load(VECTORIZER_FILE)

def nb_spam_detect(nb,vect , msg: str)-> bool:
    # 
    x_to_predict = pd.Series(data=[msg])
    x_to_predict_dtm = vect.transform(x_to_predict)
    predicted = nb.predict(x_to_predict_dtm)
    # predicted has to 1
    assert len(predicted) == 1

    # if ham = 0, spam = 1 
    is_spam = predicted[0] == 1
    return is_spam

# ==========================================
def is_bad_msg(msg: str)->bool:

    is_spam = nb_spam_detect(nb = nb, vect = vect, msg = msg)
    return is_spam
# ======================================
# string utils
def user_id_to_mention_str(user_id: str)->str:
    return f"<@{user_id}>"
# ======================================
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    user_id = message.author.id
    mention_user_str = user_id_to_mention_str(user_id)
    if is_bad_msg(message.content):
        await message.channel.send(f"{mention_user_str} Your message is deleted because it is a spam, Bing Chilllling !!!!")
        await message.delete()
    else:
        await message.channel.send(f'{mention_user_str} Your message is good')


# ==================== CLI creation ==============
parser = argparse.ArgumentParser()
parser.add_argument("DISCORD_BOT_TOKEN", help="Your discord bot token" , type=str)
args = parser.parse_args()
# run the bot with the token 
print(args.DISCORD_BOT_TOKEN)
client.run(args.DISCORD_BOT_TOKEN)
# ============================================


