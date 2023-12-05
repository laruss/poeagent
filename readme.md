# PoeAgent Module Documentation

## Overview
The `PoeAgent` module is a comprehensive toolkit for managing bots and chats within a specified system. It encompasses functionalities to create, edit, delete, and retrieve information about bots, as well as to manage chats and messages.

## Installation
Install the `PoeAgent` module using the following command:
```
pip install poeagent
```

## Getting Started
Before using the module, create an instance of the `PoeAgent` class by providing an authentication token:

```python
from poeagent import PoeAgent

token = "YOUR_TOKEN"
agent = PoeAgent(token)
```

## Key Features
The module includes the following key functionalities:
- `get_available_bots()`: Retrieve a list of available bots.
- `create_bot()`, `edit_bot()`, `delete_bot()`: Manage bots.
- `get_bot_data()`: Get data about a specific bot.
- `get_chats_history()`, `get_one_chat_data()`: Manage chat history.
- `send_message()`, `delete_messages()`: Send and delete messages.
- Many other functions for bot and chat management.

## Usage Examples
### Creating a New Bot
```python
bot_data = agent.create_bot(
    handle="example_bot",
    prompt="Sample text",
    base_model="base_model_name"
)
```

### Retrieving Chat History
```python
chats_history = agent.get_chats_history(bot_name="example_bot")
```

### Sending a Message
```python
message_generator = agent.send_message(bot_name="example_bot", message="Hello, how are you?")
```

## Important Notes
- Ensure you have the correct permissions and token to use the API.
- The module requires a stable internet connection.

# Documentation of API Methods

## 1. `get_available_bots`
#### Description:
Get available bots for a user, including system and user bots.
#### Parameters:
- `limit` (int, default = 10): The maximum number of user bots to retrieve.
#### Returns:
- `List[OverviewBot]`: A list of OverviewBot objects.

## 2. `get_bot_landing_page_data`
#### Description:
Retrieve bot landing page data by bot name (handle).
#### Parameters:
- `bot_name` (str): The bot name (handle).
#### Returns:
- `LandingBotData`: A LandingBotData object.

## 3. `get_bot_data`
#### Description:
Get single bot data by chat code, bot name, or bot id. Data types include full bot data, only landing page data, or only right sidebar data.
#### Parameters:
- `chat_code` (str, optional): The chat code.
- `bot_name` (str, optional): The bot name (handle).
- `bot_id` (int, optional): The bot id.
- `data_type` (Literal['full', 'landing_page', 'right_sidebar'], default='full'): Type of data to retrieve.
#### Returns:
- `Union[BotWithPrompt, LandingBotData, FullBotData]`: Depending on the requested data type.

## 4. `get_available_creation_bots`
#### Description:
Get available bots for user creation.
#### Parameters:
None.
#### Returns:
- `List[BotsAllowedForUserCreationItem]`: A list of BotsAllowedForUserCreationItem objects.

## 5. `create_bot`
#### Description:
Create a bot with given parameters.
#### Parameters:
Multiple parameters including `handle`, `prompt`, `base_model`, etc.
#### Returns:
- `CreatedBot`: A CreatedBot object.

## 6. `edit_bot`
#### Description:
Edit a bot with given parameters.
#### Parameters:
Multiple parameters including `bot_id`, `handle`, `api_key`, etc.
#### Returns:
- `EditBotData`: An EditBotData object.

## 7. `delete_bot`
#### Description:
Delete a bot by its id.
#### Parameters:
- `bot_id` (int): The bot id to delete.
#### Returns:
- `DeletedBotData`: A DeletedBotData object.

## 8. `get_chats_history`
#### Description:
Get chat history for a specific bot or all bots.
#### Parameters:
- `bot_name` (str, optional): The bot name (handle) to get history for. If not provided, history for all bots is retrieved.
#### Returns:
- `List[ChatHistoryData]`: A list of ChatHistoryData objects.

## 9. `get_one_chat_data`
#### Description:
Get one chat data by chat code.
#### Parameters:
- `chat_code` (str): The chat code to get data for.
#### Returns:
- `OneChatDataResponse`: A OneChatDataResponse object.

## 10. `get_chat_messages`
#### Description:
Get chat messages by chat id.
#### Parameters:
- `chat_code` (str): The chat code to get messages from.
- `count` (int, default = 25): Number of messages to retrieve.
#### Returns:
- `List[MessageData]`: MessageData objects from oldest to newest.

## 11. `delete_chat`
#### Description:
Delete a chat by its id.
#### Parameters:
- `chat_id` (int): The chat id to delete.
#### Returns:
- `DeleteChatResponse`: A DeleteChatResponse object.

## 12. `delete_messages`
#### Description:
Delete messages by their ids.
#### Parameters:
- `chat_code` (str): The chat code to delete messages from.
- `message_ids` (int[]): Message ids to delete.
#### Returns:
- `DeleteMessagesResponse`: A DeleteMessagesResponse object.

## 13. `stop_message`
#### Description:
Stop message generation by id.
#### Parameters:
- `message_id` (int): The message id to stop.
- `text_length` (int): The text length to stop at.
#### Returns:
- `MessageCancelResponse`: A MessageCancelResponse object.

## 14. `send_message`
#### Description:
Send a message to the bot.
#### Parameters:
- `bot_name` (str): The bot name (handle) to send a message to.
- `message` (str): The message text to send.
- `chat_id` (int, optional): The chat id to send a message to. If not

 provided, a new chat is created.
#### Returns:
- `MessageGenerator`: A generator of WsMessage objects until a bot message is complete.

## 15. `regenerate_message`
#### Description:
Regenerate the last bot message in a chat.
#### Parameters:
- `chat_code` (str): The chat code to regenerate a message in.
#### Returns:
- `MessageGenerator`: A generator of WsMessage objects.

## 16. `get_settings`
#### Description:
Get settings data.
#### Parameters:
None.
#### Returns:
- `SettingsResponse`: A SettingsResponse object.
