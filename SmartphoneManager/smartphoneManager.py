import datetime


class SmartphoneManager:
    def __init__(self, connection):
        self.connection = connection

    def addSmartphone(self, id=None, brand=None, model=None, price=None, rom=None, cpu=None):
        if id is None:
            id = int(input("Enter smartphone ID: "))
        if brand is None:
            brand = input("Enter smartphone brand: ")
        if model is None:
            model = input("Enter smartphone model: ")
        if price is None:
            price = int(input("Enter smartphone price: "))
        if rom is None:
            rom = int(input("Enter smartphone ROM size: "))
        if cpu is None:
            cpu = input("Enter smartphone CPU: ")

        query = "INSERT INTO smartphones (id, brand, model, price, rom, cpu) VALUES (%s, %s, %s, %s, %s, %s)"
        with self.connection.cursor() as cursor:
            cursor.execute(query, (id, brand, model, price, rom, cpu))
        self.connection.commit()
        print("Smartphone added successfully!")

    def showAllSmartphones(self):
        print("Here are all smartphones:")
        query = "SELECT * FROM smartphones ORDER BY id ASC"
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            print("{:<5} {:<20} {:<30} {:<10} {:<10} {:<20}".format("ID", "Brand", "Model", "Price", "ROM", "CPU"))
            print("-" * 85)
            for record in cursor.fetchall():
                id, brand, model, price, rom, cpu = record
                print("{:<5} {:<20} {:<30} {:<10} {:<10} {:<20}".format(id, brand, model, f"${price}", f"{rom}GB", cpu))

    def updateSmartphone(self, id=None, brand=None, model=None, price=None, rom=None, cpu=None):
        if id is None:
            id = int(input("Enter smartphone ID: "))
        if brand is None:
            brand = input("Enter new smartphone brand: ")
        if model is None:
            model = input("Enter new smartphone model: ")
        if price is None:
            price = int(input("Enter new smartphone price: "))
        if rom is None:
            rom = int(input("Enter new smartphone ROM size: "))
        if cpu is None:
            cpu = input("Enter new smartphone CPU: ")
        query = "UPDATE smartphones SET brand = %s, model = %s, price = %s, rom = %s, cpu = %s WHERE id = %s"
        with self.connection.cursor() as cursor:
            cursor.execute(query, (brand, model, price, rom, cpu, id))
        self.connection.commit()
        print("Smartphone updated successfully!")

    def deleteSmartphone(self, id=None):
        if id is None:
            id = int(input("Enter smartphone ID to delete: "))
        query = "DELETE FROM smartphones WHERE id = %s"
        with self.connection.cursor() as cursor:
            cursor.execute(query, (id,))
        self.connection.commit()
        print("Smartphone deleted successfully!")

    def searchSmartphone(self):
        print("Enter search criteria:")
        brand = input("Brand (leave empty to skip): ")
        model = input("Model (leave empty to skip): ")
        min_price = input("Minimum price (leave empty to skip): ")
        max_price = input("Maximum price (leave empty to skip): ")
        min_rom = input("Minimum ROM size in GB (leave empty to skip): ")
        cpu = input("CPU (leave empty to skip): ")

        # Формируем запрос в зависимости от введенных критериев
        query = "SELECT * FROM smartphones WHERE TRUE"
        params = []

        if brand:
            query += " AND brand = %s"
            params.append(brand)
        if model:
            query += " AND model = %s"
            params.append(model)
        if min_price:
            query += " AND price >= %s"
            params.append(min_price)
        if max_price:
            query += " AND price <= %s"
            params.append(max_price)
        if min_rom:
            query += " AND rom >= %s"
            params.append(min_rom)
        if cpu:
            query += " AND cpu = %s"
            params.append(cpu)

        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
            smartphones = cursor.fetchall()
            if smartphones:
                print("Search results:")
                for record in smartphones:
                    id, brand, model, price, rom, cpu = record
                    print(f"ID: {id}, Brand: {brand}, Model: {model}, Price: ${price}, ROM: {rom}GB, CPU: {cpu}")
            else:
                print("No smartphones found matching the specified criteria.")

    def ratingOfSmartphones(self):
        print("Choose the type of rating:")
        print("1. The most powerful smartphones")
        print("2. The cheapest smartphones")
        print("3. The most expensive smartphones")

        choice = input("Enter your choice: ")

        if choice == "1":
            self.topSmartphones("powerful")

        elif choice == "2":
            self.topSmartphones("cheapest")

        elif choice == "3":
            self.topSmartphones("expensive")

        else:
            print("Invalid choice. Please try again.")

    def topSmartphones(self, rating_type):
        if rating_type == "powerful":
            query = "SELECT * FROM smartphones ORDER BY id ASC LIMIT 3"
            rating_name = "The most powerful smartphones"
        elif rating_type == "cheapest":
            query = "SELECT * FROM smartphones ORDER BY price ASC LIMIT 3"
            rating_name = "The cheapest smartphones"
        elif rating_type == "expensive":
            query = "SELECT * FROM smartphones ORDER BY price DESC LIMIT 3"
            rating_name = "The most expensive smartphones"

        print(rating_name + ":")
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            smartphones = cursor.fetchall()
            for idx, record in enumerate(smartphones, start=1):
                id, brand, model, price, rom, cpu = record
                print(f"{idx}. Brand: {brand}, Model: {model}, Price: ${price}, ROM: {rom}GB, CPU: {cpu}")

    def purchaseSmartphone(self, username):
        try:

            with self.connection.cursor() as cursor:
                query = "SELECT id FROM users WHERE username = %s"
                cursor.execute(query, (username,))
                customer_id = cursor.fetchone()[0]

            brand = input("Enter smartphone brand: ")
            model = input("Enter smartphone model: ")

            with self.connection.cursor() as cursor:
                query = "SELECT id FROM smartphones WHERE brand = %s AND model = %s"
                cursor.execute(query, (brand, model))
                smartphone = cursor.fetchone()
                if smartphone:
                    smartphone_id = smartphone[0]
                else:
                    print("Smartphone not found.")
                    return

            purchase_date = datetime.date.today()
            with self.connection.cursor() as cursor:
                query = "INSERT INTO purchases (customer_id, smartphone_id, purchase_date) VALUES (%s, %s, %s)"
                cursor.execute(query, (customer_id, smartphone_id, purchase_date))
            self.connection.commit()
            print("Purchase successful!")
        except Exception as e:
            print("Error purchasing smartphone:", e)

    def viewPurchases(self, username):
        try:
            with self.connection.cursor() as cursor:
                query_user_id = "SELECT id FROM users WHERE username = %s"
                cursor.execute(query_user_id, (username,))
                result = cursor.fetchone()
                if result:
                    customer_id = result[0]
                else:
                    print("User not found.")
                    return

                query = "SELECT p.purchase_id, s.brand, s.model, p.purchase_date FROM purchases p INNER JOIN smartphones s ON p.smartphone_id = s.id WHERE p.customer_id = %s"
                cursor.execute(query, (customer_id,))
                purchases = cursor.fetchall()
                if purchases:
                    print("Your purchases:")
                    print("{:<10} {:<20} {:<30} {:<20}".format("ID", "Brand", "Model", "Purchase Date"))
                    print("-" * 80)
                    for purchase in purchases:
                        purchase_id, brand, model, purchase_date = purchase
                        purchase_date_str = purchase_date.strftime("%Y-%m-%d")
                        print("{:<10} {:<20} {:<30} {:<20}".format(purchase_id, brand, model, purchase_date_str))
                else:
                    print("You haven't made any purchases yet.")
        except Exception as e:
            print("Error viewing purchases:", e)

    def clearCart(self, username):
        try:
            with self.connection.cursor() as cursor:
                query = "SELECT id FROM users WHERE username = %s"
                cursor.execute(query, (username,))
                result = cursor.fetchone()
                if result:
                    customer_id = result[0]
                    delete_query = "DELETE FROM purchases WHERE customer_id = %s"
                    cursor.execute(delete_query, (customer_id,))
                    self.connection.commit()
                    print("Cart cleared successfully!")
                else:
                    print("User not found.")
        except Exception as e:
            print("Error clearing cart:", e)

    def viewAllPurchases(self):
        try:
            with self.connection.cursor() as cursor:
                query = "SELECT p.purchase_id, u.username, s.brand, s.model, p.purchase_date FROM purchases p INNER JOIN users u ON p.customer_id = u.id INNER JOIN smartphones s ON p.smartphone_id = s.id"
                cursor.execute(query)
                purchases = cursor.fetchall()
                if purchases:
                    print("All purchases:")
                    print("{:<10} {:<20} {:<20} {:<30} {:<20}".format("Purchase ID", "Customer", "Brand", "Model",
                                                                      "Purchase Date"))
                    print("-" * 100)
                    for purchase in purchases:
                        purchase_id, username, brand, model, purchase_date = purchase
                        purchase_date_str = purchase_date.strftime("%Y-%m-%d")
                        print("{:<10} {:<20} {:<20} {:<30} {:<20}".format(purchase_id, username, brand, model,
                                                                          purchase_date_str))
                else:
                    print("No purchases found.")
        except Exception as e:
            print("Error viewing purchases:", e)
