from uuid import RFC_4122
import discord
from models import User, engine, Base, Session
import random as rdm

Base.metadata.create_all(engine)
session = Session(bind=engine)

class Leaderboard:
    def __init__(self):
        self.leaderboard = []

    def sort(self, list):
        return list['Lvl']

    def run(self):
        for user in session.query(User).all():
            self.leaderboard.append({"Lvl" : user.user_lvl, "User" : user.user})
        self.leaderboard.sort(reverse=True, key=self.sort)

    def get_data(self):
        self.run()
        return self.leaderboard


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        author = message.author.name + message.author.discriminator
        user = session.query(User).filter(User.user==author).first()
        if user:
            if message.author.name != 'KoalaBot':
                user.user_lvl = user.user_lvl + 5
                if message.content.startswith('&&lvl'):
                    await message.reply("Your level is: " + str(user.user_lvl), mention_author=False)
                elif message.content.startswith('&&insult'):
                    msg = message.content
                    msg = msg.split()
                    insults = ["You are older that the Queen", "You sure that you are old enough to use Discord?", "You have the thought process of a child", "Your like Pixel, but worse", "You are as evil as Gareth, but even he has morals or something", "You don't deserve to be insulted, you are actually a decent person"]
                    value = rdm.randint(0, len(insults) - 1)
                    await message.reply(insults[value] + ", " + msg[1] + " :p", mention_author=False)
                elif message.content.startswith('&&leaderboard'):
                    data = Leaderboard()
                    data = data.get_data()
                    R1 = data[0]
                    R2 = data[1]
                    R3 = data[2]
                    LB_str ="#1: " + R1['User'] + " with " + str(R2['Lvl']) + " levels" + "\n#2: " + R2['User'] + " with " + str(R2['Lvl']) + " levels" + "\n#3: " + R3['User'] + " with " + str(R3['Lvl']) + " levels"
                    await message.reply(LB_str, mention_author=False)
                elif message.content.startswith('&&help'):
                    await message.reply("""
[] = required argument
() = optional argument

Commands:
    - &&insult [@user] - Returns a random insult directed at the mention user.
    - &&help - Returns this help text.
    - &&leaderboard - Returns the top 3 users.
    - &&lvl - Returns a user's level.
    - &&github - Returns link to the GitHub repository.
                    """, mention_author=False)
                elif message.content.startswith('&&pride'):
                    await message.reply(":rainbow_flag: love is love, everyone matters, no matter who they love or are. :rainbow_flag:", mention_author=False)
                elif message.content.startswith('&&github'):
                    await message.reply("https://github.com/KoalasAreDeveloping/KoalaBot", mention_author=False)
                elif message.content.find("69") != -1:
                    await message.reply("69? Nice!", mention_author=False)
        else:
            new_user = User(user=author, user_lvl=5)
            session.add(new_user)
            session.commit()

client = MyClient()
client.run('token goes here')
