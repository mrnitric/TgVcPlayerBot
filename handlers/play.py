import os
from os import path
from pyrogram import Client, filters
from pyrogram.types import Message, Voice, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserAlreadyParticipant
from callsmusic import callsmusic, queues
from callsmusic.callsmusic import client as USER
from helpers.admins import get_administrators
import requests
import aiohttp
import youtube_dl
from youtube_search import YoutubeSearch
import converter
from downloaders import youtube
from config import DURATION_LIMIT
from helpers.filters import command
from helpers.decorators import errors
from helpers.errors import DurationLimitError
from helpers.gets import get_url, get_file_name
import aiofiles
import ffmpeg
from PIL import Image, ImageFont, ImageDraw


def transcode(filename):
    ffmpeg.input(filename).output("input.raw", format='s16le', acodec='pcm_s16le', ac=2, ar='48k').overwrite_output().run() 
    os.remove(filename)

# Convert seconds to mm:ss
def convert_seconds(seconds):
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d" % (minutes, seconds)


# Convert hh:mm:ss to seconds
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))


# Change image size
def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage

async def generate_cover(requested_by, title, views, duration, thumbnail):
    async with aiohttp.ClientSession() as session:
        async with session.get(thumbnail) as resp:
            if resp.status == 200:
                f = await aiofiles.open("background.png", mode="wb")
                await f.write(await resp.read())
                await f.close()

    image1 = Image.open("./background.png")
    image2 = Image.open("etc/foreground.png")
    image3 = changeImageSize(1280, 720, image1)
    image4 = changeImageSize(1280, 720, image2)
    image5 = image3.convert("RGBA")
    image6 = image4.convert("RGBA")
    Image.alpha_composite(image5, image6).save("temp.png")
    img = Image.open("temp.png")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("etc/font.otf", 32)
    draw.text((190, 550), f"Title: {title}", (255, 255, 255), font=font)
    draw.text(
        (190, 590), f"Duration: {duration}", (255, 255, 255), font=font
    )
    draw.text((190, 630), f"Views: {views}", (255, 255, 255), font=font)
    draw.text((190, 670),
        f"Added By: {requested_by}",
        (255, 255, 255),
        font=font,
    )
    img.save("final.png")
    os.remove("temp.png")
    os.remove("background.png")




@Client.on_message(command("play") 
                   & filters.group
                   & ~filters.edited 
                   & ~filters.forwarded
                   & ~filters.via_bot)
async def play(_, message: Message):

    lel = await message.reply("𝙋𝙧𝙤𝙘𝙚𝙨𝙨𝙞𝙣𝙜 𝙔𝙤𝙪𝙧 𝙎𝙤𝙣𝙜...**")
    
    administrators = await get_administrators(message.chat)
    chid = message.chat.id

    try:
        user = await USER.get_me()
    except:
        user.first_name = "Sanki"
    usar = user
    wew = usar.id
    try:
        await _.get_chat_member(chid, wew)
    except:
        for administrator in administrators:
            if administrator == message.from_user.id:
                try:
                    invitelink = await _.export_chat_invite_link(chid)
                except:
                    await lel.edit(
                        "<b>𝘼𝙙𝙙 𝙈𝙚 𝘼𝙨 𝘼𝙙𝙢𝙞𝙣 𝙁𝙞𝙧𝙨𝙩 𝙎𝙩𝙪𝙥𝙞𝙙.</b>")
                    return

                try:
                    await USER.join_chat(invitelink)
                    await USER.send_message(
                        message.chat.id, "**𝙃𝙚𝙮 𝙈𝙮 𝘼𝙨𝙨𝙞𝙨𝙩𝙖𝙣𝙩 𝙄𝙨 𝙅𝙤𝙞𝙣𝙚𝙙. 𝙃𝙪𝙧𝙧𝙧𝙚𝙮 🐬🤞**")

                except UserAlreadyParticipant:
                    pass
                except Exception:
                    await lel.edit(
                        f"<b>🛑 𝙁𝙡𝙤𝙤𝙙 𝙀𝙧𝙧𝙤𝙧 🛑</b> \n\𝙃𝙚𝙮 {user.first_name}, 𝘼𝙨𝙨𝙞𝙨𝙩𝙖𝙣𝙩 𝘾𝙤𝙪𝙡𝙙𝙣'𝙩 𝙅𝙤𝙞𝙣 𝙔𝙤𝙪𝙧 𝙂𝙧𝙤𝙪𝙥. 𝙈𝙖𝙮 𝘽𝙚 𝙄𝙩𝙨 𝘽𝙖𝙣𝙣𝙚𝙙 𝙊𝙧 𝘼𝙣𝙮 𝙊𝙩𝙝𝙚𝙧 𝙄𝙨𝙨𝙪𝙚")
    try:
        await USER.get_chat(chid)
    except:
        await lel.edit(
            f"<i>𝙃𝙚𝙮 {user.first_name}, 𝘼𝙨𝙨𝙞𝙨𝙩𝙖𝙣𝙩 𝙄𝙨 𝙉𝙤𝙩 𝙃𝙚𝙧𝙚 :( 𝙎𝙚𝙣𝙙 /play 𝘾𝙤𝙢𝙢𝙖𝙣𝙙 𝙁𝙞𝙧𝙨𝙩 𝙏𝙤 𝘼𝙙𝙙 𝘼𝙨𝙨𝙞𝙨𝙩𝙖𝙣𝙩.</i>")
        return
    
    audio = (message.reply_to_message.audio or message.reply_to_message.voice) if message.reply_to_message else None
    url = get_url(message)

    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"𝙑𝙞𝙙𝙚𝙤 𝙄𝙨 𝙇𝙤𝙣𝙜𝙚𝙧 𝙏𝙝𝙖𝙣 {DURATION_LIMIT} 𝙈𝙞𝙣𝙪𝙩𝙚𝙨."
            )

        file_name = get_file_name(audio)
        title = file_name
        thumb_name = "https://telegra.ph/file/51a70e2ef9e0bde60b0d2.jpg"
        thumbnail = thumb_name
        duration = round(audio.duration / 60)
        views = "Locally added"

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="𝘾𝙝𝙖𝙣𝙣𝙚𝙡 🔊",
                        url="https://t.me/Sanki_BOTs")
                   
                ]
            ]
        )
        
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)  
        file_path = await converter.convert(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name)) else file_name
        )

    elif url:
        try:
            results = YoutubeSearch(url, max_results=1).to_dict()
            # print results
            title = results[0]["title"]       
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f'thumb{title}.jpg'
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)
            duration = results[0]["duration"]
            url_suffix = results[0]["url_suffix"]
            views = results[0]["views"]
            durl = url
            durl = durl.replace("youtube", "youtubepp")
            
            secmul, dur, dur_arr = 1, 0, duration.split(':')
            for i in range(len(dur_arr)-1, -1, -1):
                dur += (int(dur_arr[i]) * secmul)
                secmul *= 60
                
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="𝙔𝙤𝙪𝙩𝙪𝙗𝙚 🎬",
                            url=f"{url}"),
                        InlineKeyboardButton(
                            text="𝘿𝙤𝙬𝙣𝙡𝙤𝙖𝙙 📥",
                            url=f"{durl}")

                    ]
                ]
            )
        except Exception as e:
            title = "NaN"
            thumb_name = "https://telegra.ph/file/51a70e2ef9e0bde60b0d2.jpg"
            duration = "NaN"
            views = "NaN"
            keyboard = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="𝙔𝙤𝙪𝙩𝙪𝙗𝙚 🎬",
                                url=f"https://youtube.com")

                        ]
                    ]
                )
        if (dur / 60) > DURATION_LIMIT:
             await lel.edit(f"𝙑𝙞𝙙𝙚𝙤 𝙄𝙨 𝙇𝙤𝙣𝙜𝙚𝙧 𝙏𝙝𝙖𝙣 {DURATION_LIMIT} 𝙈𝙞𝙣𝙪𝙩𝙚𝙨.")
             return
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)     
        file_path = await converter.convert(youtube.download(url))
    else:
        if len(message.command) < 2:
            return await lel.edit("🧐 **𝙒𝙝𝙞𝙘𝙝 𝙎𝙤𝙣𝙜 𝙔𝙤𝙪 𝙒𝙖𝙣𝙣𝙖 𝙋𝙡𝙖𝙮 ??**")
        await lel.edit("🔎 **𝙁𝙞𝙣𝙙𝙞𝙣𝙜... 𝙃𝙤𝙡𝙙 𝙊𝙣**")
        query = message.text.split(None, 1)[1]
        # print(query)
        await lel.edit("🔄 **𝙋𝙧𝙤𝙘𝙚𝙨𝙨𝙞𝙣𝙜... 𝙃𝙤𝙡𝙙 𝙊𝙣**")
        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            url = f"https://youtube.com{results[0]['url_suffix']}"
            # print results
            title = results[0]["title"]       
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f'thumb{title}.jpg'
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)
            duration = results[0]["duration"]
            url_suffix = results[0]["url_suffix"]
            views = results[0]["views"]
            durl = url
            durl = durl.replace("youtube", "youtubepp")

            secmul, dur, dur_arr = 1, 0, duration.split(':')
            for i in range(len(dur_arr)-1, -1, -1):
                dur += (int(dur_arr[i]) * secmul)
                secmul *= 60
                
        except Exception as e:
            await lel.edit(
                "𝙎𝙤𝙧𝙧𝙮 𝙎𝙤𝙣𝙜 𝙉𝙤𝙩 𝙁𝙤𝙪𝙣𝙙 ☹ ️𝙏𝙧𝙮 𝘼𝙜𝙖𝙞𝙣..."
            )
            print(str(e))
            return

        keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="𝙔𝙤𝙪𝙩𝙪𝙗𝙚 🎬",
                            url=f"{url}"),
                        InlineKeyboardButton(
                            text="𝘿𝙤𝙬𝙣𝙡𝙤𝙖𝙙 📥",
                            url=f"{durl}")

                    ]
                ]
            )
        
        if (dur / 60) > DURATION_LIMIT:
             await lel.edit(f"𝙑𝙞𝙙𝙚𝙤 𝙄𝙨 𝙇𝙤𝙣𝙜𝙚𝙧 𝙏𝙝𝙖𝙣 {DURATION_LIMIT} 𝙈𝙞𝙣𝙪𝙩𝙚𝙨.")
             return
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)  
        file_path = await converter.convert(youtube.download(url))
  
    if message.chat.id in callsmusic.pytgcalls.active_calls:
        position = await queues.put(message.chat.id, file=file_path)
        await message.reply_photo(
        photo="final.png", 
        caption="**🎵 𝙎𝙤𝙣𝙜 :** {}\n**🕒 𝘿𝙪𝙧𝙖𝙩𝙞𝙤𝙣 :** {} 𝙢𝙞𝙣\n**👤 𝘼𝙙𝙙𝙚𝙙 𝘽𝙮 :** {}\n\n**#⃣ 𝙌𝙪𝙚𝙪𝙚𝙙 𝙋𝙤𝙨𝙞𝙩𝙞𝙤𝙣 :** {}".format(
        title, duration, message.from_user.mention(), position
        ),
        reply_markup=keyboard)
        os.remove("final.png")
        return await lel.delete()
    else:
        callsmusic.pytgcalls.join_group_call(message.chat.id, file_path)
        await message.reply_photo(
        photo="final.png",
        reply_markup=keyboard,
        caption="**🎵 𝙎𝙤𝙣𝙜 :** {}\n**🕒 𝘿𝙪𝙧𝙖𝙩𝙞𝙤𝙣 :** {} 𝙢𝙞𝙣\n**👤 𝘼𝙙𝙙𝙚𝙙 𝘽𝙮 :** {}\n\n**▶️ 𝙉𝙤𝙬 𝙋𝙡𝙖𝙮𝙞𝙣𝙜 𝘼𝙩 `{}`**".format(
        title, duration, message.from_user.mention(), message.chat.title
        ), )
        os.remove("final.png")
        return await lel.delete()
