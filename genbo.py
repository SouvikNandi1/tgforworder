import os
import json
import telegram
import uuid
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import google.generativeai as genai

# Set the environment variable for the API key directly in the script
os.environ["GEMINI_API_KEY"] = "AIzaSyD1rwgTUfXUEyP9CbZS4fkvR2LMGxVM22Q"

# Configure the Google AI SDK with the API key
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Create the model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Initialize the Telegram bot with your Telegram token
telegram_token = '7184709586:AAE9aBg2us_BA2IcZzG1h3ZNhSW8B3mKNMM'
application = Application.builder().token(telegram_token).build()

# Print the current working directory
print("Current working directory:", os.getcwd())

# Function to log conversation to a JSON file
async def log_to_json(first_name, last_name, username, user_message, bot_response):
    log_file = 'chat_log.json'
    data = {}

    # Load existing data from JSON file if it exists
    if os.path.exists(log_file):
        try:
            with open(log_file, 'r') as f:
                data = json.load(f)
                print("Loaded existing data from JSON file.")
        except json.JSONDecodeError:
            print("JSON file is empty or invalid. Initializing new data.")

    # Initialize user data if not present
    full_name = f"{first_name} {last_name}".strip()
    profile_link = f"https://t.me/{username}" if username else "No profile link"
    if full_name not in data:
        data[full_name] = {"profile_link": profile_link, "messages": []}

    # Append new message data
    data[full_name]["messages"].append({
        "user_message": user_message,
        "bot_response": bot_response
    })

    # Write updated data back to JSON file
    with open(log_file, 'w') as f:
        json.dump(data, f, indent=4)
        print(f"Logged data for user '{full_name}' to {log_file}.")

# Function to check safety ratings
def check_safety(response):
    return True  # All responses will be accepted

# Function to handle generic messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text.lower()

    # Handle specific name-related messages first
    if "souvik" in user_message:
        await update.message.reply_text("Souvik Nandi is the creator of this bot 😊 @SouvikNandi1")
        return

    if "rohit" in user_message:
        await update.message.reply_text("Is Group Ka Malik Hai , Kuch Bola Tho Ban Ho Jao Ge")
        return

    if "pratham" in user_message:
        await update.message.reply_text("Telegram Market Ka Sabse Bada Chutiya")
        return

    if "aswathama" in user_message:
        await update.message.reply_text("@AKAAYKOHLI_OFFICIAL ka ek lota bap")
        return
    
    if "mpl" in user_message:
        await update.message.reply_text("@AmanSeth01 ka chota lulli 😂")
        return
    if "malik" in user_message:
        await update.message.reply_text("JANT MALIK MUMBAI 😂")
        return
    if "mumbai" in user_message:
        await update.message.reply_text("JANT MALIK MUMBAI 😂")
        return

    # Only respond when "genbo" is mentioned in the message
    if "genbo" in user_message:
        # Remove the word "genbo" from the message before sending it to the model
        clean_message = user_message.replace("genbo", "").strip()

        # Start a chat session with the model
        chat_session = model.start_chat(history=[])

        try:
            # Send the cleaned message to the model
            response = chat_session.send_message(clean_message)

            # Check safety ratings
            if check_safety(response):
                response_text = response.text
            else:
                response_text = "I'm sorry, but I can't respond to that right now. How about something else?"

        except Exception as e:
            response_text = "I'm sorry, but I can't respond to that right now. How about something else?"
            print(f"Error: {e}")

        # Log the conversation to the JSON file
        first_name = update.message.from_user.first_name
        last_name = update.message.from_user.last_name or ""
        username = update.message.from_user.username
        await log_to_json(first_name, last_name, username, user_message, response_text)

        # Send the response back to the user
        await update.message.reply_text(response_text)

    # No response if "genbo" is not mentioned
    else:
        return

# Add handler for text messages
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Function to start the bot
def start_bot():
    application.run_polling()

# Run the bot in the main thread
if __name__ == '__main__':
    start_bot()
