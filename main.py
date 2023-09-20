# A project by Muhammad Mirab Br. ☘️
# Collabortors: Iliya Faramarzi
# Kara Group Management Bot
from pyrogram import Client, filters, enums, errors
import dbManagement as dbManager
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, MessageEntity
import ast
import requests
from datetool import calendar
from datetime import datetime
import emoji
import enchant
dbm = dbManager.dbManager()

#Connect code to your bot
#app = Client('karaGroupManagement', api_id= your api id, api_hash= 'your api hash', bot_token= 'your bot token')
app = Client('karaGroupManagement')

bad_words = ['احمق', 'بیشعور', 'روانی']


def checkMessage(chat_ID, type):
    get_settings = dbm.GetSettings(chat_ID)
    settings = ['emoji', 'link', 'gif', 'sticker', 'picture', 'video', 'music', 'file', 'english', 'bad_words']
    return True if get_settings[settings.index(type)] == 1 else False # Delete message if True 


def settingsButtons(chat_id, user_id):
    settings = dbm.GetSettings(chat_id) 
    """
    [0] --> emoji   
    [1] --> link
    [2] --> git
    [3] --> sticker
    [4] --> picture
    [5] --> video
    [6] --> music
    [7] --> file
    [8] --> englsih
    [9] --> bad_words
    0 means disable and 1 means True
    """

    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton('ایموجی✅' if settings[0] == 1 else 'ایموجی❌', callback_data = f'emoji-{chat_id}'),
                InlineKeyboardButton('لینک✅' if settings[1] == 1 else 'لینک❌', callback_data = 'link-{chat_id}')
            ],
            [
                InlineKeyboardButton('گیف✅' if settings[2] == 1 else 'گیف❌', callback_data = f'gif-{chat_id}'),
                InlineKeyboardButton('استیکر✅' if settings[3] == 1 else 'استیکر❌', callback_data = f'sticker-{chat_id}')
            ],
            [
                InlineKeyboardButton('عکس✅' if settings[4] == 1 else 'عکس❌', callback_data = f'picture-{chat_id}'),
                InlineKeyboardButton('فیلم✅' if settings[5] == 1 else 'فیلم❌', callback_data = f'video-{chat_id}')
            ],
            [
                InlineKeyboardButton('آهنگ✅' if settings[6] == 1 else 'آهنگ❌', callback_data = f'music-{chat_id}'),
                InlineKeyboardButton('فایل✅' if settings[7] == 1 else 'فایل❌', callback_data = f'file-{chat_id}')                       
            ],
            [
                InlineKeyboardButton('انگلیسی✅' if settings[8] == 1 else 'انگلیسی❌', callback_data = f'english-{chat_id}'),
                InlineKeyboardButton('کلمات نامناسب✅' if settings[9] == 1 else 'کلمات نامناسب❌', callback_data = f'bad_words-{chat_id}')
            ],
            [
                InlineKeyboardButton('بازگشت', callback_data = f'back_to_main_menu-{user_id}')
            ]
        ]
    )

    return buttons


# the stage where bot is added and becomes an admin
@app.on_message(filters.service)
async def services(client, message):
    chatID = dbm.getChatID(message.chat.id)
    # availableGroups is the variable in which the groups that the bot is already added to are listed
    availableGroups = dbm.getAvailableGroupsID()

    try:
        if message.chat.type != "private":
            new_member_status = message.new_chat_members[0]
            if new_member_status.is_self == True:
                # checks wheter it was previously added to this group or not 
                if chatID not in availableGroups:
                    dbm.addToGroupSettings(chatID)

                toBeEditedMessage = await app.send_message(message.chat.id, "ربات به گروه افزوده شد☘️\n\n» جهت آغاز فرآیند نصب و پیکربندی \nربات را ادمین کامل نمایید🌱")
                dbm.AddAdmins(message.chat.id, f'{message.from_user.id} ')
                # the message is saved so that it can later be edited as a confirmation that bot has been upgraded to admin
                dbm.firstMessageEditID(chatID, toBeEditedMessage.id)
    except:
        pass


    try:
        new_member_status = message.new_chat_members[0]
    except:
        pass

    # checking in the database if the admin has turned off the welcome feature
    wetherWelcomeIsEnabled = dbm.checkWetherGroupSettingIsSet(chatID, "isWelcomeEnabled")
    if wetherWelcomeIsEnabled[0] == 1:
        try:
            if new_member_status.is_self != True:
                welcomeMessage = dbm.checkWetherGroupSettingIsSet(chatID, "welcomeMessage")
                new_member = [u.mention for u in message.new_chat_members]
                welcomeMessage = welcomeMessage[0].replace("[کاربر]", f"{new_member[0]}")
                await app.send_message(chatID, welcomeMessage)

        except:
            pass

    # cur.execute(
    #     f"SELECT panelCategoriesFlag FROM group{chatID} WHERE panelCategories = 'join'")
    # wetherJoinIsEnabled = cur.fetchall()[0][0]
    # if wetherJoinIsEnabled == 1:
    #     app.delete_messages(chat_id, message_id)


@app.on_chat_member_updated()
async def update_member(client, message):

    try:
        if message.old_chat_member != None and message.old_chat_member.privilegs == None:
            pass

    except AttributeError:
        try:
            member = await app.get_chat_member(message.chat.id, "me")

            if message.chat.type == enums.ChatType.CHANNEL:
                if member.status == enums.ChatMemberStatus.ADMINISTRATOR and message.new_chat_member.privileges.can_post_messages:
                    await app.send_message(message.new_chat_member.promoted_by.id, 'ربات با موفقیت در کانال ادمین شد')

                elif not message.new_chat_member.privileges.can_post_messages:
                    await app.send_message(message.new_chat_member.promoted_by.id, 'لطفا ابتدا ربات را از کانال حذف و دوباره اضافه کنید و توجه کنید که باید هنگام اضافه کردن ربات به کانال دسترسی ارسال پیام را به ربات بدهید.')

            elif message.chat.type == enums.ChatType.GROUP or message.chat.type == enums.ChatType.SUPERGROUP:
                if member.status == enums.ChatMemberStatus.ADMINISTRATOR and member.user == message.new_chat_member.user:
                    final = ''
                    admins = ''

                    # getting the admin users to display them in the message
                    async for i in app.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
                        if not i.user.is_self:
                            final += '[%s](tg://user?id=%i)\n' % (i.user.first_name, i.user.id)
                            if i.user.id != dbm.GetAllValues(message.chat.id)[1]:
                                admins += '%s ' % str(i.user.id)

                    dbm.AddAdmins(message.chat.id, f'{dbm.GetAllValues(message.chat.id)[1]} {admins}')
                    await app.edit_message_text(message.chat.id, int(dbm.getFirstMessageEditID(dbm.getChatID(message.chat.id))[0]), 'ربات با موفقیت در گروه فعال شد.\n\n ادمین های شناسایی شده:\n%s' % final, reply_markup=InlineKeyboardMarkup(
                                [
                                    [
                                        InlineKeyboardButton('ادامه پیکربندی', url = f'https://t.me/curlymoderaotbot?start=Continue_config_{message.chat.id}')
                                    ],
                                ]))

                    
                    
                    # removing the first message which was edited to admin confirmation
                    dbm.removeFirstMessageEditID(dbm.getChatID(message.chat.id))
        except errors.exceptions.not_acceptable_406.ChannelPrivate:
            pass


@app.on_message(filters=filters.private & filters.command("start"))
async def private(client, message):
    text = message.text

    text = text.replace('/start ', '')
    if text == 'Continue_config_-1001908542984':
        chat_id = text.replace('Continue_config_', '')
        admins = []
        async for admin in app.get_chat_members(chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
            admins.append(admin.user.id)

        if message.from_user.id in admins:
            await app.send_message(message.from_user.id, 'با استفاده از این لنیک زیر ربات را در کانال مورد نظر ادمین کنید.', reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton('افزودن ربات به کانال', url='https://t.me/curlymoderaotbot?startchannel=true')
                    ],
                ]
            ))
        else:
            await app.send_message(message.from_user.id, 'شما دسترسی کافی را برای انجام این کار ندارید.')


@app.on_message(filters.text & filters.group)
async def group_messages(_, message):
    chat_id = message.chat.id
    message_id = message.id
    user_id = message.from_user.id
    text = message.text
    try:
        theMessage = message.text.split(" ")
    except:
        pass

    if checkMessage(chat_id, 'emoji'):
        if list(emoji.analyze(f'{text} a')) != []:
            await app.delete_messages(chat_id, message_id)

    if checkMessage(chat_id, 'link'):
        if message.entities != None and message.entities[0].type == enums.MessageEntityType.URL:
          await app.delete_messages(chat_id, message_id)  

    if checkMessage(chat_id, 'english'):
        d = enchant.Dict("en_US")
        for word in theMessage:
            if d.check(word) == False:
                break
            else:
                await app.delete_messages(chat_id, message_id)

    if checkMessage(chat_id, 'bad_words'):
        for word in theMessage:
            if word in bad_words:
                await app.delete_messages(chat_id, message_id)

    if theMessage[0] == "تعیین" and theMessage[1] == "موقعیت":
        title = ""
        pt = dbm.getUserPositionDict(dbm.getChatID(message.chat.id))[0]
        positionTitles = ast.literal_eval(pt) if pt != "" else {}
        for i in range(2): theMessage.pop(0)
        titleMessage = ' '.join(theMessage)
        numberOfTags = [t for t in titleMessage if t.find("@") == 0]
        if len(numberOfTags) != 0:
            taggedPeople = []
            for entity in range(len(message.entities)):
                offset = message.entities[entity].offset
                taggedPeople.append(message.text[ offset : offset + message.entities[0].length])
            taggedPeopleID = await app.get_users(taggedPeople)
            for i in taggedPeople: theMessage.remove(i)
            title = " ".join(theMessage)
            if len(title) > 16:
                await message.reply("موقعیت فرد نمی‌تواند بیشتر از 16 کاراکتر باشد❌")
            else:
                for j, i in enumerate(taggedPeopleID):
                    if i.id not in positionTitles:
                        await app.promote_chat_member(message.chat.id, i.id)
                        await app.set_administrator_title(message.chat.id, i.id, title)
                        positionTitles[i.id] = title
                        await message.reply(f"موقعیت موردنظر '{title}' برای کاربر {taggedPeople[j]} با موفقیت ثبت شد✅")
                    else: 
                        await message.reply(f"موقعیت کاربر {taggedPeople[j]} از قبل ذخیره شده است، لطفا برای تغییر موقعیت شغلی از دستور\"تغییر موقعیت\" استفاده کنید❌")
        else:
            #check for who the message is replied to
            title = ' '.join(theMessage)
            userID = message.reply_to_message.from_user.id
            userName = message.reply_to_message.from_user.username
            if len(title) > 16:
                await message.reply("موقعیت فرد نمی‌تواند بیشتر از 16 کاراکتر باشد❌")
            else:
                if userID not in positionTitles:
                    await app.promote_chat_member(message.chat.id, userID) # if user is promoted to admin by another user this will throw an exception
                    await app.set_administrator_title(message.chat.id, userID, title)
                    positionTitles[userID] = title
                    await message.reply(f"موقعیت موردنظر '{title}' برای کاربر @{userName} با موفقیت ثبت شد✅")
                else: 
                    await message.reply(f"موقعیت کاربر {userName} از قبل ذخیره شده است، لطفا برای تغییر موقعیت شغلی از دستور\"تغییر موقعیت\" استفاده کنید❌")

        dbm.updateUserPositionDict(message.chat.id, positionTitles)
    
    elif theMessage[0] == "تغییر" and theMessage[1] == "موقعیت":
        title = ""
        pt = dbm.getUserPositionDict(dbm.getChatID(message.chat.id))[0]
        positionTitles = ast.literal_eval(pt) if pt != "" else {}
        for i in range(2): theMessage.pop(0)
        titleMessage = ' '.join(theMessage)
        numberOfTags = [t for t in titleMessage if t.find("@") == 0]
        if len(numberOfTags) != 0:
            taggedPeople = []
            for entity in range(len(message.entities)):
                offset = message.entities[entity].offset
                taggedPeople.append(message.text[ offset : offset + message.entities[0].length])
            taggedPeopleID = await app.get_users(taggedPeople)
            for i in taggedPeople: theMessage.remove(i)
            title = " ".join(theMessage)
            if len(title) > 16:
                await message.reply("موقعیت فرد نمی‌تواند بیشتر از 16 کاراکتر باشد❌")
            else:
                for j, i in enumerate(taggedPeopleID):
                    if i.id in positionTitles:
                        await app.promote_chat_member(message.chat.id, i.id)
                        await app.set_administrator_title(message.chat.id, i.id, title)
                        positionTitles[i.id] = title
                        await message.reply(f"موقعیت موردنظر '{title}' برای کاربر {taggedPeople[j]} با موفقیت تغییر کرد✅")
                    else:
                        await message.reply(f"موقعیت شغلی‌ای برای کاربر موردنظر ثبت نشده است❌")
        else:
            #check for who the message is replied to
            title = ' '.join(theMessage)
            userID = message.reply_to_message.from_user.id
            userName = message.reply_to_message.from_user.username
            if len(title) > 16:
                await message.reply("موقعیت فرد نمی‌تواند بیشتر از 16 کاراکتر باشد❌")
            else:
                if userID not in positionTitles:
                    await app.promote_chat_member(message.chat.id, userID)
                    await app.set_administrator_title(message.chat.id, userID, title)
                    positionTitles[userID] = title
                    await message.reply(f"موقعیت موردنظر '{title}' برای کاربر {taggedPeople[j]} با موفقیت تغییر کرد✅")
                else:
                    await message.reply(f"موقعیت شغلی‌ای برای کاربر موردنظر ثبت نشده است❌")

        dbm.updateUserPositionDict(message.chat.id, positionTitles)
    
    elif theMessage[0] == "موقعیت" and theMessage[1] == "کاربران":
        pt = dbm.getUserPositionDict(dbm.getChatID(message.chat.id))[0]
        positionTitles = ast.literal_eval(pt) if pt != "" else {}
        users = positionTitles.keys()
        userInfos = await app.get_users(users)
        usernames = [i.username for i in userInfos]
        titles = positionTitles.values()
        userTitleText = "موقعیت های شغلی افراد تنظیم شده حاضر در گروه☘️: \n"
        for i, j in zip(usernames, titles): userTitleText += f"@{i}: {j}\n"
        await message.reply(userTitleText)

    if text == 'تاریخ' or text == 'date':
        response = requests.get('https://api.keybit.ir/time/')

        resp = response.json()

        time = resp['time24']['full']['en']
        day = resp['date']['day']['name']
        month = resp['date']['month']['name']
        year = resp['date']['year']['number']['en']
        days_left = resp['date']['year']['left']['days']['en']
        year_animal = resp['date']['year']['animal']
        leapyear = resp['date']['year']['leapyear']

        data = f'ساعت: {time} ⏰\n{day} {month} {year} 📅\n امسال {leapyear} است.\n\nروز های باقیمانده تا پایان سال: {days_left} ⏲\nحیوان سال: {year_animal}'

        await app.send_message(chat_id, data, reply_to_message_id = message_id)

    elif theMessage[0] == 'تقویم' or theMessage[0] == 'calendar':
        if theMessage[1:] != []: format = int(theMessage[1])
        else: format = 1

        await app.send_message(chat_id, f'<pre>{calendar(format)}</pre language="python">', parse_mode=enums.ParseMode.HTML, reply_to_message_id = message_id)

    elif text == 'ساعت' or text == 'زمان' or text == 'time':
        await app.send_message(chat_id, datetime.now().strftime('%H:%M:%S'), reply_to_message_id = message_id)

    elif text == 'مشخصات گروه' or text == 'info':
        chat = await app.get_chat(chat_id)
        await app.send_message(chat_id, f'نام گروه: {chat.title}\nآیدی عددی گروه: {chat.id}\nتعداد اعضا: {chat.members_count}\nلینک گروه: {chat.invite_link if not chat.invite_link == None else "لینک دعوت وجود ندارد"}', reply_to_message_id = message_id, disable_web_page_preview=True)

    elif text == 'پنل':
        await app.send_message(chat_id, "لطفا یکی از گزینه های زیر را انتخاب کنید", reply_to_message_id = message_id, reply_markup=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("تنظیمات", callback_data="setting-%i" % user_id),
                InlineKeyboardButton("راهنما", callback_data="help-%i" % user_id),
            ],
            [
                InlineKeyboardButton("ارتباط با ما", callback_data="contact_us-%i" % user_id),
                InlineKeyboardButton('بستن پنل', callback_data='close-%i' % user_id),
            ]
        ]
        ))

    elif text == 'ادمین ها':
        await app.send_message(chat_id, dbm.GetAllValues(chat_id)[1], reply_to_message_id = message_id)

    elif theMessage[0] == 'تعیین' and theMessage[1] == 'مالک' and theMessage[2] == 'تیم':
        final = ['Reserved']
        async for i in app.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
            if not i.user.is_self:
                if i.user.id != theMessage[-1]:
                    final.append(str(i.user.id))
        final[0] = theMessage[-1]
        dbm.AddAdmins(chat_id, ' '.join(final))
        await app.send_message(chat_id, f'مالک تیم با موفقیت تعیین شد.\nمالک: {final[0]}\n ادمین ها: {"   ".join(final[1:])}')

                
@app.on_callback_query()
async def answer(_, callback_query):
    chat_id = callback_query.message.chat.id
    data = callback_query.data.split('-')
    inline_id = int(callback_query.message.id)

    if data[0] == 'setting':
        await app.edit_message_text(chat_id, inline_id, 'به تنظیمات خوش آمدید.', reply_markup = settingsButtons(chat_id, data[1]))

    elif data[0] == 'help':
        await app.edit_message_text(chat_id, inline_id, 'به بخش راهنماخوش آمدید', reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('بازگشت', callback_data = f'back_to_main_menu-{data[1]}')
                ]
            ]
        ))

    elif data[0] == 'contact_us':
        await app.edit_message_text(chat_id, inline_id, 'به بخش درباره ما خوش آمدید.', reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton('بازگشت', callback_data = f'back_to_main_menu-{data[1]}')
                ]
            ]
        ))

    elif data[0] == 'close':
        await app.edit_message_text(chat_id, inline_id, 'پنل با موفقیت بسته شد✅')

    elif data[0] == 'back_to_main_menu':
        await app.edit_message_text(chat_id, inline_id, "لطفا یکی از گزینه های زیر را انتخاب کنید", reply_markup=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("تنظیمات", callback_data="setting-%s" % data[1]),
                InlineKeyboardButton("راهنما", callback_data="help-%s" % data[1]),
            ],
            [
                InlineKeyboardButton("ارتباط با ما", callback_data="contact_us-%s" % data[1]),
                InlineKeyboardButton('بستن پنل', callback_data='close-%s' % data[1]),
            ]
        ]
        ))

    elif data[0] in ['emoji', 'link', 'gif', 'sticker', 'picture', 'video', 'music', 'file', 'english', 'bad_words']:
        dbm.UpdateSettins(chat_id, data[0])
        await app.edit_message_text(chat_id, inline_id, 'به تنظیمات خوش آمدید.', reply_markup = settingsButtons(chat_id, data[1]))


# -------------------- Check settings to delete or keep messages ------------------------------ #
@app.on_message(filters.photo & filters.group)
async def photos(_, message):
    chat_id = message.chat.id
    message_id = message.id
    user_id = message.from_user.id
    if checkMessage(chat_id, 'picture'):
        await app.delete_messages(chat_id, message_id)

@app.on_message(filters.sticker & filters.group)
async def photos(_, message):
    chat_id = message.chat.id
    message_id = message.id
    user_id = message.from_user.id
    if checkMessage(chat_id, 'sticker'):
        await app.delete_messages(chat_id, message_id)

@app.on_message(filters.video & filters.group)
async def photos(_, message):
    chat_id = message.chat.id
    message_id = message.id
    user_id = message.from_user.id
    if checkMessage(chat_id, 'video'):
        await app.delete_messages(chat_id, message_id)

@app.on_message(filters.audio & filters.group)
async def photos(_, message):
    chat_id = message.chat.id
    message_id = message.id
    user_id = message.from_user.id
    if checkMessage(chat_id, 'music'):
        await app.delete_messages(chat_id, message_id)

@app.on_message(filters.document & filters.group)
async def photos(_, message):
    chat_id = message.chat.id
    message_id = message.id
    user_id = message.from_user.id
    if checkMessage(chat_id, 'file'):
        await app.delete_messages(chat_id, message_id)

@app.on_message(filters.animation & filters.group)
async def photos(_, message):
    chat_id = message.chat.id
    message_id = message.id
    user_id = message.from_user.id
    if checkMessage(chat_id, 'gif'):
        await app.delete_messages(chat_id, message_id)
# --------------------------------------------------------------------------------------------- #

if __name__ == "__main__":
    print('Bot is starting ...')
    app.run()  # Automatically start() and idle()
