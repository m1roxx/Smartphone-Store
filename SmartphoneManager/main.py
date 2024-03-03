from database import Database
from smartphoneManager import SmartphoneManager
from userManager import UserManager


def menu():
    print("*** Welcome to Smartphone Manager! ***")
    print("1. Customer")
    print("2. Seller")
    print("3. Exit")


def customerMenu():
    print("Menu:")
    print("1. Show all Smartphones")
    print("2. Search by Smartphones")
    print("3. Rating of Smartphones")
    print("4. Buy a Smartphone")
    print("5. View my Purchases")
    print("6. Clear cart")
    print("7. Exit")


def sellerMenu():
    print("Menu:")
    print("1. Show all Smartphones")
    print("2. Add Smartphone")
    print("3. Update Smartphone")
    print("4. Delete Smartphone")
    print("5. Rating of Smartphones")
    print("6. View all Purchases")
    print("7. Exit")


def main():
    try:
        database = Database(
            dbname="postgres",
            user="postgres",
            password="1234",
            host="localhost",
            port="5432"
        )
        database.connect()

        user_manager = UserManager(database.connection)

        print("Welcome to the Smartphone store!")
        print("1. Login")
        print("2. Register")
        user_option = input("Enter your choice: ")

        if user_option == "1":
            username = input("Enter your username: ")
            password = input("Enter your password: ")

            user = user_manager.login_user(username, password)
            if user:
                role = user['role']
                if role == 'seller':
                    manager = SmartphoneManager(database.connection)
                    sellerMenu()

                elif role == 'customer':
                    manager = SmartphoneManager(database.connection)
                    customerMenu()

                else:
                    print("Invalid role.")
                    return

                while True:
                    option = int(input("Choose an option >> "))
                    if role == 'seller':
                        if option == 1:
                            manager.showAllSmartphones()
                            sellerMenu()

                        elif option == 2:
                            manager.addSmartphone()
                            sellerMenu()

                        elif option == 3:
                            manager.updateSmartphone()
                            sellerMenu()

                        elif option == 4:
                            manager.deleteSmartphone()
                            sellerMenu()

                        elif option == 5:
                            manager.ratingOfSmartphones()
                            sellerMenu()

                        elif option == 6:
                            manager.viewAllPurchases()
                            sellerMenu()

                        elif option == 7:
                            print("Exiting program.")
                            break

                        else:
                            print("Invalid choice. Please try again.")
                    elif role == 'customer':
                        if option == 1:
                            manager.showAllSmartphones()
                            customerMenu()

                        elif option == 2:
                            manager.searchSmartphone()
                            customerMenu()

                        elif option == 3:
                            manager.ratingOfSmartphones()
                            customerMenu()

                        elif option == 4:
                            manager.purchaseSmartphone(username)
                            customerMenu()

                        elif option == 5:
                            manager.viewPurchases(username)
                            customerMenu()

                        elif option == 6:
                            manager.clearCart(username)
                            customerMenu()

                        elif option == 7:
                            print("Exiting program.")
                            break

                        else:
                            print("Invalid choice. Please try again.")

        elif user_option == "2":
            username = input("Enter your username: ")
            password = input("Enter your password: ")
            user_manager.register_user(username, password)
            main()

    except Exception as e:
        print("Error:", e)

    finally:
        if database is not None:
            database.disconnect()


if __name__ == "__main__":
    main()
