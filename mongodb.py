from pymongo import MongoClient

# Verbindung zur MongoDB-Instanz herstellen
client = MongoClient('localhost', 27017)

# Datenbank und Collections holen
btsDB = client["BTS"]
guilds = btsDB["guilds"]

# Guild Metadata

# add new or update Guild Setup
def saveGuild(guild_options):
    guilds.update_one({"guild_id": guild_options["guild_id"]}, {"$set": guild_options}, upsert=True)

# find guild options
def findGuildOptions(guild_id):
    guild_options = guilds.find_one({"guild_id" : guild_id})
    if guild_options:
        return guild_options
    return {"guild_id" : guild_id, "language" : "english"}