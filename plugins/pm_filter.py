# Don't Remove Credit @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot @Tech_VJ
# Ask Doubt on telegram @KingVJ01

import os, logging, string, asyncio, time, re, ast, random, math, pytz, pyrogram
from datetime import datetime, timedelta, date, time
from Script import script
from info import *
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaPhoto, ChatPermissions, WebAppInfo
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait, UserIsBlocked, MessageNotModified, PeerIdInvalid
from pyrogram.errors.exceptions.bad_request_400 import MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty
from utils import get_size, is_subscribed, pub_is_subscribed, get_poster, search_gagala, temp, get_settings, save_group_settings, get_shortlink, get_tutorial, send_all, get_cap
from database.users_chats_db import db
from database.ia_filterdb import Media, get_file_details, get_search_results, get_bad_files
from database.filters_mdb import del_all, find_filter, get_filters
from database.connections_mdb import active_connection, all_connections, delete_connection, if_active, make_active, make_inactive
from database.gfilters_mdb import find_gfilter, get_gfilters, del_allg
from urllib.parse import quote_plus
from TechVJ.util.file_properties import get_name, get_hash, get_media_file_size
from plugins.Extra.save_restrict_content.save import run_save, get_link
from plugins.Extra.save_restrict_content.join import join

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)
lock = asyncio.Lock()

BUTTON = {}
BUTTONS = {}
FRESH = {}
BUTTONS0 = {}
BUTTONS1 = {}
BUTTONS2 = {}
SPELL_CHECK = {}

@Client.on_message(filters.group & filters.text & filters.incoming)
async def give_filter(client, message):
    if message.chat.id != SUPPORT_CHAT_ID:
        settings = await get_settings(message.chat.id)
        chatid = message.chat.id 
        user_id = message.from_user.id if message.from_user else 0
        if settings.get('fsub') != None:
            try:
                btn = await pub_is_subscribed(client, message, settings['fsub'])
                if btn:
                    btn.append([InlineKeyboardButton("Unmute Me ðŸ”•", callback_data=f"unmuteme#{int(user_id)}")])
                    await client.restrict_chat_member(chatid, message.from_user.id, ChatPermissions(can_send_messages=False))
                    await message.reply_photo(photo=random.choice(PICS), caption=f"ðŸ‘‹ Hello {message.from_user.mention},\n\nPlease join the channel then click on unmute me button. ðŸ˜‡", reply_markup=InlineKeyboardMarkup(btn), parse_mode=enums.ParseMode.HTML)
                    return
            except Exception as e:
                print(e)
            
        manual = await manual_filters(client, message)
        if manual == False:
            settings = await get_settings(message.chat.id)
            try:
                if settings.get('auto_ffilter'):
                    ai_search = True
                    reply_msg = await message.reply_text(f"<b><i>Searching For {message.text} ðŸ”</i></b>")
                    await auto_filter(client, message.text, message, reply_msg, ai_search)
            except KeyError:
                grpid = await active_connection(str(message.from_user.id))
                await save_group_settings(grpid, 'auto_ffilter', True)
                settings = await get_settings(message.chat.id)
                if settings.get('auto_ffilter'):
                    ai_search = True
                    reply_msg = await message.reply_text(f"<b><i>Searching For {message.text} ðŸ”</i></b>")
                    await auto_filter(client, message.text, message, reply_msg, ai_search)
    else: #a better logic to avoid repeated lines of code in auto_filter function
        search = message.text
        temp_files, temp_offset, total_results = await get_search_results(chat_id=message.chat.id, query=search.lower(), offset=0, filter=True)
        if total_results == 0:
            return
        else:
            return await message.reply_text(f"<b>Há´‡Ê {message.from_user.mention}, {str(total_results)} Ê€á´‡sá´œÊŸá´›s á´€Ê€á´‡ Ò“á´á´œÉ´á´… ÉªÉ´ á´Ê á´…á´€á´›á´€Ê™á´€sá´‡ Ò“á´Ê€ Êá´á´œÊ€ á´Ì¨á´œá´‡Ê€Ê {search}. \n\nTÊœÉªs Éªs á´€ sá´œá´˜á´˜á´Ê€á´› É¢Ê€á´á´œá´˜ sá´ á´›Êœá´€á´› Êá´á´œ á´„á´€É´'á´› É¢á´‡á´› Ò“ÉªÊŸá´‡s Ò“Ê€á´á´ Êœá´‡Ê€á´‡...\n\nJá´ÉªÉ´ á´€É´á´… Sá´‡á´€Ê€á´„Êœ Há´‡Ê€á´‡ - https://t.me/+X6JIRNl5xeQxYzY1</b>")

@Client.on_message(filters.private & filters.text & filters.incoming)
async def pm_text(bot, message):
    content = message.text
    user = message.from_user.first_name
    user_id = message.from_user.id
    save = await db.get_save(user_id)
    if 't.me/+' in content and SAVE_RESTRICTED_MODE == True:
        await join(message, content)
        return 
    if save == True and SAVE_RESTRICTED_MODE == True:
        try:
            link = get_link(content)
            if not link:
                if content.startswith("/") or content.startswith("#"): return  # ignore commands and hashtags
                if PM_SEARCH == True:
                    ai_search = True
                    reply_msg = await bot.send_message(message.from_user.id, f"<b><i>Searching For {content} ðŸ”</i></b>", reply_to_message_id=message.id)
                    await auto_filter(bot, content, message, reply_msg, ai_search)
                else:
                    await message.reply_text(text=f"<b>Êœá´‡Ê {user} ðŸ˜ ,\n\nÊá´á´œ á´„á´€É´'á´› É¢á´‡á´› á´á´á´ Éªá´‡s êœ°Ê€á´á´ Êœá´‡Ê€á´‡. Ê€á´‡Ç«á´œá´‡sá´› Éªá´› ÉªÉ´ á´á´œÊ€ <a href=https://t.me/+X6JIRNl5xeQxYzY1>á´á´á´ Éªá´‡ É¢Ê€á´á´œá´˜</a> á´Ê€ á´„ÊŸÉªá´„á´‹ Ê€á´‡Ç«á´œá´‡sá´› Êœá´‡Ê€á´‡ Ê™á´œá´›á´›á´É´ Ê™á´‡ÊŸá´á´¡ ðŸ‘‡</b>", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ðŸ“ Ê€á´‡Ç«á´œá´‡sá´› Êœá´‡Ê€á´‡ ", url=f"https://t.me/+X6JIRNl5xeQxYzY1")]]))
                    await bot.send_message(chat_id=LOG_CHANNEL, text=f"<b>#ððŒ_ðŒð’ð†\n\nNá´€á´á´‡ : {user}\n\nID : {user_id}\n\nMá´‡ssá´€É¢á´‡ : {content}</b>")
        except TypeError:
            return 
        _range = await bot.ask(user_id, "**sá´‡É´á´… á´á´‡ á´›Êœá´‡ É´á´œá´Ê™á´‡Ê€ á´Ò“ Ò“ÉªÊŸá´‡s/Ê€á´€É´É¢á´‡ Êá´á´œ á´¡á´€É´á´› á´›á´ sá´€á´ á´‡ Ò“Ê€á´á´ á´›Êœá´‡ É¢Éªá´ á´‡É´ á´á´‡ssá´€É¢á´‡**")
        try:
            value = int(_range.text)
            if value > 100:
                await _range.reply("**Êá´á´œ á´„á´€É´ á´É´ÊŸÊ É¢á´‡á´› á´œá´˜á´›á´ 100 Ò“ÉªÊŸá´‡s ÉªÉ´ á´€ sÉªÉ´É¢ÊŸá´‡ Ê™á´€á´›á´„Êœ.**")
                return
        except ValueError:
            await _range.reply("**Ê€á´€É´É¢á´‡ á´á´œsá´› Ê™á´‡ á´€É´ ÉªÉ´á´›á´‡É¢á´‡Ê€**")
        await run_save(bot, user_id, content, value) 
        await db.set_save(user_id, save=False)
        return 
    if content.startswith("/") or content.startswith("#"): return  # ignore commands and hashtags
    if PM_SEARCH == True:
        ai_search = True
        reply_msg = await bot.send_message(message.from_user.id, f"<b><i>Searching For {content} ðŸ”</i></b>", reply_to_message_id=message.id)
        await auto_filter(bot, content, message, reply_msg, ai_search)
    else:
        await message.reply_text(text=f"<b>Êœá´‡Ê {user} ðŸ˜ ,\n\nÊá´á´œ á´„á´€É´'á´› É¢á´‡á´› á´á´á´ Éªá´‡s êœ°Ê€á´á´ Êœá´‡Ê€á´‡. Ê€á´‡Ç«á´œá´‡sá´› Éªá´› ÉªÉ´ á´á´œÊ€ <a href=https://t.me/+X6JIRNl5xeQxYzY1>á´á´á´ Éªá´‡ É¢Ê€á´á´œá´˜</a> á´Ê€ á´„ÊŸÉªá´„á´‹ Ê€á´‡Ç«á´œá´‡sá´› Êœá´‡Ê€á´‡ Ê™á´œá´›á´›á´É´ Ê™á´‡ÊŸá´á´¡ ðŸ‘‡</b>", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ðŸ“ Ê€á´‡Ç«á´œá´‡sá´› Êœá´‡Ê€á´‡ ", url=f"https://t.me/+X6JIRNl5xeQxYzY1")]]))
        await bot.send_message(chat_id=LOG_CHANNEL, text=f"<b>#ððŒ_ðŒð’ð†\n\nNá´€á´á´‡ : {user}\n\nID : {user_id}\n\nMá´‡ssá´€É¢á´‡ : {content}</b>")

@Client.on_callback_query(filters.regex(r"^next"))
async def next_page(bot, query):
    ident, req, key, offset = query.data.split("_")
    curr_time = datetime.now(pytz.timezone('Asia/Kolkata')).time()
    if int(req) not in [query.from_user.id, 0]:
        return await query.answer(script.ALRT_TXT.format(query.from_user.first_name), show_alert=True)
    try:
        offset = int(offset)
    except:
        offset = 0
    if BUTTONS.get(key)!=None:
        search = BUTTONS.get(key)
    else:
        search = FRESH.get(key)
    if not search:
        await query.answer(script.OLD_ALRT_TXT.format(query.from_user.first_name),show_alert=True)
        return

    files, n_offset, total = await get_search_results(query.message.chat.id, search, offset=offset, filter=True)
    try:
        n_offset = int(n_offset)
    except:
        n_offset = 0

    if not files:
        return
    temp.GETALL[key] = files
    temp.SHORT[query.from_user.id] = query.message.chat.id
    settings = await get_settings(query.message.chat.id)
    pre = 'filep' if settings['file_secure'] else 'file'
    if settings['button']:
        btn = [
            [
                InlineKeyboardButton(
                    text=f"[{get_size(file.file_size)}] {' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@') and not x.startswith('www.'), file.file_name.split()))}", callback_data=f'{pre}#{file.file_id}'
                ),
            ]
            for file in files
        ]

        btn.insert(0, 
            [
                InlineKeyboardButton(f'Ç«á´œá´€ÊŸÉªá´›Ê', callback_data=f"qualities#{key}"),
                InlineKeyboardButton("á´‡á´˜Éªsá´á´…á´‡s", callback_data=f"episodes#{key}"),
                InlineKeyboardButton("sá´‡á´€sá´É´s",  callback_data=f"seasons#{key}")
            ]
        )
        btn.insert(0, [
            InlineKeyboardButton("ð’ðžð§ð ð€ð¥ð¥", callback_data=f"sendfiles#{key}"),
            InlineKeyboardButton("ÊŸá´€É´É¢á´œá´€É¢á´‡s", callback_data=f"languages#{key}"),
            InlineKeyboardButton("Êá´‡á´€Ê€s", callback_data=f"years#{key}")
        ])
    else:
        btn = []
        btn.insert(0, 
            [
                InlineKeyboardButton(f'Ç«á´œá´€ÊŸÉªá´›Ê', callback_data=f"qualities#{key}"),
                InlineKeyboardButton("á´‡á´˜Éªsá´á´…á´‡s", callback_data=f"episodes#{key}"),
                InlineKeyboardButton("sá´‡á´€sá´É´s",  callback_data=f"seasons#{key}")
            ]
        )
        btn.insert(0, [
            InlineKeyboardButton("ð’ðžð§ð ð€ð¥ð¥", callback_data=f"sendfiles#{key}"),
            InlineKeyboardButton("ÊŸá´€É´É¢á´œá´€É¢á´‡s", callback_data=f"languages#{key}"),
            InlineKeyboardButton("Êá´‡á´€Ê€s", callback_data=f"years#{key}")
        ])
    try:
        if settings['max_btn']:
            if 0 < offset <= 10:
                off_set = 0
            elif offset == 0:
                off_set = None
            else:
                off_set = offset - 10
            if n_offset == 0:
                btn.append(
                    [InlineKeyboardButton("âŒ« ðð€ð‚ðŠ", callback_data=f"next_{req}_{key}_{off_set}"), InlineKeyboardButton(f"{math.ceil(int(offset)/10)+1} / {math.ceil(total/10)}", callback_data="pages")]
                )
            elif off_set is None:
                btn.append([InlineKeyboardButton("ðð€ð†ð„", callback_data="pages"), InlineKeyboardButton(f"{math.ceil(int(offset)/10)+1} / {math.ceil(total/10)}", callback_data="pages"), InlineKeyboardButton("ðð„ð—ð“ âžª", callback_data=f"next_{req}_{key}_{n_offset}")])
            else:
                btn.append(
                    [
                        InlineKeyboardButton("âŒ« ðð€ð‚ðŠ", callback_data=f"next_{req}_{key}_{off_set}"),
                        InlineKeyboardButton(f"{math.ceil(int(offset)/10)+1} / {math.ceil(total/10)}", callback_data="pages"),
                        InlineKeyboardButton("ðð„ð—ð“ âžª", callback_data=f"next_{req}_{key}_{n_offset}")
                    ],
                )
        else:
            if 0 < offset <= int(MAX_B_TN):
                off_set = 0
            elif offset == 0:
                off_set = None
            else:
                off_set = offset - int(MAX_B_TN)
            if n_offset == 0:
                btn.append(
                    [InlineKeyboardButton("âŒ« ðð€ð‚ðŠ", callback_data=f"next_{req}_{key}_{off_set}"), InlineKeyboardButton(f"{math.ceil(int(offset)/int(MAX_B_TN))+1} / {math.ceil(total/int(MAX_B_TN))}", callback_data="pages")]
                )
            elif off_set is None:
                btn.append([InlineKeyboardButton("ðð€ð†ð„", callback_data="pages"), InlineKeyboardButton(f"{math.ceil(int(offset)/int(MAX_B_TN))+1} / {math.ceil(total/int(MAX_B_TN))}", callback_data="pages"), InlineKeyboardButton("ðð„ð—ð“ âžª", callback_data=f"next_{req}_{key}_{n_offset}")])
            else:
                btn.append(
                    [
                        InlineKeyboardButton("âŒ« ðð€ð‚ðŠ", callback_data=f"next_{req}_{key}_{off_set}"),
                        InlineKeyboardButton(f"{math.ceil(int(offset)/int(MAX_B_TN))+1} / {math.ceil(total/int(MAX_B_TN))}", callback_data="pages"),
                        InlineKeyboardButton("ðð„ð—ð“ âžª", callback_data=f"next_{req}_{key}_{n_offset}")
                    ],
                )
    except KeyError:
        await save_group_settings(query.message.chat.id, 'max_btn', True)
        if 0 < offset <= 10:
            off_set = 0
        elif offset == 0:
            off_set = None
        else:
            off_set = offset - 10
        if n_offset == 0:
            btn.append(
                [InlineKeyboardButton("âŒ« ðð€ð‚ðŠ", callback_data=f"next_{req}_{key}_{off_set}"), InlineKeyboardButton(f"{math.ceil(int(offset)/10)+1} / {math.ceil(total/10)}", callback_data="pages")]
            )
        elif off_set is None:
            btn.append([InlineKeyboardButton("ðð€ð†ð„", callback_data="pages"), InlineKeyboardButton(f"{math.ceil(int(offset)/10)+1} / {math.ceil(total/10)}", callback_data="pages"), InlineKeyboardButton("ðð„ð—ð“ âžª", callback_data=f"next_{req}_{key}_{n_offset}")])
        else:
            btn.append(
                [
                    InlineKeyboardButton("âŒ« ðð€ð‚ðŠ", callback_data=f"next_{req}_{key}_{off_set}"),
                    InlineKeyboardButton(f"{math.ceil(int(offset)/10)+1} / {math.ceil(total/10)}", callback_data="pages"),
                    InlineKeyboardButton("ðð„ð—ð“ âžª", callback_data=f"next_{req}_{key}_{n_offset}")
                ],
            )
    if not settings["button"]:
        cur_time = datetime.now(pytz.timezone('Asia/Kolkata')).time()
        time_difference = timedelta(hours=cur_time.hour, minutes=cur_time.minute, seconds=(cur_time.second+(cur_time.microsecond/1000000))) - timedelta(hours=curr_time.hour, minutes=curr_time.minute, seconds=(curr_time.second+(curr_time.microsecond/1000000)))
        remaining_seconds = "{:.2f}".format(time_difference.total_seconds())
        cap = await get_cap(settings, remaining_seconds, files, query, total, search)
        try:
            await query.message.edit_text(text=cap, reply_markup=InlineKeyboardMarkup(btn), disable_web_page_preview=True)
        except MessageNotModified:
            pass
    else:
        try:
            await query.edit_message_reply_markup(
                reply_markup=InlineKeyboardMarkup(btn)
            )
        except MessageNotModified:
            pass
    await query.answer()

@Client.on_callback_query(filters.regex(r"^spol"))
async def advantage_spoll_choker(bot, query):
    _, user, movie_ = query.data.split('#')
    movies = SPELL_CHECK.get(query.message.reply_to_message.id)
    if not movies:
        return await query.answer(script.OLD_ALRT_TXT.format(query.from_user.first_name), show_alert=True)
    if int(user) != 0 and query.from_user.id != int(user):
        return await query.answer(script.ALRT_TXT.format(query.from_user.first_name), show_alert=True)
    if movie_ == "close_spellcheck":
        return await query.message.delete()
    movie = movies[(int(movie_))]
    movie = re.sub(r"[:\-]", " ", movie)
    movie = re.sub(r"\s+", " ", movie).strip()
    await query.answer(script.TOP_ALRT_MSG)
    gl = await global_filters(bot, query.message, text=movie)
    if gl == False:
        k = await manual_filters(bot, query.message, text=movie)
        if k == False:
            files, offset, total_results = await get_search_results(query.message.chat.id, movie, offset=0, filter=True)
            if files:
                k = (movie, files, offset, total_results)
                ai_search = True
                reply_msg = await query.message.edit_text(f"<b><i>Searching For {movie} ðŸ”</i></b>")
                await auto_filter(bot, movie, query, reply_msg, ai_search, k)
            else:
                reqstr1 = query.from_user.id if query.from_user else 0
                reqstr = await bot.get_users(reqstr1)
                if NO_RESULTS_MSG:
                    await bot.send_message(chat_id=LOG_CHANNEL, text=(script.NORSLTS.format(reqstr.id, reqstr.mention, movie)))
                k = await query.message.edit(script.MVE_NT_FND)
                await asyncio.sleep(10)
                await k.delete()

# Year 
@Client.on_callback_query(filters.regex(r"^years#"))
async def years_cb_handler(client: Client, query: CallbackQuery):

    try:
        if int(query.from_user.id) not in [query.message.reply_to_message.from_user.id, 0]:
            return await query.answer(
                f"âš ï¸ Êœá´‡ÊŸÊŸá´{query.from_user.first_name},\ná´›ÊœÉªêœ± Éªêœ± É´á´á´› Êá´á´œÊ€ á´á´á´ Éªá´‡ Ê€á´‡Qá´œá´‡êœ±á´›,\nÊ€á´‡Qá´œá´‡êœ±á´› Êá´á´œÊ€'êœ±...",
                show_alert=True,
            )
    except:
        pass
    _, key = query.data.split("#")
    search = FRESH.get(key)
    search = search.replace(' ', '_')
    btn = []
    for i in range(0, len(YEARS)-1, 4):
        row = []
        for j in range(4):
            if i+j < len(YEARS):
                row.append(
                    InlineKeyboardButton(
                        text=YEARS[i+j].title(),
                        callback_data=f"fy#{YEARS[i+j].lower()}#{key}"
                    )
                )
        btn.append(row)

    btn.insert(
        0,
        [
            InlineKeyboardButton(
                text="sá´‡ÊŸá´‡á´„á´› Êá´á´œÊ€ Êá´‡á´€Ê€", callback_data="ident"
            )
        ],
    )
    req = query.from_user.id
    offset = 0
    btn.append([InlineKeyboardButton(text="â†­ Ê™á´€á´„á´‹ á´›á´ êœ°ÉªÊŸá´‡s â†­", callback_data=f"fy#homepage#{key}")])

    await query.edit_message_reply_markup(InlineKeyboardMarkup(btn))
    

@Client.on_callback_query(filters.regex(r"^fy#"))
async def filter_yearss_cb_handler(client: Client, query: CallbackQuery):
    _, lang, key = query.data.split("#")
    curr_time = datetime.now(pytz.timezone('Asia/Kolkata')).time()
    search = FRESH.get(key)
    search = search.replace("_", " ")
    baal = lang in search
    if baal:
        search = search.replace(lang, "")
    else:
        search = search
    req = query.from_user.id
    chat_id = query.message.chat.id
    message = query.message
    try:
        if int(req) not in [query.message.reply_to_message.from_user.id, 0]:
            return await query.answer(
                f"âš ï¸ Êœá´‡ÊŸÊŸá´{query.from_user.first_name},\ná´›ÊœÉªêœ± Éªêœ± É´á´á´› Êá´á´œÊ€ á´á´á´ Éªá´‡ Ê€á´‡Qá´œá´‡êœ±á´›,\nÊ€á´‡Qá´œá´‡êœ±á´› Êá´á´œÊ€'êœ±...",
                show_alert=True,
            )
    except:
        pass
    if lang != "homepage":
        search = f"{search} {lang}" 
    BUTTONS[key] = search

    files, offset, total_results = await get_search_results(chat_id, search, offset=0, filter=True)
    if not files:
        await query.answer("ðŸš« ð—¡ð—¼ ð—™ð—¶ð—¹ð—² ð—ªð—²ð—¿ð—² ð—™ð—¼ð˜‚ð—»ð—± ðŸš«", show_alert=1)
        return
    temp.GETALL[key] = files
    settings = await get_settings(message.chat
