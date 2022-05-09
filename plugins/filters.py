

import re
import pyrogram
import asyncio

from pyrogram import (
    filters,
    Client
)

from pyrogram.types import (
    InlineKeyboardButton, 
    InlineKeyboardMarkup, 
    Message,
    CallbackQuery
)

from bot import Bot
from script import script
from config import MAINCHANNEL_ID, ADMINS, LOG_CHANNEL

BUTTONS = {}
 
@Client.on_message(filters.incoming & filters.text)
async def filter(client: Bot, message: Message):
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return

    if len(message.text) > 1:    
        btn = []
        async for msg in client.USER.search_messages(MAINCHANNEL_ID,query=message.text,filter='url'):
            file_name = msg.text
            msg_id = msg.message_id                     
            link = msg.link
            btn.append(
                [InlineKeyboardButton(text=f"{file_name}",url=f"{link}")]
            )

        if not btn:
            return

        if len(btn) > 10: 
            btns = list(split_list(btn, 10)) 
            keyword = f"{message.chat.id}-{message.message_id}"
            BUTTONS[keyword] = {
                "total" : len(btns),
                "buttons" : btns
            }
        else:
            cap = f"\n<b>️📽️ℝ𝕖𝕢𝕦𝕖𝕤𝕥𝕖𝕕 𝕄𝕠𝕧𝕚𝕖 </b> : {message.text}\n<b>👤ℝ𝕖𝕢𝕦𝕖𝕤𝕥𝕖𝕕 𝕓𝕪 </b> : {message.from_user.mention}\n\n⚙️<b>𝗧𝗵𝗶𝘀 𝗺𝗲𝘀𝘀𝗮𝗴𝗲 𝘄𝗶𝗹𝗹 𝗯𝗲 𝗱𝗲𝗹𝗲𝘁𝗲𝗱 𝗮𝗳𝘁𝗲𝗿 1 𝗺𝗶𝗻𝘂𝘁𝗲.</b>"
            reply_id = message.reply_to_message.message_id if message.reply_to_message else message.message_id
            buttons = btn 
            buttons.append(

                [InlineKeyboardButton(text="☝️ 𝗧𝗮𝗸𝗲 𝗔𝗕𝗢𝗩𝗘 𝗿𝗲𝘀𝘂𝗹𝘁 ☝️",callback_data="pages")]

            )
            await asyncio.sleep(3)
            await client.send_message(LOG_CHANNEL,f'{message.from_user.mention} took file👇 \n\n<b>{message.text}</b>')
            fuk = await message.reply_photo(photo="https://telegra.ph/file/4e7e0a76a54d16ce2b80c.jpg", caption=cap, reply_to_message_id=reply_id, reply_markup=InlineKeyboardMarkup(buttons))
            await asyncio.sleep(40)
            await fuk.edit(f"\n \n⚙️ {message.from_user.mention}'s Result for {message.text} Closed ️")
            return

        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()

        buttons.append(
            [InlineKeyboardButton(text="NEXT ⏩",callback_data=f"next_0_{keyword}")]
        )    
        buttons.append(
            [InlineKeyboardButton(text=f"📃 Pages 1/{data['total']}",callback_data="pages")]
        )

        cap = f"\n<b>️📽️ℝ𝕖𝕢𝕦𝕖𝕤𝕥𝕖𝕕 𝕄𝕠𝕧𝕚𝕖 </b> : {message.text}\n<b>👤ℝ𝕖𝕢𝕦𝕖𝕤𝕥𝕖𝕕 𝕓𝕪 </b> : {message.from_user.mention}\n\n⚙️<b>𝗧𝗵𝗶𝘀 𝗺𝗲𝘀𝘀𝗮𝗴𝗲 𝘄𝗶𝗹𝗹 𝗯𝗲 𝗱𝗲𝗹𝗲𝘁𝗲𝗱 𝗮𝗳𝘁𝗲𝗿 1 𝗺𝗶𝗻𝘂𝘁𝗲.</b>"
        reply_id = message.reply_to_message.message_id if message.reply_to_message else message.message_id
        await asyncio.sleep(3)
        await client.send_message(LOG_CHANNEL,f'{message.from_user.mention} took file👇 \n\n<b>{message.text}</b>')
        fuk = await message.reply_photo(photo="https://telegra.ph/file/4e7e0a76a54d16ce2b80c.jpg", caption=cap, reply_to_message_id=reply_id, reply_markup=InlineKeyboardMarkup(buttons))
        await asyncio.sleep(40)
        await fuk.edit(f"\n \n⚙️ {message.from_user.mention}'s Result for {message.text} Closed ️")  


@Client.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    if query.message.reply_to_message.from_user.id == query.from_user.id:

        if query.data.startswith("next"):
            await query.answer()
            ident, index, keyword = query.data.split("_")
            data = BUTTONS[keyword]

            if int(index) == int(data["total"]) - 2:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("⏪ BACK", callback_data=f"back_{int(index)+1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"📃 Pages {int(index)+2}/{data['total']}", callback_data="pages")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return
            else:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("⏪ BACK", callback_data=f"back_{int(index)+1}_{keyword}"),InlineKeyboardButton("NEXT ⏩", callback_data=f"next_{int(index)+1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"📃 Pages {int(index)+2}/{data['total']}", callback_data="pages")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return


        elif query.data.startswith("back"):
            await query.answer()
            ident, index, keyword = query.data.split("_")
            data = BUTTONS[keyword] 

            if int(index) == 1:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("NEXT ⏩", callback_data=f"next_{int(index)-1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"📃 Pages {int(index)}/{data['total']}", callback_data="pages")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return   
            else:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("⏪ BACK", callback_data=f"back_{int(index)-1}_{keyword}"),InlineKeyboardButton("NEXT ⏩", callback_data=f"next_{int(index)-1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"📃 Pages {int(index)}/{data['total']}", callback_data="pages")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return


        elif query.data == "pages":
            await query.answer()


        elif query.data == "start_data":
            await query.answer()
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("HELP", callback_data="help_data"),
                    InlineKeyboardButton("ABOUT", callback_data="about_data")],
                [InlineKeyboardButton("⭕️ JOIN OUR CHANNEL ⭕️", url="https://t.me/CineHub02")]
            ])

            await query.message.edit_text(
                script.START_MSG.format(query.from_user.mention),
                reply_markup=keyboard,
                disable_web_page_preview=True
            )


        elif query.data == "help_data":
            await query.answer()
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("BACK", callback_data="start_data"),
                    InlineKeyboardButton("ABOUT", callback_data="about_data")],
                [InlineKeyboardButton("⭕️ SUPPORT ⭕️", url="https://t.me/CineHub02")]
            ])

            await query.message.edit_text(
                script.HELP_MSG,
                reply_markup=keyboard,
                disable_web_page_preview=True
            )


        elif query.data == "about_data":
            await query.answer()
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("BACK", callback_data="help_data"),
                    InlineKeyboardButton("START", callback_data="start_data")],
                [InlineKeyboardButton("SOURCE CODE", url="https://github.com/soymadip")]
            ])

            await query.message.edit_text(
                script.ABOUT_MSG,
                reply_markup=keyboard,
                disable_web_page_preview=True
            )


    else:
        await query.answer("Thats not for you!!",show_alert=True)


def split_list(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]  
