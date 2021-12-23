from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str
ADMINS = env.list("ADMINS")  # Тут будет список из админов
IP = env.str("ip")  # Тоже str, но для айпи адреса хоста