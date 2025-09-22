"""This module contains the MoralesServer class that defines Discord server configuration.

The module provides constants and methods for accessing Discord channel IDs used in the Morales server,
including general channel, alert channels, sheet channels.
"""

from l1_infra.utils.class_utils.frozen_type import FrozenType


class MoralesServer(metaclass=FrozenType):
    """Configuration class containing Discord channel IDs for the Morales server.

    This class uses a frozen type metaclass to prevent modifications after initialization.
    It contains channel IDs for the different channels within the server.

    Attributes:
        server_id (int): The Discord server ID
        general_channel_id (int): Main general communication channel
        error_alert_channel_id (int): Channel for error notifications
        ftm_message_alert_channel_id (int): Channel for FTM message alerts
        sp_sheet_texts_channel_id (int): Channel for SP sheet texts
        ig_sheet_texts_channel_id (int): Channel for IG sheet texts
    """

    server_id = 1268073645477986355

    # top level
    general_channel_id = 1268073645943820340

    # alerts
    error_alert_channel_id = 1384145306983207004
    ftm_message_alert_channel_id = 1285622390344126464

    # sheets
    sp_sheet_texts_channel_id = 1383881524394332270
    ig_sheet_texts_channel_id = 1383881563561001091

    @classmethod
    def return_morales_server_channels(cls) -> list[int]:
        """Return a list of all FTM bot master user IDs."""
        return [
            value
            for name, value in cls.__dict__.items()
            if name.endswith("_channel_id")
        ]

    @classmethod
    def return_morales_server_channels_dict(cls) -> dict[str, int]:
        """Return a dictionary mapping bot master names to their user IDs."""
        return {
            name: value
            for name, value in cls.__dict__.items()
            if name.endswith("_channel_id")
        }
