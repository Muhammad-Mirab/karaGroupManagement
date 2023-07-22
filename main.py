# A project by Muhammad Mirab Br. ☘️
# Collabortors: Iliya Faramarzi
# Kara Group Management Bot
from pyrogram import Client, filters, enums
import dbManagement as dbManager
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

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

    try:
        if message.chat.type != "private":
            new_member_status = message.new_chat_members[0]
            if new_member_status.is_self == True:
                # checks wheter it was previously added to this group or not 
                if chatID not in availableGroups:
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
                                InlineKeyboardButton('ادامه پیکربندی', url = f'https://t.me/curlymoderaotbot?start=Continue_config_{message.chat.id}')
                            ],
                        ]))
            
            # removing the first message which was edited to admin confirmation
            dbm.removeFirstMessageEditID(dbm.getChatID(message.chat.id))

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



if __name__ == "__main__":
    print('Bot is starting ...')
    app.run()  # Automatically start() and idle()