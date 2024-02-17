from config import app

from satori import Event
from satori.client import Account
import plugins


@app.register
async def listen(account: Account, event: Event):
    print(account, event)


#
#     if event.user.id == "1764203060" and str(event.message.content[0]) == "test":
#         await my_job()
#         await account.session.send_message(
#             event.channel.id,
#             "Hep!",
#         )


# @scheduler.scheduled_job('interval', minutes=1)
# async def my_job():
#     print("run my_job")
#     account = app.get_account("chronocat/{}".format(BOTACCOUNT))
#     await account.session.send_message(channel="897380826", message="Bek")


app.run()
