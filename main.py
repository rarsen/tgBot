from telegram import Update, Bot
from telegram.constants import ParseMode
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler
from booking.booking import Booking
from booking.booking_report import BookingReport
import logging
import re

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define states for the conversation
LOCATION, CHECKIN, CHECKOUT, ADULTS, CHILDREN, AGES, STARS = range(7)

# Validate date input format (YYYY-MM-DD)
def valid_date(date_text):
    return bool(re.match(r'^\d{4}-\d{2}-\d{2}$', date_text))

# Start the bot
async def start(update: Update, context) -> int:
    await update.message.reply_text("Welcome! Where do you want to go?")
    return LOCATION

# Collect location input
async def get_location(update: Update, context) -> int:
    context.user_data['location'] = update.message.text
    await update.message.reply_text(f"Great! Now, what is the check-in date? (Format: YYYY-MM-DD)")
    return CHECKIN

# Collect check-in date input
async def get_checkin_date(update: Update, context) -> int:
    if valid_date(update.message.text):
        context.user_data['checkin_date'] = update.message.text
        await update.message.reply_text("What is the check-out date? (Format: YYYY-MM-DD)")
        return CHECKOUT
    else:
        await update.message.reply_text("Invalid date format. Please enter the check-in date in the format YYYY-MM-DD.")
        return CHECKIN

# Collect check-out date input
async def get_checkout_date(update: Update, context) -> int:
    if valid_date(update.message.text):
        context.user_data['checkout_date'] = update.message.text
        await update.message.reply_text("How many adults?")
        return ADULTS
    else:
        await update.message.reply_text("Invalid date format. Please enter the check-out date in the format YYYY-MM-DD.")
        return CHECKOUT

# Collect number of adults input
async def get_adults(update: Update, context) -> int:
    if update.message.text.isdigit():
        context.user_data['adults'] = int(update.message.text)
        await update.message.reply_text("How many children?")
        return CHILDREN
    else:
        await update.message.reply_text("Please enter a valid number for adults.")
        return ADULTS

# Collect number of children input
async def get_children(update: Update, context) -> int:
    if update.message.text.isdigit():
        context.user_data['children'] = int(update.message.text)
        if int(update.message.text) > 0:
            await update.message.reply_text("Please enter the ages of the children separated by commas (e.g., 3, 5, 7):")
            return AGES
        else:
            await update.message.reply_text("What star rating would you prefer? (Enter numbers separated by commas, e.g., 3,4,5)")
            return STARS
    else:
        await update.message.reply_text("Please enter a valid number for children.")
        return CHILDREN

# Collect children's ages input
async def get_children_ages(update: Update, context) -> int:
    children_ages = update.message.text.split(',')
    if all(age.strip().isdigit() for age in children_ages):
        context.user_data['children_ages'] = [int(age.strip()) for age in children_ages]
        await update.message.reply_text("What star rating would you prefer? (Enter numbers separated by commas, e.g., 3,4,5)")
        return STARS
    else:
        await update.message.reply_text("Please enter valid ages for children, separated by commas.")
        return AGES

# Collect star ratings and initiate the search
async def get_star_ratings(update: Update, context) -> int:
    star_ratings = update.message.text.split(',')
    if all(star.strip().isdigit() for star in star_ratings):
        context.user_data['star_ratings'] = [int(star.strip()) for star in star_ratings]
        await update.message.reply_text("Got it! I'll start searching for the best deals now...")

        # Extract user input details
        location = context.user_data['location']
        checkin_date = context.user_data['checkin_date']
        checkout_date = context.user_data['checkout_date']
        adults = int(context.user_data['adults'])
        children = int(context.user_data['children'])
        children_ages = context.user_data.get('children_ages', [])
        star_values = context.user_data['star_ratings']

        try:
            # Using the Booking bot to search for hotels
            with Booking() as bot:
                bot.land_first_page()
                bot.change_currency(currency="USD")
                bot.select_place_to_go(location)
                bot.select_date(checkIn=checkin_date, checkOut=checkout_date)
                bot.select_people(adultsCount=adults, childrenCount=children, childrenAges=children_ages)
                bot.clickSearch()
                bot.apply_filters(*star_values)  # Apply the star filters

                # Grab the hotel list (update this XPATH with the appropriate one for your case)
                hotelBoxes = bot.find_element(By.XPATH, '//*[@id="bodyconstraint-inner"]/div[2]/div/div[2]/div[3]/div[2]/div[2]/div[3]')
                
                # Call the report_results_with_links function to send messages
                await report_results_with_links(context.bot, update.message.chat_id, hotelBoxes)
                # bot.wa
        except Exception as e:
            logger.error(f"Error occurred during hotel search: {e}")
            await update.message.reply_text("An error occurred while searching for hotels. Please try again later.")

        return ConversationHandler.END
    else:
        await update.message.reply_text("Please enter valid star ratings (numbers separated by commas).")
        return STARS

# Send hotel results to the user
async def report_results_with_links(bot: Bot, chat_id: int, hotel_boxes_element: WebElement):
    report = BookingReport(hotel_boxes_element)
    hotel_data = report.pullDealBoxesAttributes()

    if not hotel_data:
        await bot.send_message(chat_id=chat_id, text="No hotels found.")
        return

    # Iterate through each hotel and send a message
    for hotel in hotel_data:
        message_text = (
            f"*Hotel Name:* {hotel['name']}\n"
            f"*Price:* {hotel['price']}\n"
            f"*Score:* {hotel['score']}\n"
            f"*Link:* [Click here]({hotel['link']})"
        )

        # Send the message for each hotel
        await bot.send_message(chat_id=chat_id, text=message_text, parse_mode=ParseMode.MARKDOWN)

# Cancel the conversation
async def cancel(update: Update, context) -> int:
    await update.message.reply_text("Goodbye! If you need help, just type /start again.")
    return ConversationHandler.END

def main():
    TOKEN = '7545097824:AAEFt61RydVcsakk7Hz4A0LFL6YG9x5WUbg'

    # Create the Application and pass the bot's token
    application = Application.builder().token(TOKEN).build()

    # Define a conversation handler with states
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            LOCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_location)],
            CHECKIN: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_checkin_date)],
            CHECKOUT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_checkout_date)],
            ADULTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_adults)],
            CHILDREN: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_children)],
            AGES: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_children_ages)],
            STARS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_star_ratings)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    # Add conversation handler to application
    application.add_handler(conv_handler)

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()
