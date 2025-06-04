#resturant management system


menu = {
    'Pizza': 40,
    'Burger': 30,
    'Pasta': 50,
    'Salad': 20,
    'coffee': 10,

    }

#Greet
print("Welcome to the Jim 's Restaurant")
print("Pizza :Tk.40\nBurger :Tk.30\nPasta :Tk.50\nSalad :Tk.20\nCoffee :Tk.10")

order_total = 0

item_1 = input("Enter the name of the item you want to order (or type 'done' to finish): ")
if item_1 in menu:
    order_total += menu[item_1]
    order_total += menu[item_1]
    print(f"Your item{item_1} has beem added to your order")

else:
    print(f"Sorry, we don't have {item_1} on the menu.")

    another_item = input("Do you want to order another item? (yes/no): ")
    if another_item == 'yes':
        item_2 = input("Enter the name of the seconf item =")
        if item_2 in menu:
            order_total += menu[item_2]
            print(f"Your item{item_2} has been added to your order")

        else:
            print(f"Sorry, we don't have {item_2} on the menu.")

            print(f"Your total order amount is Tk.{order_total}")
            print("Thank you for dining with us!")
