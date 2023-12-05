import json
import logging
import random
import re
import secrets
import string
import queue
from typing import List, Literal, Union, Generator, Optional

from .api_session import ApiSession
from .models.available_bots_data import GetBotDataResponse, OverviewBot
from .models.available_creation_bots_data import AvailableCreationBotsResponse, BotsAllowedForUserCreationItem
from .models.bot import BotWithPrompt, FullBotData
from .models.bot_data import ResponseByChatCode, ResponseByBotName, ResponseByBotId
from .models.bot_landing_page_data import GetBotLandingPageDataResponse, LandingBotData
from .models.chat_messages_data import ChatMessagesResponse, MessageData
from .models.chats_history_data import ChatsHistoryResponse, ChatHistoryData
from .models.chats_history_filtered_data import ChatHistoryFilteredResponse
from .models.create_bot_data import CreateBotResponse, CreatedBot
from .models.delete_bot_data import DeleteBotResponse, DeletedBotData
from .models.delete_chat_data import DeleteChatResponse
from .models.delete_messages_data import DeleteMessagesResponse
from .models.edit_bot_data import EditBotResponse, EditBotData
from .models.message_cancel_data import MessageCancelResponse
from .models.one_chat_data import OneChatDataResponse
from .models.regenerate_message_data import RegenerateMessageResponse
from .models.send_message_data import SendMessageResponse, LastMessage, MessageEdgeCreate
from .models.settings_data import SettingsResponse
from .models.ws_message import WsMessage
from .queries import Queries
from .ws_session import WsSession

logger = logging.getLogger(__name__)

MessageGenerator = Generator[WsMessage, None, None]


class PoeAgent:
    def __init__(self, token: str, retries: int = 10, reconnect_on_error: bool = True):
        self.token = token
        self.retries = retries
        self.reconnect_on_error = reconnect_on_error
        self.tried_retries = 0
        self.ws_session: WsSession = None
        self.api_session: ApiSession = None

        self._active_messages = dict()
        self._message_queues = dict()

        self.connect()

    def __del__(self):
        self.disconnect()

    def _on_connect(self):
        self.tried_retries = 0

    def _on_message(self, message):
        if not message.get("messages"):
            return
        for message_str in message["messages"]:
            message_data = json.loads(message_str)
            if message_data["message_type"] != "subscriptionUpdate" or \
                    (message_data["payload"]["subscription_name"] != "messageAdded"):
                continue
            message = message_data["payload"]["data"]["messageAdded"]

            copied_dict = self._active_messages.copy()
            for key, value in copied_dict.items():
                if value == message["messageId"] and key in self._message_queues:
                    self._message_queues[key].put(message)
                    return

                elif key != "pending" and value is None and message["state"] != "complete":
                    self._active_messages[key] = message["messageId"]
                    self._message_queues[key].put(message)
                    return

    def _on_error(self):
        self.tried_retries += 1
        if self.tried_retries >= self.retries:
            raise ConnectionError("Max retries exceeded")
        self.connect()

    @property
    def _ws_url(self):
        ws_domain = f"tch{random.randint(1, int(1e6))}"[:9]
        td = self.api_session.tchannel_data
        return f"ws://{ws_domain}.tch.{td.baseHost}/up/{td.boxName}/updates" \
               f"?min_seq={td.minSeq}&channel={td.channel}&hash={td.channelHash}"

    @property
    def is_connected(self):
        return self.ws_session.is_connected

    def send_query(self, query: Queries, variables: dict = None, base_url: str = None, **kwargs):
        if self.api_session.js.requests_params.reload_if_needed():
            logger.info("Requests params reloaded, reconnecting with new params")
            self.connect(True, True)

        send = lambda: self.api_session.send_query(query, variables, base_url, **kwargs)
        try:
            response = send()
        except ConnectionError as e:
            if not self.reconnect_on_error:
                raise e
            logger.warning("Connection error, reconnecting, updating requests params and retrying")
            self.connect(True, True)
            response = send()

        if errors := response.get("errors"):
            raise ValueError(f"Query '{query}' failed with errors: {errors}")

        return response

    def connect(self, reconnect: bool = False, update_requests_params: bool = False):
        if not reconnect:
            if (s := self.ws_session) and s.is_connected:
                return

        if self.ws_session:
            self.ws_session.stop()
        if self.api_session:
            self.api_session.close()

        self.api_session = ApiSession(token=self.token)
        if update_requests_params:
            self.api_session.reload_request_params()
        self.subscribe_to_mutations()
        self.ws_session = WsSession(url=self._ws_url,
                                    on_message_callback=self._on_message,
                                    on_error_callback=self._on_error,
                                    on_connect_callback=self._on_connect)

    def reconnect_to_ws(self):
        self.ws_session.stop()
        self.ws_session = WsSession(url=self._ws_url,
                                    on_message_callback=self._on_message,
                                    on_error_callback=self._on_error,
                                    on_connect_callback=self._on_connect)

    def disconnect(self):
        if (ws := self.ws_session) and ws.is_connected:
            self.ws_session.stop()
            self.api_session.close()

    def __get_subscription_data(self) -> List[dict]:
        req_params = self.api_session.requests_params
        subscriptions = filter(lambda x: x.operationKind == "subscription", req_params.values())
        logger.debug(f"Subscriptions: {subscriptions}")
        return [
            dict(
                query=None,
                queryHash=sub.id,
                subscriptionName=sub.name.replace("subscriptions_", "").replace("_Subscription", "")
            ) for sub in subscriptions
        ]

    def subscribe_to_mutations(self):
        """
        subscribe to mutations by means of websocket

        :return: none
        """
        logger.info("Subscribing to mutations")

        variables = dict(subscriptions=self.__get_subscription_data())
        res = self.send_query(Queries.subscription, variables=variables)

        logger.debug(f"Sent subscription request: {variables}")
        logger.info(f"Got subscription response: {res}")
        logger.info("Subscribed to mutations successfully")

    def get_available_bots(self, limit: int = 10) -> List[OverviewBot]:
        """
        get available for user bots (system bots + user bots)

        :param limit: limit of user bots to get
        :return: a list of OverviewBot objects
        """
        logger.info(f"Getting users bots, limit: {limit}")

        response = self.send_query(Queries.bot_selector)
        model = GetBotDataResponse(**response)
        connection = model.data.viewer.availableBotsConnection
        system_bots = [edge.node for edge in connection.edges]
        cursor = connection.pageInfo.endCursor

        response = self.send_query(Queries.available_bots, variables=dict(cursor=cursor, limit=limit))
        model = GetBotDataResponse(**response)
        connection = model.data.viewer.availableBotsConnection
        user_bots = [edge.node for edge in connection.edges]

        logger.info(f"Got {len(user_bots)} user bots and {len(system_bots)} system bots")

        return user_bots + system_bots

    def get_bot_landing_page_data(self, bot_name: str) -> LandingBotData:
        """
        get bot landing page data by bot name (handle)

        :param bot_name: bot name (handle), string
        :return: LandingBotData object
        """
        variables = dict(botHandle=bot_name)

        response = self.send_query(Queries.handle_landing_bot_page, variables=variables)
        model = GetBotLandingPageDataResponse(**response)

        return model.data.bot

    def get_bot_data(self,
                     chat_code: str = None,
                     bot_name: str = None,
                     bot_id: int = None,
                     data_type: Literal['full', 'landing_page', 'right_sidebar'] = 'full'
                     ) -> Union[BotWithPrompt, LandingBotData, FullBotData]:
        """
        get single bot data by chat code, bot name or bot id
        data types:
            - full: full bot data, including prompt, landing page and right sidebar
            - landing_page: only landing page data (w/o prompt)
            - right_side_bar: only right sidebar data (w/o landing page data, such as default bot)

        :param chat_code: chat code, string
        :param bot_name: bot name (handle), string
        :param bot_id: bot id, int
        :param data_type: type of data to get, can be 'full', 'landing_page', 'right_sidebar'
        :return: BotWithPrompt object
        """
        if (bool(chat_code) + bool(bot_name) + bool(bot_id)) != 1:
            raise ValueError("Only one of chat_code, bot_name, bot_id, post_id can be used")

        logger.info(f"Getting bot data, {chat_code=}, {bot_name=}, {bot_id=}")

        variables = dict(
            botId=bot_id or 0,
            botName=bot_name or "",
            chatCode=chat_code or "",
            postId=0,
            shareCode="",
            useBotId=bool(bot_id),
            useBotName=bool(bot_name),
            useChat=bool(chat_code),
            usePostId=False,
            useShareCode=False
        )

        response = self.send_query(Queries.layout_right_sidebar, variables=variables)
        logger.info(f"Got response: {response}")

        if rs_data := response.get("data"):
            if not rs_data.get("bot") and not rs_data.get("botById"):
                raise ValueError("Bot not found")

        right_sidebar_data = None
        if chat_code:
            right_sidebar_data = ResponseByChatCode(**response).data.chatOfCode.defaultBotObject
        elif bot_name:
            right_sidebar_data = ResponseByBotName(**response).data.bot
        elif bot_id:
            right_sidebar_data = ResponseByBotId(**response).data.botById

        if data_type == 'right_sidebar':
            return right_sidebar_data

        landing_page_data = self.get_bot_landing_page_data(bot_name=bot_name or right_sidebar_data.handle)

        if data_type == 'landing_page':
            return landing_page_data

        full_bot_data = right_sidebar_data.model_dump(by_alias=True)
        full_bot_data.update(landing_page_data.model_dump(by_alias=True))

        return FullBotData(**full_bot_data)

    def get_available_creation_bots(self) -> List[BotsAllowedForUserCreationItem]:
        """
        get available bots for user creation

        :return: A list of BotsAllowedForUserCreationItem objects
        """
        logger.info("Getting available creation bots")
        variables = dict(messageId=None)
        response = self.send_query(Queries.create_bot_index_page, variables=variables)
        model = AvailableCreationBotsResponse(**response)

        return model.data.viewer.botsAllowedForUserCreation

    @staticmethod
    def _validate_handle(handle):
        pattern = re.compile(r"^[A-Za-z0-9_-]{4,20}$")
        if not bool(pattern.match(handle)):
            raise ValueError("Invalid handle, must be 4-20 characters, alphanumeric, underscores and dashes only")

    @staticmethod
    def _strip_handle(handle):
        return handle.lower().replace(' ', '').replace('_', '').replace('-', '')

    @staticmethod
    def _generate_nonce(length: int = 16):
        return "".join(secrets.choice(string.ascii_letters + string.digits) for _ in range(length))

    def create_bot(self,
                   handle: str,
                   prompt: str,
                   base_model: str,
                   display_name=None,
                   description: str = "",
                   intro_message: str = "",
                   api_key: str = None,
                   custom_message_limit: int = None,
                   is_api_bot: bool = False,
                   api_url: str = None,
                   is_prompt_public: bool = True,
                   profile_picture_url: str = None,
                   has_markdown_rendering: bool = True,
                   has_suggested_replies: bool = False,
                   is_private: bool = False,
                   temperature: float = None,
                   ) -> CreatedBot:
        """
        create a bot with given params

        :param handle: bot handle (name), 4-20 characters, alphanumeric, underscores and dashes only
        :param prompt: prompt for bot, not empty string
        :param base_model: base model for bot, you can get available models from PoeApi.get_available_creation_bots
        :param display_name: name to be displayed in chat, can be none
        :param description: description for bot, can be empty string
        :param intro_message: intro message for bot, can be empty string
        :param api_key: api key for bot, can be none
        :param custom_message_limit: custom message limit for bot, can be none
        :param is_api_bot: is bot an api bot, can be none
        :param api_url: api url for bot, can be none
        :param is_prompt_public: is prompt public, default True
        :param profile_picture_url: profile picture url for bot, can be none
        :param has_markdown_rendering: if bot has markdown rendering, default True
        :param has_suggested_replies: if bot has suggested replies, default False
        :param is_private: if bot is private, default False
        :param temperature: temperature for bot, can be none
        :return: CreatedBot object
        """
        logger.info(f"Creating bot {handle} with prompt {prompt}")
        self._validate_handle(handle)
        available_bots = self.get_available_creation_bots()

        if not prompt:
            raise ValueError("Prompt is required and cannot be empty string")

        if base_model not in (base_models := [bot.model for bot in available_bots]):
            raise ValueError(f"Invalid base model {base_model}. Please choose from {base_models}")

        base_bot: BotsAllowedForUserCreationItem = next(filter(lambda x: x.model == base_model, available_bots))

        variables = dict(
            api_key=api_key,
            api_url=api_url,
            baseBotId=base_bot.botId,
            customMessageLimit=custom_message_limit,
            description=description,
            displayName=display_name,
            handle=handle,
            hasMarkdownRendering=has_markdown_rendering,
            hasSuggestedReplies=has_suggested_replies,
            introduction=intro_message,
            isApiBot=is_api_bot,
            isPrivateBot=is_private,
            isPromptPublic=is_prompt_public,
            knowledgeSourceIds=[],
            messagePriceCc=None,
            model=base_model,
            profilePictureUrl=profile_picture_url,
            prompt=prompt,
            shouldCiteSources=False,
            temperature=temperature,
        )
        response = self.send_query(Queries.create_bot_main, variables=variables)
        logger.info(f"Got response: {response}")

        if rs_data := response.get("data"):
            if rs_bot_create := rs_data.get("poeBotCreate"):
                if rs_bot_create.get('status') != "success":
                    raise ValueError(f"Bot creation failed: {rs_bot_create.get('statusMessage')}")

        model = CreateBotResponse(**response)

        return model.data.poeBotCreate.bot

    def edit_bot(self,
                 bot_id: int,
                 handle: str = None,
                 api_key: str = None,
                 api_url: str = None,
                 base_model: str = None,
                 custom_message_limit: int = None,
                 description: str = None,
                 display_name: str = None,
                 has_markdown_rendering: bool = None,
                 has_suggested_replies: bool = None,
                 intro_message: str = None,
                 is_private: bool = None,
                 is_prompt_public: bool = None,
                 profile_picture_url: str = None,
                 prompt: str = None,
                 temperature: float = None
                 ) -> EditBotData:
        """
        edit bot with given params
        any additional params will be ignored if not provided

        :param bot_id: bot id to edit
        :param handle: a handle to set (bot name)
        :param api_key: api key for bot
        :param api_url: api url for bot
        :param base_model: base model for bot (you can get available models from PoeApi.get_available_creation_bots)
        :param custom_message_limit: custom message limit for bot, int
        :param description: description for bot
        :param display_name: display name for bot
        :param has_markdown_rendering: if bot has markdown rendering (default True)
        :param has_suggested_replies: if bot has suggested replies (default False)
        :param intro_message: intro message for bot
        :param is_private: if bot is private (will be set from bot data if not provided)
        :param is_prompt_public: if bot prompt is public (default False)
        :param profile_picture_url: profile picture url for bot
        :param prompt: prompt for bot, not empty string
        :param temperature: temperature for bot, 0.0 - 1.0
        :return: EditBotData object
        """
        logger.info(f"Editing bot {bot_id}")
        base_bot_id = None
        if handle:
            self._validate_handle(handle)

        creation_bots = self.get_available_creation_bots()
        if base_model:
            if base_model not in (base_models := [bot.model for bot in creation_bots]):
                raise ValueError(f"Invalid base model {base_model}. Please choose from {base_models}")
            base_bot: BotsAllowedForUserCreationItem = next(filter(lambda x: x.model == base_model, creation_bots))
            base_bot_id = base_bot.botId

        if prompt is not None and not prompt:
            raise ValueError("Prompt cannot be empty string")

        bot: FullBotData = self.get_bot_data(bot_id=bot_id)
        creation_bot: BotsAllowedForUserCreationItem = next(filter(lambda x: x.model == bot.model, creation_bots))

        variables = dict(
            apiKey=api_key,
            apiUrl=api_url,
            baseBot=base_model or bot.model,
            baseBotId=base_bot_id or creation_bot.botId,
            botId=bot_id,
            customMessageLimit=custom_message_limit,
            description=description or bot.description,
            displayName=display_name or bot.displayName,
            handle=handle or bot.handle,
            hasMarkdownRendering=has_markdown_rendering or True,
            hasSuggestedReplies=has_suggested_replies or False,
            introduction=intro_message or bot.introduction,
            isPrivateBot=is_private or bot.isPrivateBot,
            isPromptPublic=bool(is_prompt_public),
            knowledgeSourceIdsToAdd=[],
            knowledgeSourceIdsToRemove=[],
            messagePriceCc=None,
            profilePictureUrl=profile_picture_url,
            prompt=prompt or bot.promptPlaintext,
            shouldCiteSources=False,
            temperature=temperature,
        )

        response = self.send_query(Queries.edit_bot_main, variables=variables)
        model = EditBotResponse(**response)

        return model.data.poeBotEdit.bot

    def delete_bot(self, bot_id: int) -> DeletedBotData:
        """
        delete bot by id

        :param bot_id: bot id to delete, int
        :return: DeletedBotData object
        """
        logger.info(f"Deleting bot {bot_id}")
        variables = dict(botId=bot_id)

        response = self.send_query(Queries.delete_bot, variables=variables)
        model = DeleteBotResponse(**response)

        return model.data.poeBotDelete.bot

    def get_chats_history(self, bot_name: str = None) -> List[ChatHistoryData]:
        """
        get chats history for bot or all bots

        :param bot_name: bot name (a.k.a. handle) to get history for, if not provided, will get history for all bots
        :return: a list of ChatHistoryData objects
        """
        logger.info(f"Getting chats history, {bot_name=}")
        variables = dict(handle=bot_name or "", useBot=bool(bot_name))

        response = self.send_query(Queries.chat_history_page, variables=variables)
        model = ChatHistoryFilteredResponse(**response) if bot_name else ChatsHistoryResponse(**response)
        chats = model.data.filteredChats if bot_name else model.data.viewer.chats

        if chats.pageInfo.hasNextPage:
            logger.warning("! There are more chats to get, but pagination is not implemented yet !")

        return [edge.node for edge in chats.edges]

    def get_one_chat_data(self, chat_code: str) -> OneChatDataResponse:
        """
        get one chat data by chat code

        :param chat_code: chat code to get data for
        :return: OneChatDataResponse object
        """
        logger.info(f"Getting one chat data, {chat_code=}")
        variables = dict(chatCode=chat_code)
        response = self.send_query(Queries.chat_page, variables=variables)
        return OneChatDataResponse(**response)

    def get_chat_messages(self, chat_code: str, count: int = 25) -> List[MessageData]:
        """
        get chat messages by chat id (from oldest to newest)

        :param chat_code: chat code to get messages from, string
        :param count: count of messages to get, int
        :return: MessageData objects from oldest to newest
        """
        logger.info(f"Getting chat messages, {chat_code=}, {count=}")
        count = count or 100

        chat_data = self.get_one_chat_data(chat_code=chat_code)
        chat_data = chat_data.data.chatOfCode
        chat_id = chat_data.id
        last_messages_nodes = chat_data.messagesConnection.edges
        if count <= len(last_messages_nodes):
            return [edge.node for edge in last_messages_nodes[-count:]]
        cursor = last_messages_nodes[0].cursor
        last_messages = [edge.node for edge in last_messages_nodes]
        count -= len(last_messages_nodes)

        variables = dict(count=count, id=chat_id, cursor=cursor)
        response = self.send_query(Queries.chat_list_pagination, variables=variables)

        if response.get("data") and not response.get("data").get("node"):
            logger.warning(f"Chat node with id {chat_id} not found, {response=}")
            return [] + last_messages

        model = ChatMessagesResponse(**response)
        messages = [edge.node for edge in model.data.node.messagesConnection.edges] + last_messages

        return messages

    def delete_chat(self, chat_id: int) -> DeleteChatResponse:
        """
        delete chat by id

        :param chat_id: chat id to delete, int
        :return: DeleteChatResponse object
        """
        logger.info(f"Deleting chat {chat_id=}")
        variables = dict(chatId=chat_id)
        response = self.send_query(Queries.delete_chat, variables=variables)
        return DeleteChatResponse(**response)

    def delete_messages(self, chat_code: str, *message_ids: int) -> DeleteMessagesResponse:
        """
        delete messages by ids

        :param chat_code: chat code to delete messages from
        :param message_ids: message ids to delete
        :return: DeleteMessagesResponse object
        """
        logger.info(f"Deleting messages {message_ids=} from chat {chat_code=}")
        chat_data = self.get_one_chat_data(chat_code=chat_code)
        variables = dict(
            connections=[f"client:{chat_data.data.chat.id}:__ChatMessagesView_chat_messagesConnection_connection"],
            messageIds=list(message_ids)
        )
        response = self.send_query(Queries.delete_messages, variables=variables)
        return DeleteMessagesResponse(**response)

    def stop_message(self, message_id: int, text_length: int):
        """
        stop message generation by id

        :param message_id: message id to stop, int
        :param text_length: text length to stop at, int
        :return: MessageCancelResponse object
        """
        logger.info(f"Stopping message {message_id=}")
        variables = dict(messageId=message_id, textLength=text_length)
        response = self.send_query(Queries.stop_message, variables=variables)
        return MessageCancelResponse(**response)

    def _message_generator(self,
                           last_message: Union[LastMessage, MessageData],
                           edge_create: Optional[MessageEdgeCreate] = None) -> MessageGenerator:
        """
        generator for messages
        will yield WsMessage objects until a bot message is complete
        in the end will add humanMessage field to WsMessage object if edge_create is provided
        to get the generated message text, you can use ws_model.text

        :param last_message: LastMessage object
        :param edge_create: MessageEdgeCreate object, optional
        :return: generator of WsMessage objects
        """
        attempts = 0
        max_attempts = 3

        while True:
            try:
                ws_response = self._message_queues[last_message.id].get(timeout=5)
            except queue.Empty:
                if attempts == max_attempts:
                    self.disconnect()
                    raise ConnectionError("Connection lost")

                self.reconnect_to_ws()
                attempts += 1
                continue

            ws_model = WsMessage(**ws_response)

            if ws_model.state not in ("incomplete", "complete"):
                raise ValueError(f"Invalid message state: {ws_model.state}, data: {ws_response}")

            if ws_model.state == 'complete' and edge_create:
                ws_model.humanMessage = edge_create.message.node

            yield ws_model

            if ws_model.state == "complete":
                break

    def send_message(self, bot_name: str, message: str, chat_id: int = None) -> MessageGenerator:
        """
        send a message to the bot
        will return generator until a bot message is complete
        in the end will add humanMessage field to WsMessage object
        to get the generated message text, you can use ws_model.text

        :param bot_name: bot name (handle) to send a message to, string
        :param message: message text to send, string
        :param chat_id: chat id to send a message to, int, if not provided, will create a new chat
        :return: generator of WsMessage objects
        """
        logger.info(f"Sending message {message=} to {bot_name=}, {chat_id=}")
        variables = dict(
            attachments=[],
            bot=self._strip_handle(bot_name),
            chatId=chat_id,
            clientNonce=self._generate_nonce(),
            query=message,
            sdid="",
            shouldFetchChat=True,
            source=dict(sourceType="chat_input", chatInputMetadata=dict(useVoiceRecord=False))
        )
        response = self.send_query(Queries.send_message, variables=variables)

        if response.get("data") and (me_create := response["data"].get("messageEdgeCreate")):
            if status := me_create.get("status"):
                if status != "success":
                    raise ValueError(f"Failed to send message: {status}")

        model = SendMessageResponse(**response)
        edge_create = model.data.messageEdgeCreate
        chat = edge_create.chat
        last_message = chat.lastMessage

        logger.info(f"Subscribing to message {last_message.id} via websocket")
        self._active_messages[last_message.id] = None
        self._message_queues[last_message.id] = queue.Queue()

        yield from self._message_generator(last_message, edge_create)

        del self._active_messages[last_message.id]
        del self._message_queues[last_message.id]

    def regenerate_message(self, chat_code: str) -> MessageGenerator:
        """
        regenerate last bot message in chat

        :param chat_code: chat code to regenerate message in, string
        :return: generator of WsMessage objects
        """
        logger.info(f"Regenerating message in chat {chat_code=}")
        last_messages = self.get_chat_messages(chat_code, count=2)

        if last_messages[-1] == "human":
            raise ValueError("Last message is human, cannot regenerate")

        human_message, bot_message = last_messages
        human_message: MessageData
        variables = dict(messageId=bot_message.messageId)
        response = self.send_query(Queries.retry_message, variables=variables)
        RegenerateMessageResponse(**response)

        logger.info(f"Subscribing to message {human_message.id} via websocket")
        self._active_messages[human_message.id] = None
        self._message_queues[human_message.id] = queue.Queue()

        yield from self._message_generator(human_message)

        del self._active_messages[human_message.id]
        del self._message_queues[human_message.id]

    def get_settings(self) -> SettingsResponse:
        """
        get settings data
        to get bot limits: settings.data.viewer.messageLimitsConnection.edges[i].node

        :return: SettingsResponse object
        """
        logger.info("Getting settings")
        response = self.send_query(Queries.settings_page, {})
        return SettingsResponse(**response)
