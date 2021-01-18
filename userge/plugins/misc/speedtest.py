# Copyright (C) 2020 by UsergeTeam@Github, < https://github.com/UsergeTeam >.
#
# This file is part of < https://github.com/UsergeTeam/Userge > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/uaudith/Userge/blob/master/LICENSE >
#
# All rights reserved.

import os
import wget
import speedtest
from userge import userge, Message
from userge.utils import humanbytes

CHANNEL = userge.getCLogger(__name__)


@userge.on_cmd("speedtest", about={'header': "test your server speed"})
async def speedtst(message: Message):
    await message.edit("`Memulai Uji Coba Kecepatan Speed Server , Sayang Kuu . . .`")
    try:
        test = speedtest.Speedtest()
        test.get_best_server()
        await message.try_to_edit("`Mencari Server Terbaik Untuk Mu, Sayang Kuuu . . .`")
        test.download()
        await message.try_to_edit("`Mengecek Upload Speed , Demi Kamu Sayang Kuu . . .`")
        test.upload()
        test.results.share()
        result = test.results.dict()
    except Exception as e:
        await message.err(text=e)
        return
    path = wget.download(result['share'])
    output = f"""**--Started at {result['timestamp']}--

Client:

ISP: `{result['client']['isp']}`
Country: `{result['client']['country']}`

Server:

Name: `{result['server']['name']}`
Lokasi: `{result['server']['country']}, {result['server']['cc']}`
ISP: `{result['server']['sponsor']}`
Latensi: `{result['server']['latency']}`

Ping: `{result['ping']}`
Sent: `{humanbytes(result['bytes_sent'])}`
Received: `{humanbytes(result['bytes_received'])}`
Download: `{humanbytes(result['download'] / 8)}/s`
Upload: `{humanbytes(result['upload'] / 8)}/s`**"""
    msg = await message.client.send_photo(chat_id=message.chat.id,
                                          photo=path,
                                          caption=output)
    await CHANNEL.fwd_msg(msg)
    os.remove(path)
    await message.delete()
