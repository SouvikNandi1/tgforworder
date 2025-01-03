from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# Replace with your bot token
BOT_TOKEN = '7397423501:AAHxsRXPz8qJssxGf2Yzi_XpbQyq66by45o'

# Source channel ID and destination group/channel IDs
CHANNEL_GROUP_MAP = {
    -1001473141095: [-1001957102020]  # Channel 1 -> Group 1
}

CHANNEL_GROUP_MAP_2 = {
    -1001473141095: [-1002372581992, -1002106307921],
    -1002311528048: [-1001925442740]  # Channel 1 -> Group 1, Group 2
}

async def copy_and_forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Copies and forwards messages from source channels to destination groups/channels."""
    if update.channel_post:
        source_channel_id = update.channel_post.chat.id
        
        # First, check if the source channel exists in the copy mapping
        if source_channel_id in CHANNEL_GROUP_MAP:
            for destination_id in CHANNEL_GROUP_MAP[source_channel_id]:
                # Handle text messages
                if update.channel_post.text:
                    await context.bot.send_message(
                        chat_id=destination_id,
                        text=update.channel_post.text
                    )
                # Handle photos
                elif update.channel_post.photo:
                    await context.bot.send_photo(
                        chat_id=destination_id,
                        photo=update.channel_post.photo[-1].file_id,  # Use the best quality photo
                        caption=update.channel_post.caption or ""
                    )
                # Handle videos
                elif update.channel_post.video:
                    await context.bot.send_video(
                        chat_id=destination_id,
                        video=update.channel_post.video.file_id,
                        caption=update.channel_post.caption or ""
                    )
                # Handle documents
                elif update.channel_post.document:
                    await context.bot.send_document(
                        chat_id=destination_id,
                        document=update.channel_post.document.file_id,
                        caption=update.channel_post.caption or ""
                    )
                # Handle other message types (optional)
                else:
                    print("Unsupported message type")
        
        # Now, check if the source channel exists in the forwarding mapping
        if source_channel_id in CHANNEL_GROUP_MAP_2:
            for group_id in CHANNEL_GROUP_MAP_2[source_channel_id]:
                # Forward the message to each destination group or channel
                await context.bot.forward_message(
                    chat_id=group_id,
                    from_chat_id=source_channel_id,
                    message_id=update.channel_post.message_id
                )

def main():
    # Create the bot application
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add a handler for channel posts
    for channel_id in CHANNEL_GROUP_MAP.keys():
        application.add_handler(MessageHandler(filters.Chat(channel_id), copy_and_forward_message))
    for channel_id in CHANNEL_GROUP_MAP_2.keys():
        application.add_handler(MessageHandler(filters.Chat(channel_id), copy_and_forward_message))

    # Start the bot
    print("Bot is running... Press Ctrl+C to stop.")
    application.run_polling()

if __name__ == '__main__':
    main()
