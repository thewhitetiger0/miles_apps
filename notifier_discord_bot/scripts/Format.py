from Notifier import Notifier
from utils.env_utils import config

# bot token
bot_token = config.tester_bot_discord_token

# bot id
bot_id = 1287321658859720770

# user ids
morales_user_id = 1157609962420326421
list_of_user_ids_to_notify = [morales_user_id]

# subscription end date, It should be in "%d-%m-%Y" format
subscription_end_date = "01-01-2026"

# free trial? True or False
free_trial = False

# channel ids
morales_general_channel_id = 1268073645943820340
list_of_channel_ids_to_be_notified_of = [morales_general_channel_id]

# run notifier
run_notifier = Notifier(bot_token, bot_id, subscription_end_date, free_trial,
                        list_of_user_ids_to_notify, list_of_channel_ids_to_be_notified_of)
