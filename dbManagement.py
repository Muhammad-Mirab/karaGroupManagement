import sqlite3


class dbManager:
    def __init__(self) -> None:
        self.con = sqlite3.connect("KaraGroups.db", check_same_thread = False)
        self.cur = self.con.cursor()

        # cur.execute("INSERT INTO groupSettings(groupID, welcomeMessage) VALUES ('1', 'سلام، همکار / دوست گرامی [یوزر جدید] به تیم [اسم گروه] خوش اومدی🌹 \n من ربات کارا هستم، یک ربات مدیریت گروه و پروژه از راه دور که میتونی از طریق دکمه زیر باهاش آشنا بشی و طرز کار باهاش رو یاد بگیری :)') ")
        # con.commit()
    def getChatID(self, groupId):
        chat_idDB = str(groupId).split("-")
        return f"Minus{chat_idDB[1]}" if chat_idDB[0] == "" else chat_idDB[0]
    def firstMessageEditID(self, chatID, messageID):
        self.cur.execute(f"INSERT or IGNORE INTO firstMessageQueue VALUES ('{chatID}', '{messageID}')")
        self.con.commit()
    def getFirstMessageEditID(self, chatID):
        self.cur.execute(f"SELECT messageID From firstMessageQueue WHERE chatID='{chatID}'")
        return [i[0] for i in self.cur.fetchall()]
    def removeFirstMessageEditID(self, chatID):
        self.cur.execute(f"DELETE FROM firstMessageQueue WHERE chatID = {chatID}")
        self.con.commit()
    def getAvailableGroupsID(self):
        self.cur.execute("SELECT groupID FROM groupSettings")
        return [i[0] for i in self.cur.fetchall()]
    def addToGroupSettings(self, groupID):
        defaultIsWelcomeEnabled = 1
        defaultWelcomeMessage = f'سلام، همکار / دوست گرامی [کاربر] به تیم خوش اومدی🌹 \n من ربات کارا هستم، یک ربات مدیریت گروه و پروژه از راه دور که میتونی از طریق دکمه زیر باهاش آشنا بشی و طرز کار باهاش رو یاد بگیری :)'
        self.cur.execute(f"INSERT or IGNORE INTO groupSettings VALUES ('{groupID}', {defaultIsWelcomeEnabled}, '{defaultWelcomeMessage}')")
        self.con.commit()
    def checkWetherGroupSettingIsSet(self, chatID, attribute):
        self.cur.execute(f"SELECT {attribute} FROM groupSettings WHERE groupID='{chatID}'")
        return [i[0] for i in self.cur.fetchall()]
# dbManagemerCls = dbManager()

# wetherWelcomeIsEnabled = dbManagemerCls.checkWetherGroupSettingIsSet(1, "isWelcomeEnabled")
# print(f"is welcome enabled: {wetherWelcomeIsEnabled}")