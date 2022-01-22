import discord
from models import User, engine, Base, Session

Base.metadata.create_all(engine)
session = Session(bind=engine)

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        author = message.author.name + message.author.discriminator
        user = session.query(User).filter(User.user==author).first()
        if user:
            user.user_lvl = user.user_lvl + 5
            if message.content.startswith('&&lvl'):
                await message.reply("Your level is: " + str(user.user_lvl), mention_author=False)
        else:
            new_user = User(user=author, user_lvl=5)
            session.add(new_user)
            session.commit()

client = MyClient()
client.run('token goes here')
