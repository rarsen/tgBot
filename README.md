Booking.com Hotel Finder Telegram Bot
=====================================

A Telegram bot built with Python and the python-telegram-bot library that allows users to search for hotels on [Booking.com](https://www.booking.com) by providing details such as location, check-in/check-out dates, number of guests, and preferred star ratings. The bot scrapes data from Booking.com and sends results back to the user in a structured format with hotel names, prices, and ratings.

Features
--------

*   **User-friendly Interaction**: The bot interacts with users step-by-step, asking for relevant booking details.
    
*   **Hotel Search**: Retrieves hotel information (name, price, rating) from Booking.com based on the user's input.
    
*   **Multi-user Support**: Multiple users can use the bot simultaneously, with each session handled independently.
    
*   **Customizable Search**: Users can specify location, travel dates, number of adults and children, children's ages, and desired hotel star ratings.
    
*   **Booking Links**: Provides clickable links to view and book hotels directly on Booking.com.
    

Bot Conversation Flow
---------------------

1.  **/start** - Initiates the conversation and prompts the user for a location.
    
2.  **Location** - The user provides the city or destination where they want to stay.
    
3.  **Check-in Date** - The bot asks for the check-in date in YYYY-MM-DD format.
    
4.  **Check-out Date** - The bot asks for the check-out date in YYYY-MM-DD format.
    
5.  **Number of Adults** - The user specifies how many adults are traveling.
    
6.  **Number of Children** - The user specifies how many children are traveling, if any.
    
7.  **Children's Ages** - If children are included, the bot asks for their ages.
    
8.  **Star Rating** - The user selects the preferred hotel star ratings (e.g., 3, 4, 5 stars).
    
9.  **Results** - The bot scrapes Booking.com and returns a list of matching hotels with prices, ratings, and links.
    

Requirements
------------

*   Python 3.7+
    
*   python-telegram-bot library
    
*   selenium for web scraping
    
*   A Telegram bot token from the BotFather
    

Setup
-----

1. git clone https://github.com/your-username/your-repo-name.gitcd your-repo-name
    
2.  pip install -r requirements.txt
    
3.  **Set Up the Telegram Bot**
    
    *   Create a new bot using the Telegram BotFather.
        
    *   TOKEN = 'YOUR\_TELEGRAM\_BOT\_TOKEN'
        
4.  **Configure Selenium**
    
    *   Ensure you have a valid webdriver (e.g., ChromeDriver) installed and configured.
        
    *   Download ChromeDriver from here and make sure it matches your Chrome browser version.
        
5.  **Run the Bot** Start the bot using: python bot.py

Usage
-----

Once the bot is running:

*   **Start a conversation** with the bot by sending /start.
    
*   Follow the bot's prompts to provide details like location, check-in/check-out dates, and preferences.
    
*   The bot will return a list of hotels matching your criteria, along with prices, ratings, and Booking.com links.
    

### Example Interaction:
 

https://github.com/user-attachments/assets/04793910-6a21-47e5-881e-122c46fcb3f3



Notes
-----

*   **Error Handling**: The bot ensures users enter valid data for dates, numbers of guests, and star ratings. If invalid input is provided, the bot will ask the user to correct it.
    
*   **Multi-user Support**: The bot can handle multiple conversations independently, ensuring each user's session is isolated from others.
    

Contribution
------------

Feel free to open an issue or submit a pull request if you want to contribute or improve this project.
