import discord
from models import User, engine, Base, Session

Base.metadata.create_all(engine)
Session = Session()

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        author = message.author
        user = User.query.filter_by(user=author).first()
        if user:
            user.user_lvl =+ 5
            if message.content.startswith('&&lvl'):
                await message.reply("Your level is: " + str(user.user_lvl))
        else:
            new_user = User(user=author, author_lvl=5)
            Session.add(new_user)
            Session.commit()

client = MyClient()
client.run('token goes here')
