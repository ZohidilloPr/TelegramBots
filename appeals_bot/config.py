from decouple import config

# --- Secret information of developer ---

TOKEN = config("TOKEN")
DB_NAME = config("DB_NAME")
DB_PASSWORD = config("DB_PASSWORD")
DB_USER = config("DB_USER")
DB_HOST = config("DB_HOST")

# --- The end of Secret information of developer ---
id = "group id"
ADMINS = [id]

GROUP_CHAT_ID = [id]
RESPOND_GROUPS = [id]
GROUPS = {
    "fuqoro": id,
    "tadbirkor": id,
}   
