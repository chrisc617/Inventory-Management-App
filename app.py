import csv
import os

def menu(username="@prof-rossetti", products_count=100):
    # this is a multi-line string, also using preceding `f` for string interpolation
    menu = f"""
    -----------------------------------
    INVENTORY MANAGEMENT APPLICATION
    -----------------------------------
    Welcome {username}!
    There are {products_count} products in the database.
        operation | description
        --------- | ------------------
        'List'    | Display a list of product identifiers and names.
        'Show'    | Show information about a product.
        'Create'  | Add a new product.
        'Update'  | Edit an existing product.
        'Destroy' | Delete an existing product.
        'Reset'   | Reset the inventory list back to default
    Please select an operation: """ # end of multi- line string. also using string interpolation
    return menu

def read_products_from_file(filename="products.csv"):
    filepath = os.path.join(os.path.dirname(__file__), "db", filename)
    print(f"READING PRODUCTS FROM FILE: '{filepath}'")
    products = []
#
#
    with open(filepath, "r") as csv_file:
        reader = csv.DictReader(csv_file) # assuming your CSV has headers, otherwise... csv.reader(csv_file)
        for row in reader:
            # print(row["name"], row["price"])
            products.append(dict(row))

    return products
#
def write_products_to_file(filename="products.csv", products=[]):
    filepath = os.path.join(os.path.dirname(__file__), "db", filename)
    # print(f"OVERWRITING CONTENTS OF FILE: '{filepath}' \n ... WITH {len(products)} PRODUCTS")
    with open(filepath, "w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["id", "name", "aisle", "department", "price"])
        writer.writeheader()
        for product in products:
            writer.writerow(product)

def reset_products_file(filename="products.csv", from_filename="products_default.csv"):
    print("RESETTING DEFAULTS")
    products = read_products_from_file(from_filename)
    print('THERE ARE NOW '+str(len(products))+' PRODUCTS IN INVENTORY')
    write_products_to_file(filename, products)

def is_valid_price(my_price):
    try:
        float(my_price)
        return True
    except Exception as e:
        return False

def new_prod_id(products):
    if len(products)==0:
        return 1
    else:
        new_prod=[int(p['id']) for p in products]
        return max(new_prod)+1

def run():
    # First, read products from file...
    products = read_products_from_file()

    # Then, prompt the user to select an operation...
    print(menu(username="@some-user")) #TODO instead of printing, capture user input

    # Then, handle selected operation: "List", "Show", "Create", "Update", "Destroy" or "Reset"...
    #TODO: handle selected operation

    # Finally, save products to file so they persist after script is done...
    write_products_to_file(products=products)



# # only prompt the user for input if this script is run from the command-line
# # this allows us to import and test this application's component functions


    choice=input(menu('Chris',str(len(read_products_from_file()))))
    choice=choice.title()
    filename="products.csv"
    filepath = os.path.join(os.path.dirname(__file__), "db", filename)
    if choice=='List':
        print('-----------------')
        print('LISTING ' + str(len(read_products_from_file()))+' PRODUCTS')
        print('-----------------')
        for row in products:
            print('#'+str(row['id']),row['name'])


    elif choice =='Show':
        show_what=input('Please input Product ID to see product details: ')
        try:
            matching_products=[p for p in products if int(p['id'])==int(show_what)]
            matching_product=matching_products[0]
            print('-------------------------------------------------------')
            print('SHOWING PROD ID '+str(matching_product['id'])+' DETAILS BELOW')
            print(matching_product)
            print('-------------------------------------------------------')
        except IndexError:
            print('Product Not Found')



    elif choice=='Create':

        name_input=input('OK. Please input the name of the product: ')
        aisle_input=input('OK. Please input the product aisle: ')
        department_input=input('OK. Please input the product department: ')
        #
        try:
            price_input=float(input('OK. Please input the product price: '))
        except ValueError:
            print('Not a Valid Price')
            price_input=False

        if price_input!=False:
            products1={"id": new_prod_id(products),
                       "name": name_input,
                       "aisle": aisle_input,
                       "department": department_input,
                       'price': str("{0:.2f}".format(float(price_input)))}
            products.append(products1)
            write_products_to_file(filename, products)
            print('-------------------------------------------------------')
            print('NEW PRODUCT CREATED')
            print(products1)
            print('-------------------------------------------------------')



    elif choice=='Update':

        update_what=int(input('Please input Product ID that you want to update: '))
        try:
            matching_products=[p for p in products if int(p['id'])==update_what]
            matching_product=matching_products[0]
            name_input=input('OK. Current name of the product is ' +matching_product['name']+'\nPlease input the new name: ')
            aisle_input=input('OK. Current aisle of the product is ' +matching_product['aisle']+'\nPlease input the new aisle: ')
            department_input=input('OK. Current department of the product is ' +matching_product['department']+'\nPlease input the new department: ')
            price_input=input('OK. Current price of the product is ' +matching_product['price']+'\nPlease input the new price (All prices will be reformatted to two decimal places to the right of the decimal): ')
            while is_valid_price(price_input)==True:
                matching_product['name']=name_input
                matching_product['aisle']=aisle_input
                matching_product['department']=department_input
                matching_product['price']=str("{0:.2f}".format(float(price_input)))
                print('-------------------------------------------------------')
                print('UPDATED PRODUCT DETAILS')
                print(matching_product)
                print('-------------------------------------------------------')

                for p in products:
                    if int(p['id'])==int(matching_product['id']):
                        p=matching_product
                        write_products_to_file(filename, products)
                break
            else:
                print("Not a valid price")

        except IndexError:
            print('Product Not Found')
    elif choice=="Destroy":
        destroy_what=int(input('Please input Product ID that you wish to destroy: '))
        try:
            matching_products=[p for p in products if int(p['id'])==int(destroy_what)]
            matching_product=matching_products[0]
            print('-----------------')
            print('DESTROYING '+matching_product['name'])
            print('-----------------')


            del products[products.index(matching_product)]
            write_products_to_file(filename, products)
        except IndexError:
            print('Product Not Found')
    elif choice=="Reset":
        reset_products_file()

    else:
        print('NOT A VALID CHOICE')
if __name__ == "__main__":
    run()
