import sqlite3


class dbManager:
    def __init__(self) -> None:
        self.con = sqlite3.connect("KaraGroups.db", check_same_thread = False)
        self.cur = self.con.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS groupSettings(groupID STRING, isWelcomeEnabled STRING, welcomeMessage STRING)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS firstMessageQueue(chatID STRING, messageID STRING)")
        # self.cur.execute("INSERT OR IGNORE INTO groupSettings(groupID, welcomeMessage) VALUES ('1', 'سلام، همکار / دوست گرامی [یوزر جدید] به تیم [اسم گروه] خوش اومدی🌹 \n من ربات کارا هستم، یک ربات مدیریت گروه و پروژه از راه دور که میتونی از طریق دکمه زیر باهاش آشنا بشی و طرز کار باهاش رو یاد بگیری :)') ")
        # self.con.commit()
    # converts numeral chat id into sth the database can handle
    def getChatID(self, groupId):
        chat_idDB = str(groupId).split("-")
        # checks if the chat id value is negative if not will return the exact same thing
        return f"Minus{chat_idDB[1]}" if chat_idDB[0] == "" else chat_idDB[0]
    
    # adds the bot's first message to firstMessageQueue table in the db
    def firstMessageEditID(self, chatID, messageID):
        self.cur.execute(f"INSERT or IGNORE INTO firstMessageQueue VALUES ('{chatID}', '{messageID}')")
        self.con.commit()

    # returns the message id of the first message using the group's chat id
    def getFirstMessageEditID(self, chatID):
        self.cur.execute(f"SELECT messageID From firstMessageQueue WHERE chatID='{chatID}'")
        return [i[0] for i in self.cur.fetchall()]
    
    # it removes the first message's entry in database after editing the message and confirming the admin process
    def removeFirstMessageEditID(self, chatID):
        self.cur.execute(f"DELETE FROM firstMessageQueue WHERE chatID = {chatID}")
        self.con.commit()

    # return a list of the groups the bot is active in
    def getAvailableGroupsID(self):
        self.cur.execute("SELECT groupID FROM groupSettings")
        return [i[0] for i in self.cur.fetchall()]
    
    # adds the group into groupSettings table which will hold all the admin related settings of the group
    def addToGroupSettings(self, groupID):
        defaultIsWelcomeEnabled = 1
        defaultWelcomeMessage = f'سلام، همکار / دوست گرامی [کاربر] به تیم خوش اومدی🌹 \n من ربات کارا هستم، یک ربات مدیریت گروه و پروژه از راه دور که میتونی از طریق دکمه زیر باهاش آشنا بشی و طرز کار باهاش رو یاد بگیری :)'
        self.cur.execute(f"INSERT or IGNORE INTO groupSettings VALUES ('{groupID}', {defaultIsWelcomeEnabled}, '{defaultWelcomeMessage}')")
        self.con.commit()

    # using the chatID and attribute(which is the name of the value in db e.g. "isWelcomeEnabled") will check if the admin has disabled a feature
    def checkWetherGroupSettingIsSet(self, chatID, attribute):
        self.cur.execute(f"SELECT {attribute} FROM groupSettings WHERE groupID='{chatID}'")
        return [i[0] for i in self.cur.fetchall()]
