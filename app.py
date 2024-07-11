import csv
import datetime

from sqlalchemy import func
from models import Base, session, engine, Brands, Product


def main_menu():
    while True:
        print('''
        \n PROGRAMMING INVENTORY
        \r v) View all products
        \r n) Add new product
        \r a) Analyse database
        \r b) Create a backup
        \r x) Exit     
        ''')
        choice = input("Please choose an option above. ").lower()
        if choice in ("v", "n", "a", "b", "x"):
            return choice
        else:
            input('''
            \r Please choose a valid option from above.
            \r Please press enter to try again. ''')


def submenu():
    while True:
        print('''
         \n PROGRAMMING INVENTORY
         \r e) Edit product
         \r d) Delete product
         \r x) Exit     
         ''')
        choice = input("Please choose an option above. ").lower()
        if choice in ("e", "d", "x"):
            return choice
        else:
            input('''
             \r Please choose a valid option from above.
             \r Please press enter to try again. ''')


def add_inventory_csv():
    with open("inventory.csv") as csvfile:
        data = csv.reader(csvfile)
        next(data)
        for row in data:
            product_in_db = session.query(Product).filter(Product.product_name == row[0]).one_or_none()
            if product_in_db is None:
                product_name = row[0]
                product_price = clean_db_price(row[1])
                product_quantity = row[2]
                date_updated = clean_db_date(row[3])
                brand_name = row[4]
                brand = session.query(Brands).filter(Brands.brand_name == brand_name).one_or_none()
                new_product = Product(product_name=product_name, product_quantity=product_quantity,
                                      product_price=product_price, date_updated=date_updated, brand=brand)
                session.add(new_product)
        session.commit()


def clean_db_price(price_str):
    fixed = price_str[1:]
    try:
        price_float = float(fixed)
    except ValueError:
        input('''
                 \n PRICE ERROR
                 \r The price format should be a number without a currency symbol.
                 \r Ex: 10.99.
                 \r Press enter to try again. ''')
    else:
        return int(price_float * 100)


def clean_db_date(date_str):
    try:
        fixed_date = datetime.datetime.strptime(date_str, '%m/%d/%Y').date()
    except ValueError:
        input("""
        \n DATE ERROR
        \r The date format should be MM/DD/YYYY.
        \r Press enter to try again.""")
    else:
        return fixed_date


def add_brands_csv():
    with open("brands.csv") as csvfile:
        data = csv.reader(csvfile)
        next(data)
        for row in data:
            brand_in_db = session.query(Brands).filter(Brands.brand_name == row[0]).one_or_none()
            if brand_in_db is None:
                brand_name = row[0]
                new_brand = Brands(brand_name=brand_name)
                session.add(new_brand)
        session.commit()


def clean_date():
    while True:
        date_updated = input("Date Updated (MM/DD/YYYY): ")
        try:
            date = datetime.datetime.strptime(date_updated, '%m/%d/%Y').date()
            if date > datetime.date.today():
                raise ValueError("Date cannot be in the future. Please enter a valid date.")
            return date
        except ValueError as e:
            print(f"Date format error: {e}")


def clean_user_price(price_str):
    try:
        price_float = float(price_str)
        return int(price_float * 100)
    except ValueError:
        input('''
                \n PRICE ERROR
                \r The price format should be a number without a currency symbol.
                \r Ex: 10.99.
                \r Press enter to try again. ''')
        return None


def clean_brand_id(brand_id, options):
    while True:
        try:
            brand_id = int(brand_id)
            if brand_id in options:
                return brand_id
        except ValueError:
            pass
        input('''
                \n ID ERROR
                \r Please choose a valid ID from the numbers provided.
                \r Options: {options}
                \r Press press enter to try again. ''')
        brand_id = input("Please enter new ID:")


def add_new_product():
    product_name = input("New Product: ")
    while True:
        price = input("New Price: ")
        try:
            product_price = clean_user_price(price)
            break
        except ValueError:
            print("Price should be a valid number without a currency symbol. Please try again.")
    product_quantity = input("New Quantity: ")
    date_updated = clean_date()
    id_error = True
    while id_error:
        for brand in session.query(Brands):
            print(f"{brand.id}: {brand.brand_name}")
        id_choice = input(f'''Brand ID: ''')
        brand_id = id_choice
        if type(brand_id) == int:
            id_error = False
        brand = session.query(Brands).filter_by(id=brand_id).first()
        if not brand:
            print("Invalid Brand ID. Please choose a valid ID.")
        existing_product = session.query(Product).filter_by(product_name=product_name).first()
        if existing_product:
            existing_product.product_quantity = product_quantity
            existing_product.product_price = price
            existing_product.date_updated = date_updated
            existing_product.brand = brand
            session.commit()
            print(f"Product '{product_name}' updated successfully.")
            input("Press enter to continue.")
            return
        else:
            new_product = Product(
                product_name=product_name,
                product_quantity=product_quantity,
                product_price=product_price,
                date_updated=date_updated,
                brand=brand
                )
            session.add(new_product)
            session.commit()
            print(f"Product '{product_name}' added successfully.")
            input("Press enter to continue.")
            return


def edit_product_check(column_name, current_value):
    print(f'Edit {column_name}')
    if column_name == "Price":
        print(f'Current Price: ${current_value / 100}')
    elif column_name == "Last Updated":
        print(f'Last Updated: {current_value}')
    elif column_name == "Brand":
        print(f"Current Brand: {current_value}")
        for brand in session.query(Brands):
            print(f"{brand.id}: {brand.brand_name}")
    else:
        print(f'{column_name}: {current_value}')

    while True:
        try:
            if column_name == "Last Updated":
                updated_value = clean_date()
                return updated_value
            else:
                updated_value = input(f"Enter Updated {column_name}: ")

            if column_name == "Price":
                updated_value = clean_user_price(updated_value)
                if updated_value is not None:
                    return updated_value
            elif column_name == "Brand":
                brand_id = int(updated_value)
                brand = session.query(Brands).filter_by(id=brand_id).first()
                if not brand:
                    raise ValueError("Invalid Brand ID. Please choose a valid ID.")
                return brand_id
            else:
                return updated_value
        except ValueError as e:
            print(f'Error: {e}')


def clean_id(product_id, options):
    while True:
        try:
            product_id = int(product_id)
            if product_id in options:
                return product_id
        except ValueError:
            pass
        input('''
            \n ID ERROR
            \r Please choose a valid ID from the numbers provided.
            \r Press press enter to try again. ''')
        product_id = input("Please enter new ID:")


def view_product():
    id_options = [product.id for product in session.query(Product)]
    if not id_options:
        print("No products available.")
    id_choice = None
    while not id_choice:
        id_choice = input(f'''
                        \n ID Options {id_options}
                        \r Product ID: ''')
        id_choice = clean_id(id_choice, id_options)

    selected_product = session.query(Product).filter(Product.id == id_choice).first()
    if selected_product:
        print(f'''
                \n Product Name: {selected_product.product_name}
                \r Price: ${selected_product.product_price / 100}
                \r Quantity: {selected_product.product_quantity}
                \r Last Updated: {selected_product.date_updated}
                \r {selected_product.brand}''')
        input('Press enter to continue. ')
        sub_choice = submenu()
        if sub_choice == "e":
            selected_product.product_name = edit_product_check('Product', selected_product.product_name)
            selected_product.product_price = edit_product_check('Price', selected_product.product_price)
            selected_product.product_quantity = edit_product_check('Quantity', selected_product.product_quantity)
            selected_product.date_updated = edit_product_check('Last Updated', selected_product.date_updated)
            selected_product.price = edit_product_check('Brand', selected_product.brand)
            session.add(selected_product)
            session.commit()
            print("Product Updated!")
            input('Press enter to return to the menu.')
        elif sub_choice == "d":
            session.delete(selected_product)
            session.commit()
            print("Product deleted!")
            input("Press enter to return to the main menu")
    else:
        print("Product not found.")


def product_analysis():
    most_expensive = session.query(Product).order_by(Product.product_price.desc()).first()
    print(f'''Most Expensive: 
    Product Name:{most_expensive.product_name}, Quantity: {most_expensive.product_quantity},
    Price: ${most_expensive.product_price / 100}, Date Updated: {most_expensive.date_updated},
    Brand: {most_expensive.brand}''')
    # Least expensive item
    least_expensive = session.query(Product).order_by(Product.product_price.asc()).first()
    print(f'''Least Expensive: 
    Product Name:{least_expensive.product_name}, Quantity: {least_expensive.product_quantity},
    Price: ${least_expensive.product_price / 100}, Date Updated: {least_expensive.date_updated}
    Brand: {least_expensive.brand}''')
    # brand with most products
    popular_brand = (session.query(Brands.brand_name, func.count(Product.id).label('product_count'))
                     .join(Brands).group_by(Brands.brand_name).order_by(func.count(Product.id).desc()).first())
    print(f'''Most Popular Brand: {popular_brand.brand_name}''')
    # Average price of products
    average_price = session.query(func.avg(Product.product_price)).scalar()
    print(f'''Average Price: £{round(average_price, 2)}''')
    # Total number of products
    total_number_products = session.query(Product).count()
    print(f'''Total Number of Products: {total_number_products}''')
    # Total quantity of inventory
    total_inventory_quantity = session.query(func.sum(Product.product_quantity)).scalar()
    print(f'''Total Inventory Quantity: {total_inventory_quantity}''')
    # Total value of inventory
    total_inventory_value = session.query(func.sum(Product.product_price)).scalar()
    print(f'''Total Inventory Value: £{total_inventory_value}''')
    # Most recently updated item
    input("Press enter to continue.")


def backup_database():
    choice = input("Are you sure you wish to backup the database? Y/N ").lower()
    if choice == "y":
        with open("backup_inventory.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            field = ["product_name", "product_price", "product_quantity", "date_updated", "brand_name"]
            writer.writerow(field)
            products = session.query(Product).all()

            for product in products:
                brand_name = product.brand.brand_name if product.brand else ''
                formated_date = datetime.datetime.strptime(product.date_updated, "%Y-%m-%d").strftime("%m/%d/%Y")
                row = [
                    product.product_name,
                    f"${float(product.product_price) / 100:.2f}",
                    product.product_quantity,
                    formated_date,
                    brand_name
                ]
                writer.writerow(row)
            session.commit()

            with open("backup_brands.csv", "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                field = ["brand_name"]
                writer.writerow(field)
                brands = session.query(Brands).all()
                for brand in brands:
                    row = [
                        brand.brand_name
                    ]
                    writer.writerow(row)
                session.commit()
            print("Backup successful.")


def app():
    app_running = True
    while app_running:
        choice = main_menu()
        if choice == "v":
            view_product()
        elif choice == "n":
            add_new_product()
        elif choice == "a":
            product_analysis()
        elif choice == "b":
            backup_database()
        else:
            app_running = False
            print("Exiting programme")


if __name__ == '__main__':
    Base.metadata.create_all(engine)
    add_brands_csv()
    add_inventory_csv()
    app()
