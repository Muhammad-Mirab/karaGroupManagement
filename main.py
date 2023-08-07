# A project by Muhammad Mirab Br. ☘️
# Collabortors: Iliya Faramarzi
# Kara Group Management Bot
from pyrogram import Client, filters, enums
import dbManagement as dbManager
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, MessageEntity
import ast

dbm = dbManager.dbManager()

#Connect code to your bot
#app = Client('karaGroupManagement', api_id= your api id, api_hash= 'your api hash', bot_token= 'your bot token')
app = Client('karaGroupManagement')

# the stage where bot is added and becomes an admin
@app.on_message(filters.service)
async def services(client, message):
    chatID = dbm.getChatID(message.chat.id)
    # availableGroups is the variable in which the groups that the bot is already added to are listed
    availableGroups = dbm.getAvailableGroupsID()
    print(availableGroups)

    try:
        if message.chat.type != "private":
            new_member_status = message.new_chat_members[0]
            if new_member_status.is_self == True:
                # checks wheter it was previously added to this group or not 
                if chatID not in availableGroups:
                    print("hi")
                    dbm.addToGroupSettings(chatID)

                toBeEditedMessage = await app.send_message(message.chat.id, "ربات به گروه افزوده شد☘️\n\n» جهت آغاز فرآیند نصب و پیکربندی \nربات را ادمین کامل نمایید🌱")
                
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
    member = await app.get_chat_member(message.chat.id, "me")
    if message.chat.type == enums.ChatType.CHANNEL:
        if member.status == enums.ChatMemberStatus.ADMINISTRATOR and message.new_chat_member.privileges.can_post_messages:
            await app.send_message(message.new_chat_member.promoted_by.id, 'ربات با موفقیت در کانال ادمین شد')
        
        elif not message.new_chat_member.privileges.can_post_messages:
            await app.send_message(message.new_chat_member.promoted_by.id, 'لطفا ابتدا ربات را از کانال حذف و دوباره اضافه کنید و توجه کنید که باید هنگام اضافه کردن ربات به کانال دسترسی ارسال پیام را به ربات بدهید.')

    elif message.chat.type == enums.ChatType.GROUP or message.chat.type == enums.ChatType.SUPERGROUP:
        if member.status == enums.ChatMemberStatus.ADMINISTRATOR:
            final = ''
            
            # getting the admin users to display them in the message
            async for i in app.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
                if not i.user.is_self:
                    final += '[%s](tg://user?id=%i)\n' % (i.user.first_name, i.user.id)
                    
            await app.edit_message_text(message.chat.id, int(dbm.getFirstMessageEditID(dbm.getChatID(message.chat.id))[0]), 'ربات با موفقیت در گروه فعال شد.\n\n ادمین های شناسایی شده:\n%s' % final, reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton('ادامه پیکربندی', callback_data = 'Continue_config')
                            ],
                        ]))
            
            # removing the first message which was edited to admin confirmation
            dbm.removeFirstMessageEditID(dbm.getChatID(message.chat.id))

@app.on_message(filters.text & filters.group)
async def userTitles(client, message):
    theMessage = message.text.split(" ")
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
                    await app.promote_chat_member(message.chat.id, userID)
                    await app.set_administrator_title(message.chat.id, userID, title)
                    positionTitles[userID] = title
                    await message.reply(f"موقعیت موردنظر '{title}' برای کاربر @{userName} با موفقیت ثبت شد✅")
                else: 
                    await message.reply(f"موقعیت کاربر {userName} از قبل ذخیره شده است، لطفا برای تغییر موقعیت شغلی از دستور\"تغییر موقعیت\" استفاده کنید❌")

        dbm.updateUserPositionDict(message.chat.id, positionTitles)

@app.on_callback_query()
async def answer(client, callback_query):
    user_id = callback_query.from_user.id
    callback_data = callback_query.data
    
    admins = []
    async for admin in app.get_chat_members(callback_query.message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
        admins.append(admin.user.id)

    if callback_data == "Continue_config":
        if user_id in admins:
            await app.send_message(user_id, 'تست', reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton('افزودن ربات به کانال', url='https://t.me/curlymoderaotbot?startchannel=true')
                    ],
                ]
            ))
            await app.answer_callback_query(callback_query.id, 'برای ادامه پیکربندی به پیوی ربات مراجعه کنید.', show_alert=True)

        else:
            await app.answer_callback_query(callback_query.id, 'برای استفاده از این گزینه باید ادمین باشید.', show_alert=False)
    
# @app.on_message(filters.text & filters.private)
# async def echo(client, message):
#     await message.reply(message.text)
if __name__ == "__main__":
    app.run()  # Automatically start() and idle()