from pyrogram import Client, filters, enums
import dbManagement as dbManager


# Create a new Client instance
with open("credentials.txt", "r") as file:
    cred = file.readlines()
    app = Client("karaGroupManagement", api_hash=cred[0], api_id=int(cred[1]), bot_token=cred[2])
dbm = dbManager.dbManager()

@app.on_message(filters.service)
async def services(client, message):
    chatID = dbm.getChatID(message.chat.id)
    availableGroups = dbm.getAvailableGroupsID()

    try:
        if message.chat.type != "private":
            new_member_status = message.new_chat_members[0]
            if new_member_status.is_self == True:
                if chatID not in availableGroups:
                    dbm.addToGroupSettings(chatID)
                toBeEditedMessage = await app.send_message(
                    message.chat.id, "ربات به گروه افزوده شد☘️\n\n» جهت آغاز فرآیند نصب و پیکربندی \nربات را ادمین کامل نمایید🌱")
                dbm.firstMessageEditID(chatID, toBeEditedMessage.id)
    except:
        pass


    try:
        new_member_status = message.new_chat_members[0]
    except:
        pass

    wetherWelcomeIsEnabled = dbm.checkWetherGroupSettingIsSet(chatID, "isWelcomeEnabled")
    if wetherWelcomeIsEnabled[0] == 1:
        try:
            if new_member_status.is_self != True:
                welcomeMessage = dbm.checkWetherGroupSettingIsSet(chatID, "welcomeMessage")
                new_member = [u.mention for u in message.new_chat_members]
                welcomeMessage = welcomeMessage[0].replace(
                    "[کاربر]", f"{new_member[0]}")
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
    print(member.status)
    if member.status == enums.ChatMemberStatus.ADMINISTRATOR:
        print("jksdnksjn")
        final = ''

        async for i in app.get_chat_members(message.chat.id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
            if not i.user.is_self:
                final += '[%s](tg://user?id=%i)\n' % (i.user.first_name, i.user.id)
     
        await app.edit_message_text(message.chat.id, int(dbm.getFirstMessageEditID(dbm.getChatID(message.chat.id))[0]), 'ربات با موفقیت در گروه فعال شد.\n\n ادمین های شناسایی شده:\n%s' % final)
        dbm.removeFirstMessageEditID(message.chat.id)
@app.on_message(filters.text & filters.private)
async def echo(client, message):
    await message.reply(message.text)

app.run()  # Automatically start() and idle()