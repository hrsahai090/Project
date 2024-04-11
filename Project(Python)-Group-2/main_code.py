import mysql.connector
from datetime import datetime
import uuid
import random
from database import DB_HOST, DB_USER, DB_PASSWORD, DB_DATABASE

conn = mysql.connector.connect(
    host = DB_HOST,
    user = DB_USER,
    password = DB_PASSWORD,
    database = DB_DATABASE
)

cursor = conn.cursor()
def clear():
    for _ in range(10):
        print()
                
# Function to handle user registration
def register_user():
    name = input("\nEnter Your Name: ")
    mobile_number = input("\nPlease Enter your mobile number: ")
    parking_sticker = str(uuid.uuid4().hex)[:4]  # Generating an 4-character parking sticker
    sql = 'INSERT INTO user_info(name, mobile_number, parking_sticker) VALUES (%s, %s, %s)'
    cursor.execute(sql, (name, mobile_number, parking_sticker))
    conn.commit()
    # Fetch the ID of the user
    cursor.execute('SELECT LAST_INSERT_ID()')
    user_id = cursor.fetchone()[0]
    print("User Login successful")
    print('Your User ID:', user_id)
    print('Your Parking Sticker Number:', parking_sticker)
    wait = input('\n\nPress any key to continue...')

# Function to add new parking entry
def add_parking_entry():
    user_id= input("\nEnter Your ID:")
    vehicle_number = input("\nEnter your Vehicle registration Number: ")
    vehicle_type = input("Enter your vehicle type: \n 1.2W,\n 2.4W,\n 3.Truck,\n 4.Physically Disabled. :")
    entry_time = datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')
    sql = 'INSERT INTO vehicles (user_id, vehicle_number, vehicle_type, entry_time) VALUES ({},"{}","{}","{}");'.format(user_id, vehicle_number, vehicle_type, entry_time)
    cursor.execute(sql)
    print("Vehicle Added successfully.")
    conn.commit()
    wait = input('\n\nPress any key to continue...')

# Function to update parking exit details
def update_parking_exit():
    # Get vehicle number from the user
    vehicle_number = input("Enter your vehicle number: ")
    # Check if the vehicle exists and exit time is not already set
    sql_check = 'SELECT * FROM vehicles WHERE vehicle_number = %s AND entry_time is NOT NULL and exit_time IS NULL;'
    cursor.execute(sql_check, (vehicle_number,))
    result = cursor.fetchone()

    if result:
        # Calculate parking duration and charges
        entry_time = result[4]  # Assuming entry time is stored in the fifth column
        exit_time = datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')
        parking_duration = exit_time - entry_time

        vehicle_type = result[3]  # Assuming vehicle type is stored in the fourth column
        charges = calculate_charges(vehicle_type, parking_duration)

        # Display total amount to be paid
        print("Total amount to be paid: {}".format(charges))

        # Ask for payment mode
        payment_mode = input("Enter payment mode (Cash/Card/Wallet/UPI): ")
         
        #random receipt number generator
        receipt_number = ''.join(random.choices('0123456789', k=4))
        
        # Update exit time in the vehicles table
        sql_exit = "UPDATE vehicles SET exit_time = %s WHERE vehicle_number = %s and entry_time is NOT NULL AND exit_time IS NULL;"
        cursor.execute(sql_exit, (exit_time, vehicle_number))
        conn.commit()

        # Direct the user to the payment function
        make_payment(vehicle_type, payment_mode, "Hourly", receipt_number, charges)
    else:
        print("Vehicle with vehicle number {} is not parked or already exited.".format(vehicle_number))

def calculate_charges(vehicle_type, parking_duration):
    # Define parking charges based on vehicle type
    charges_per_hour = {
        '2W': 100,
        '4W': 150,
        'Truck': 200,
        'Physically Disabled': 20
    }

    # Calculate charges based on parking duration and vehicle type
    charges_per_hour = charges_per_hour.get(vehicle_type, 0)
    total_hours = parking_duration.total_seconds() / 3600
    charges = total_hours * charges_per_hour

    return charges

# Function to handle payment
def make_payment(vehicle_type, payment_mode, charges_type,receipt_number, charges):
    # Insert payment details into the database
    sql = "INSERT INTO payment (vehicle_type, Payment_mode, charges_type,receipt_number, charges) VALUES (%s, %s, %s, %s,%s)"
    cursor.execute(sql, (vehicle_type, payment_mode, charges_type,receipt_number, charges))
    conn.commit()    
    print("Your receipt number is:{}".format(receipt_number))
    print("Payment successful. Thank you for using our parking system!")
    wait = input('\n\nPress any key to continue...')


# Function to generate daily collection report
def daily_collection_report():
    date = input('Enter date for daily collection report (yyyy-mm-dd): ')
    sql = """
    SELECT SUM(p.charges)
    FROM payment p
    JOIN vehicles v ON p.vehicle_type = v.vehicle_type
    WHERE DATE(v.entry_time) = %s
    """
    cursor.execute(sql, (date,))
    result = cursor.fetchone()
    clear()
    print(f'Daily Collection Report for {date}')
    print('-' * 50)
    print(f'Total Collection: {result[0]}')
    wait = input('\n\nPress any key to continue...')


# Function to generate availability report
def availability_report():
    sql = "SELECT vehicle_type, COUNT(*) FROM vehicles WHERE exit_time IS NULL GROUP BY vehicle_type"
    cursor.execute(sql)
    results = cursor.fetchall()
    clear()
    print('Availability Report')
    print('-' * 50)
    for row in results:
        print(f'{row[0]}: {row[1]}')
    wait = input('\n\nPress any key to continue...')

def main_menu():
    while True:
        clear()
        print('Parking Management System')
        print('1. Register New User')
        print('2. Add Parking Entry')
        print('3. Update Parking Exit')
        print('4. Daily Collection Report')
        print('5. Availability Report')
        print('6. Exit ')
        choice = input('Enter your choice (1-6): ')

        if choice == '1':
            register_user()
           
        elif choice == '2':
            add_parking_entry()
            
        elif choice == '3':
            update_parking_exit()
            
        elif choice == '4':
            daily_collection_report()
            
        elif choice == '5':
            availability_report()

        elif choice == '6':
            break

        else:
            print('Invalid choice.')

if __name__ == "__main__":
    main_menu()
    
cursor.close()
conn.close()
