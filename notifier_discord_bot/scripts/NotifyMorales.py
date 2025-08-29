import discord
from utils.env_utils import config


class NotifyMorales:
    """The class represents the NotifyMorales discord bot"""

    def __init__(self):

        token = config.notifymorales_bot_discord_token

        intents = discord.Intents.default()
        intents.message_content = True

        self.notify_morales = discord.Bot(intents=intents)

        self.testing1_server_id = 1284505035614588982
        self.testing1_general_channel_id = 1284505036348461078

        self.morales_user_id = 1157609962420326421
        self.notify_morales_user_id = 1284515457952645140
        self.morales_alert_channel_id = 1285622390344126464

        self.ftm_general_chat_channel_id = 1248283836651933788
        self.ftm_trading_ideas_channel_id = 1248283836651933789
        self.ftm_suggestions_channel_id = 1248283837105049702
        self.ftm_scammer_alert_channel_id = 1248283837105049705
        self.ftm_funded_chat_channel_id = 1248283837528805470
        self.ftm_funded_role_applications_channel_id = 1248283838011015287

        self.call_on_message_event()
        self.notify_morales.run(token)

    def decide_whether_to_notify_morales_about_message(self, message) -> int:
        """Runs some conditional statement to decide whether to notify morales and returns 1 if yes"""

        message_channel_is_general_chat = message.channel.id == self.ftm_general_chat_channel_id
        message_channel_is_trading_ideas = message.channel.id == self.ftm_trading_ideas_channel_id
        message_channel_is_suggestions = message.channel.id == self.ftm_suggestions_channel_id
        message_channel_is_scammer_alert = message.channel.id == self.ftm_scammer_alert_channel_id
        message_channel_is_funded_chat = message.channel.id == self.ftm_funded_chat_channel_id
        message_channel_is_funded_role_applications = message.channel.id == self.ftm_funded_role_applications_channel_id

        message_channel_is_one_of_the_six = (message_channel_is_general_chat or message_channel_is_trading_ideas
                                             or message_channel_is_suggestions or message_channel_is_scammer_alert
                                             or message_channel_is_funded_chat
                                             or message_channel_is_funded_role_applications)

        message_author_is_not_morales = message.author.id != self.morales_user_id
        message_author_is_not_notify_morales = message.author.id != self.notify_morales_user_id
        message_author_is_not_any_of_the_two = message_author_is_not_morales and message_author_is_not_notify_morales

        if message_channel_is_one_of_the_six and message_author_is_not_any_of_the_two:
            return 1

    def call_on_message_event(self):
        """Calls/defines the pycord on_message function"""

        @self.notify_morales.event
        async def on_message(message):

            # fetch alert_channel discord object
            alert_channel = await self.notify_morales.fetch_channel(self.morales_alert_channel_id)

            if self.decide_whether_to_notify_morales_about_message(message) == 1:
                await alert_channel.send(f'{message.author.global_name} sent a message to {message.channel.name}'
                                         f'\n\n"{message.content}"\n\n{message.jump_url}\n** **')


run_app = NotifyMorales()
