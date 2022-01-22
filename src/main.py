from uuid import RFC_4122
import discord
from models import User, engine, Base, Session
import random as rdm

Base.metadata.create_all(engine)
session = Session(bind=engine)
embed_col = 0x7289DA
class Leaderboard:
    def __init__(self):
        self.leaderboard = []

    def sort(self, list):
        return list['Lvl']

    def run(self):
        for user in session.query(User).all():
            self.leaderboard.append({"Lvl" : user.user_lvl, "User" : user.user_name})
        self.leaderboard.sort(reverse=True, key=self.sort)

    def get_data(self):
        self.run()
        return self.leaderboard


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        author_id = message.author.id
        user = session.query(User).filter(User.user_id==author_id).first()
        if user:
            if message.author.name != 'KoalaBot':
                user.user_lvl = user.user_lvl + 5
                if message.content.startswith('&&lvl'):
                    if message.content.find("<@!") == -1:
                        embedVar = discord.Embed(title=message.author.name + "'s Level", description=str(user.user_lvl), color=embed_col)
                    else:
                        msg = message.content
                        msg = msg.split()
                        msg = msg[1]
                        mention_id = msg[3:-1]
                        user_temp = session.query(User).filter(User.user_id==mention_id).first()
                        embedVar = discord.Embed(title=user_temp.user_name + "'s Level", description=str(user_temp.user_lvl), color=embed_col)
                    await message.reply(embed=embedVar, mention_author=False)

                elif message.content.startswith('&&insult'):
                    msg = message.content
                    msg = msg.split()
                    insults = ["You are older that the Queen", "You sure that you are old enough to use Discord?", "You have the thought process of a child", "Your like Pixel, but worse", "You are as evil as Gareth, but even he has morals or something", "You don't deserve to be insulted, you are actually a decent person"]
                    value = rdm.randint(0, len(insults) - 1)
                    embedVar = discord.Embed(title="Insulting " + msg[1] + " :p", description=insults[value] + ".", color=embed_col)
                    await message.reply(embed=embedVar, mention_author=False)

                elif message.content.startswith('&&leaderboard'):
                    data = Leaderboard()
                    data = data.get_data()
                    R1 = data[0]
                    R2 = data[1]
                    R3 = data[2]
                    embedVar = discord.Embed(title="Rankings", description="", color=embed_col)
                    embedVar.add_field(name="First Place", value=R1['User'] + " with " + str(R2['Lvl']) + " levels", inline=False)
                    embedVar.add_field(name="second Place", value=R2['User'] + " with " + str(R2['Lvl']) + " levels", inline=False)
                    embedVar.add_field(name="Third Place", value=R3['User'] + " with " + str(R3['Lvl']) + " levels", inline=False)
                    await message.reply(embed=embedVar, mention_author=False)

                elif message.content.startswith('&&help'):
                    embedVar = discord.Embed(title="Help", description="", color=embed_col)
                    embedVar.add_field(name="Prerequisites", value="[] = required argument \n() = optional argument", inline=False)
                    embedVar.add_field(name="Commands", value="- &&insult [@user] - Returns a random insult directed at the mention user.\n- &&help - Returns this help text.\n- &&leaderboard - Returns the top 3 users.\n- &&lvl (@user) - Returns a user's level.\n- &&github - Returns link to the GitHub repository.", inline=False)
                    await message.reply(embed=embedVar, mention_author=False)

                elif message.content.startswith('&&pride'):
                    embedVar = discord.Embed(title="Pride", description=":rainbow_flag: love is love, everyone matters, no matter who they love or are. :rainbow_flag:", color=embed_col)
                    await message.reply(embed=embedVar, mention_author=False)

                elif message.content.startswith('&&github'):
                    embedVar = discord.Embed(title="GitHub", description="https://github.com/KoalasAreDeveloping/KoalaBot", color=embed_col)                
                    await message.reply(embed=embedVar, mention_author=False)

                elif message.content.find("69") != -1:
                    embedVar = discord.Embed(title="69?", description="Nice!", color=embed_col)
                    await message.reply(embed=embedVar, mention_author=False)
        else:
            new_user = User(user_name=message.author.name, user_lvl=5, user_id=message.author.id)
            session.add(new_user)
            session.commit()

client = MyClient()
client.run('token goes here')
