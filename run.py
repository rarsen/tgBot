from booking.booking import Booking

try:
    with Booking() as bot:
        bot.land_first_page()
        bot.change_currency(currency="USD")
        bot.select_place_to_go("New York")
        bot.select_date(checkIn="2024-09-15",checkOut="2024-09-20")

        bot.select_people(adultsCount=2,childrenCount=2,childrenAges=[10,8])

        bot.clickSearch()
        bot.apply_filters(4,5)
        # bot.report_results()
        bot.wait(1000)


except Exception as e:
    if  "in PATH." in str(e):
        print(f"There is an error: {e}.")
    else:
        raise


#input("Where you want to go?\n")
#input("What is the check-in date?\n")
#input("What is the check-out date?\n")
#input("How many adults?\n")