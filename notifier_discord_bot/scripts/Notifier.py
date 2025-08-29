import discord
import datetime
from discord.ext import tasks


def convert_date_in_string_type_to_datetime_object(date_in_string_type: str) -> datetime:
    """Converts a date in string type into a datetime object and returns it

    Parameters
    ----------
    date_in_string_type: str
    It should be in "%d-%m-%Y" format"""

    if date_in_string_type:
        return datetime.datetime.strptime(date_in_string_type, "%d-%m-%Y")

    return None


class Notifier:
    """The class represents the Notifier discord bot"""

    def __init__(self, bot_token: str, bot_id: int, subscription_end_date: str, free_trial: bool,
                 list_of_the_user_ids_to_notify: list, list_of_the_channel_ids_to_be_notified_of: list,
                 list_of_the_category_ids_to_be_notified_of: list = None,
                 notify_of_service_commencement: bool = False):

        intents = discord.Intents.default()
        # intents.message_content = True

        self.notifier = discord.Bot(intents=intents)

        if notify_of_service_commencement:
            self.notify_users_and_dev_of_service_commencement()

        self.bot_id = bot_id
        self.subscription_end_date = convert_date_in_string_type_to_datetime_object(subscription_end_date)
        self.free_trial = free_trial
        self.list_of_the_user_ids_to_notify = list_of_the_user_ids_to_notify
        self.list_of_the_channel_ids_to_be_notified_of = list_of_the_channel_ids_to_be_notified_of
        self.list_of_the_category_ids_to_be_notified_of = list_of_the_category_ids_to_be_notified_of

        self.call_the_on_message_event()
        self.notify_the_users_of_remaining_subscription_period.start()
        self.notifier.run(bot_token)

    def notify_users_and_dev_of_service_commencement(self):
        """Notify users of the commencement of the service i.e. bot"""

        @self.notifier.event
        async def on_ready():

            miles_user_id = 1157609962420326421
            number_of_users = len(self.list_of_the_user_ids_to_notify)

            if self.free_trial:
                message_to_send_to_users = "Your free trial has now begun, congrats\n** **"
                message_to_send_to_channel = (f"The free trial for this bot has now begun"
                                              f"\n\nNumber of users = {number_of_users}\n** **")

            else:

                sub_end_date = self.subscription_end_date.strftime('%d %B %Y')

                message_to_send_to_users = (f"Your subscription has now been activated, congrats"
                                            f"\n\nSubscription ends: {sub_end_date}\n** **")

                message_to_send_to_channel = (f"The subscription for this bot has now been activated"
                                              f"\n\nNumber of users = {number_of_users}"
                                              f"\n\nSubscription ends: {sub_end_date}\n** **")

            user = await self.notifier.fetch_user(miles_user_id)
            await user.send(message_to_send_to_channel)
            await self.fetch_users_then_send_users_a_message(message_to_send_to_users)

    async def fetch_users_then_send_users_a_message(self, message_to_send: str):
        """Fetch users from the list then sends each of them a message"""

        for user_id in self.list_of_the_user_ids_to_notify:
            user = await self.notifier.fetch_user(user_id)
            await user.send(message_to_send)

    def decide_whether_to_notify_users_of_a_message(self, message: discord.Message) -> int | None:
        """Runs some conditional statement to decide whether to notify users and returns 1 if yes"""

        message_is_in_one_of_the_category_ids_to_be_notified_of = False
        message_is_in_one_of_the_channel_ids_to_be_notified_of = False
        message_is_not_from_one_of_the_user_ids_to_notify = False

        if self.list_of_the_category_ids_to_be_notified_of:
            for category_id in self.list_of_the_category_ids_to_be_notified_of:
                if message.channel.category_id == category_id:
                    message_is_in_one_of_the_category_ids_to_be_notified_of = True
                    break

        for channel_id in self.list_of_the_channel_ids_to_be_notified_of:
            if message.channel.id == channel_id:
                message_is_in_one_of_the_channel_ids_to_be_notified_of = True
                break

        for user_id in self.list_of_the_user_ids_to_notify:
            if message.author.id != user_id and message.author.id != self.bot_id:
                message_is_not_from_one_of_the_user_ids_to_notify = True
            else:
                message_is_not_from_one_of_the_user_ids_to_notify = False
                break

        if ((message_is_in_one_of_the_category_ids_to_be_notified_of
             or message_is_in_one_of_the_channel_ids_to_be_notified_of)
                and message_is_not_from_one_of_the_user_ids_to_notify):
            return 1

        return None

    def call_the_on_message_event(self):
        """Calls/defines the pycord on_message function"""

        @self.notifier.event
        async def on_message(message):
            if self.decide_whether_to_notify_users_of_a_message(message) == 1:
                message_to_send = (f"{message.author.global_name} just sent a message to {message.channel.name}"
                                   f"\n\n{message.jump_url}\n** **")
                await self.fetch_users_then_send_users_a_message(message_to_send)

    def calculate_the_remaining_subscription_period(self) -> int:
        """Calculates and returns the remaining subscription period"""

        current_date = datetime.datetime.now()
        remaining_subscription_period = self.subscription_end_date - current_date
        return int(remaining_subscription_period.days)

    @tasks.loop(hours=4)
    async def notify_the_users_of_remaining_subscription_period(self):
        """Notify users of the remaining subscription period"""

        warning_period = 7
        remaining_subscription_period = self.calculate_the_remaining_subscription_period()

        def construct_message_to_send(remaining_prd: str) -> str:
            """Construct and returns message based on free trial or paid sub and for different remaining periods"""

            if self.free_trial:
                msg_to_send = (f"Your free trial of this bot will end within {remaining_prd}"
                                   f"\n\nTo subscribe, contact the Developer\n** **")

            else:
                msg_to_send = (f"Your subscription i.e. the "
                                   f"service of this bot will end "
                                   f"within {remaining_prd} except you extend it"
                                   f"\n\nTo extend your subscription, contact the Developer\n** **")
            return msg_to_send

        if warning_period > remaining_subscription_period > 1:
            remaining_period = f"{remaining_subscription_period} days"
            message_to_send = construct_message_to_send(remaining_period)
            await self.fetch_users_then_send_users_a_message(message_to_send)

        elif remaining_subscription_period == 1:
            remaining_period = "48 hours"
            message_to_send = construct_message_to_send(remaining_period)
            await self.fetch_users_then_send_users_a_message(message_to_send)

        elif remaining_subscription_period == 0:
            remaining_period = "24 hours"
            message_to_send = construct_message_to_send(remaining_period)
            await self.fetch_users_then_send_users_a_message(message_to_send)

        elif remaining_subscription_period < 0:
            if self.free_trial:
                message_to_send = (f"Your free trial has now ended, the "
                                   f"service of this bot will be unavailable "
                                   f"within 6 hours except you subscribe"
                                   f"\n\nTo subscribe, contact the Developer\n** **")
            else:
                message_to_send = (f"Your subscription has now ended, the "
                                   f"service of this bot will be unavailable "
                                   f"within 6 hours except you renew your subscription"
                                   f"\n\nTo renew your subscription, contact the Developer\n** **")

            await self.fetch_users_then_send_users_a_message(message_to_send)
            await self.inform_the_dev_that_the_subscription_has_expired()

    async def inform_the_dev_that_the_subscription_has_expired(self):
        """Notify the Dev about the end of a subscription"""

        miles_user_id = 1157609962420326421
        number_of_users = len(self.list_of_the_user_ids_to_notify)

        if self.free_trial:
            message_to_send = f"The free trial for this bot has ended\n\nNumber of users = {number_of_users}\n** **"
        else:
            message_to_send = f"The subscription for this bot has ended\n\nNumber of users = {number_of_users}\n** **"

        user = await self.notifier.fetch_user(miles_user_id)
        await user.send(message_to_send)
