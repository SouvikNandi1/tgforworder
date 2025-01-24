from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import logging
import re

# Replace with your bot token
BOT_TOKEN = '7397423501:AAHxsRXPz8qJssxGf2Yzi_XpbQyq66by45o'

# Source channel ID and destination group/channel IDs
CHANNEL_GROUP_MAP = {
    -1001430003499: ["-1001565012822", "-1001234389929"],  # Channel 1 -> Group 1
    -1002343910094: ["-1002292833112"],
    # -1002407553232: ["-1002399639409"]
}

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def escape_markdown_v2(text):
    """Escapes special characters for MarkdownV2."""
    return re.sub(r'([_*\[\]()~`>#+\-=|{}.!])', r'\\\1', text)

async def copy_and_forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Copies and forwards messages from source channels to destination groups/channels."""
    try:
        if update.channel_post:
            source_channel_id = update.channel_post.chat.id

            # Check if the source channel exists in the mapping
            if source_channel_id in CHANNEL_GROUP_MAP:
                for destination_id in CHANNEL_GROUP_MAP[source_channel_id]:
                    # Handle text messages
                    if update.channel_post.text:
                        bold_text = f"*{escape_markdown_v2(update.channel_post.text)}*"
                        await context.bot.send_message(
                            chat_id=destination_id,
                            text=bold_text,
                            parse_mode="MarkdownV2"
                        )
                    # Handle photos
                    elif update.channel_post.photo:
                        caption = escape_markdown_v2(update.channel_post.caption or "")
                        bold_caption = f"*{caption}*" if caption else ""
                        await context.bot.send_photo(
                            chat_id=destination_id,
                            photo=update.channel_post.photo[-1].file_id,  # Use the best quality photo
                            caption=bold_caption,
                            parse_mode="MarkdownV2"
                        )
                    # Handle videos
                    elif update.channel_post.video:
                        caption = escape_markdown_v2(update.channel_post.caption or "")
                        bold_caption = f"*{caption}*" if caption else ""
                        await context.bot.send_video(
                            chat_id=destination_id,
                            video=update.channel_post.video.file_id,
                            caption=bold_caption,
                            parse_mode="MarkdownV2"
                        )
                    # Handle documents
                    elif update.channel_post.document:
                        caption = escape_markdown_v2(update.channel_post.caption or "")
                        bold_caption = f"*{caption}*" if caption else ""
                        await context.bot.send_document(
                            chat_id=destination_id,
                            document=update.channel_post.document.file_id,
                            caption=bold_caption,
                            parse_mode="MarkdownV2"
                        )
                    else:
                        logger.warning("Unsupported message type")
    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)

def main():
    try:
        # Create the bot application
        application = ApplicationBuilder().token(BOT_TOKEN).concurrent_updates(50).build()

        # Add a handler for channel posts
        for channel_id in CHANNEL_GROUP_MAP.keys():
            application.add_handler(MessageHandler(filters.Chat(channel_id), copy_and_forward_message))

        # Start the bot
        logger.info("Bot is running... Press Ctrl+C to stop.")
        application.run_polling()
    except Exception as e:
        logger.critical(f"Critical error: {e}", exc_info=True)

if __name__ == '__main__':
    main()
