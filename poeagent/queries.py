from enum import Enum


class Queries(Enum):
    available_bots = "availableBotsSelectorModalPaginationQuery"
    bot_selector = "BotSelectorModalQuery"
    chat_history_page = "chatsHistoryPageQuery"
    chat_list_pagination = "ChatListPaginationQuery"
    chat_page = "ChatPageQuery"
    create_bot_index_page = "createBotIndexPageQuery"
    create_bot_main = "CreateBotMain_poeBotCreate_Mutation"
    delete_bot = "BotInfoCardActionBar_poeBotDelete_Mutation"
    delete_chat = "useDeleteChat_deleteChat_Mutation"
    delete_messages = "MessageDeleteConfirmationModal_deleteMessageMutation_Mutation"
    edit_bot_main = "EditBotMain_poeBotEdit_Mutation"
    handle_landing_bot_page = 'HandleBotLandingPageQuery'
    layout_right_sidebar = "layoutRightSidebarQuery"
    retry_message = "regenerateMessageMutation"
    send_message = "sendMessageMutation"
    settings_page = "settingsPageQuery"
    stop_message = "stopMessage_messageCancel_Mutation"
    subscription = "subscriptionsMutation"
