import tkinter as tk
from tkinter import Label
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime, timedelta
import mysql.connector
import uuid
import random
import mysql_data
from PIL import Image, ImageTk


class ParkingSystem(tk.Tk):
    def __init__(self):
        super().__init__()
        # Database connection
        mysql_data.sql_data(self)
        self.cursor = self.conn.cursor()
        
        self.title("Parking Management System")
        self.geometry("1920x1080")
        
        self.bg_image = Image.open("park.jpg")
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = tk.Label(self, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=2, relheight=4)

        self.main_frame = tk.Frame(self)
        self.main_frame.pack(padx=15, pady=15)
        
        button_font = ('Helvetica', 14)
        button_padx = 20
        button_pady = 10

        self.register_button = tk.Button(self.main_frame, text="User Registration", command=self.register_user,font=button_font)
        self.register_button.grid(row=0, column=0, padx=button_padx, pady=button_pady)

        self.add_entry_button = tk.Button(self.main_frame, text="Add Parking Vehicle ", command=self.add_parking_entry,font=button_font)
        self.add_entry_button.grid(row=1, column=0, padx=button_padx, pady=button_pady)

        self.exit_button = tk.Button(self.main_frame, text="Exit Parked Vehicle", command=self.update_parking_exit,font=button_font)
        self.exit_button.grid(row=2, column=0, padx=button_padx, pady=button_pady)

        self.daily_report_button = tk.Button(self.main_frame, text=" Collection Report", command=self.daily_collection_report,font=button_font)
        self.daily_report_button.grid(row=0, column=1, padx=button_padx, pady=button_pady)

        self.availability_button = tk.Button(self.main_frame, text="Vehicle Availability", command=self.availability_report,font=button_font)
        self.availability_button.grid(row=1, column=1, padx=button_padx, pady=button_pady)

        self.exit_button = tk.Button(self.main_frame, text="Exit", command=self.destroy,font=button_font)
        self.exit_button.grid(row=2, column=1, padx=button_padx, pady=button_pady)

    def register_user(self):
        def submit():
            name = name_entry.get()
            mobile_number = mobile_entry.get()
            parking_sticker = str(uuid.uuid4().hex)[:4]
            sql = 'INSERT INTO user_info(name, mobile_number, parking_sticker) VALUES (%s, %s, %s)'
            self.cursor.execute(sql, (name, mobile_number, parking_sticker))
            self.conn.commit()
            register_window.destroy()  # Close the registration window
            messagebox.showinfo("Registration Successful", f"Thank you for registering!\nYour ID: {self.cursor.lastrowid}\nYour Parking Sticker : {parking_sticker}")

        register_window = tk.Toplevel(self)
        register_window.title("Register New User")

        name_label = tk.Label(register_window, text="Name:")
        name_label.grid(row=0, column=0, padx=10, pady=5)
        name_entry = tk.Entry(register_window)
        name_entry.grid(row=0, column=1, padx=10, pady=5)

        mobile_label = tk.Label(register_window, text="Mobile Number:")
        mobile_label.grid(row=1, column=0, padx=10, pady=5)
        mobile_entry = tk.Entry(register_window)
        mobile_entry.grid(row=1, column=1, padx=10, pady=5)

        submit_button = tk.Button(register_window, text="Submit", command=submit)
        submit_button.grid(row=2, columnspan=2, padx=10, pady=10)

    def add_parking_entry(self):
        def submit():
            user_id = user_id_entry.get()
            vehicle_number = vehicle_entry.get()
            vehicle_type = vehicle_type_combobox.get()

        # Check if the selected vehicle type is valid
            if vehicle_type not in ["2 Wheeler", "4 wheeler", "Truck/Bus", "Physically Disabled"]:
                messagebox.showerror("Invalid Choice", "Please select your vehicle type from the dropdown.")
                vehicle_type_combobox.focus_set()  # Return focus to the vehicle type combobox
                return

            entry_time = datetime.now()#.strftime('%Y-%m-%d %H:%M:%S')
            sql = 'INSERT INTO vehicles (user_id, vehicle_number, vehicle_type, entry_time) VALUES (%s, %s, %s, %s)'
            self.cursor.execute(sql, (user_id, vehicle_number, vehicle_type, entry_time))
            self.conn.commit()
            user_id_entry.delete(0, tk.END)
            vehicle_entry.delete(0, tk.END)
            vehicle_type_combobox.set('')
            add_entry_window.destroy()  # Close the entry window
            messagebox.showinfo("Success", "Your vehicle is parked successfully.")

        add_entry_window = tk.Toplevel(self)
        add_entry_window.title("Add Parking Entry")

        user_id_label = tk.Label(add_entry_window, text="User ID:")
        user_id_label.grid(row=0, column=0, padx=10, pady=5)
        user_id_entry = tk.Entry(add_entry_window)
        user_id_entry.grid(row=0, column=1, padx=10, pady=5)

        vehicle_label = tk.Label(add_entry_window, text="Vehicle Number:")
        vehicle_label.grid(row=1, column=0, padx=10, pady=5)
        vehicle_entry = tk.Entry(add_entry_window)
        vehicle_entry.grid(row=1, column=1, padx=10, pady=5)

    # Display vehicle charges per hour and minimum parking time information
        charges_info = """
        Vehicle charges per hour:
        2 Wheeler : 100 Rs/hr,
        4 wheeler : 150 Rs/hr,
        Truck/Bus : 200 Rs/hr,
        Physically Disabled : 20 Rs/hr

        Minimum parking time: 30 minutes
        """
        charges_info_label = tk.Label(add_entry_window, text=charges_info, justify='left')
        charges_info_label.grid(row=2, columnspan=2, padx=10, pady=5)

        vehicle_type_label = tk.Label(add_entry_window, text="Vehicle Type:")
        vehicle_type_label.grid(row=3, column=0, padx=10, pady=5)
        vehicle_type_combobox = ttk.Combobox(add_entry_window, values=["2 Wheeler", "4 wheeler", "Truck/Bus", "Physically Disabled"])
        vehicle_type_combobox.grid(row=3, column=1, padx=10, pady=5)

        submit_button = tk.Button(add_entry_window, text="Submit", command=submit)
        submit_button.grid(row=4, columnspan=2, padx=10, pady=10)


    def update_parking_exit(self):
        # Function to submit the parking exit form
        def submit():
            vehicle_number = vehicle_number_entry.get()
            # Check if the vehicle exists and exit time is not already set
            sql_check = 'SELECT * FROM vehicles WHERE vehicle_number = %s AND entry_time is NOT NULL and exit_time IS NULL;'
            self.cursor.execute(sql_check, (vehicle_number,))
            result = self.cursor.fetchone()

            if result:
                # Calculate parking duration and charges
                entry_time = result[4]  # Assuming entry time is stored in the fifth column
                exit_time = datetime.now()#.strftime('%Y-%m-%d %H:%M:%S')
                # Calculate parking duration and charges
                #entry_time = datetime.strptime(entry_time, '%Y-%m-%d %H:%M:%S')
                #exit_time = datetime.strptime(exit_time, '%Y-%m-%d %H:%M:%S')
                parking_duration = exit_time - entry_time

                vehicle_type = result[3]  # Assuming vehicle type is stored in the fourth column
                total_hours = parking_duration.total_seconds() / 3600
                charges = self.calculate_charges(vehicle_type, total_hours)

                # Display total amount to be paid
                messagebox.showinfo("Charges", "Total amount to be paid: {} rupees.".format(charges))

                # Ask for payment mode
                payment_mode = payment_mode_combobox.get()

                # Random receipt number generator
                receipt_number = ''.join(random.choices('0123456789', k=4))

                # Update exit time in the vehicles table
                sql_exit = "UPDATE vehicles SET exit_time = %s WHERE vehicle_number = %s and entry_time is NOT NULL AND exit_time IS NULL;"
                self.cursor.execute(sql_exit, (exit_time, vehicle_number))
                self.conn.commit()

                # Direct the user to the payment function
                self.make_payment(vehicle_type, payment_mode, "Hourly", receipt_number, charges)
            else:
                messagebox.showerror("Error", "Vehicle with vehicle number {} is not parked or already exited.".format(vehicle_number))

        # Create update parking exit window
        update_exit_window = tk.Toplevel(self)
        update_exit_window.title("Update Parking Exit")

        # Vehicle number entry
        vehicle_number_label = tk.Label(update_exit_window, text="Vehicle Number:")
        vehicle_number_label.grid(row=0, column=0, padx=10, pady=5)
        vehicle_number_entry = tk.Entry(update_exit_window)
        vehicle_number_entry.grid(row=0, column=1, padx=10, pady=5)

        # Payment mode entry
        payment_mode_label = tk.Label(update_exit_window, text="Payment Mode:")
        payment_mode_label.grid(row=1, column=0, padx=10, pady=5)
        payment_mode_combobox = ttk.Combobox(update_exit_window, values=["Cash", "Card", "Wallet", "UPI"])
        payment_mode_combobox.grid(row=1, column=1, padx=10, pady=5)

        # Submit button
        submit_button = tk.Button(update_exit_window, text="Submit", command=submit)
        submit_button.grid(row=2, columnspan=2, padx=10, pady=10)

    # Function to calculate charges
    def calculate_charges(self,vehicle_type,total_hours):
        # Define parking charges based on vehicle type
        charges_per_hour = {
            '2W': 100,
            '4W': 150,
            'Truck': 200,
            'Physically Disabled': 20
        }

        # Get charges per hour for the given vehicle type
        charges_per_hour = charges_per_hour.get(vehicle_type,0)

        # Minimum parking duration in minutes
        minimum_duration_minutes = 30

        # Check if parking duration is less than 30 minutes
        if total_hours * 60 < minimum_duration_minutes:
            # If parking duration is less than 30 minutes, charge for 1 hour
            total_hours = 1

        # Calculate total charges
        charges = total_hours * charges_per_hour

        return charges
    
    # Function to handle payment
    def make_payment(self, vehicle_type, payment_mode, charges_type, receipt_number, charges):
        # Insert payment details into the database
        sql = "INSERT INTO payment (vehicle_type, Payment_mode, charges_type, receipt_number, charges) VALUES (%s, %s, %s, %s, %s)"
        self.cursor.execute(sql, (vehicle_type, payment_mode, charges_type, receipt_number, charges))
        self.conn.commit()
        messagebox.showinfo("Payment Successful", f"Your receipt number is: {receipt_number}\nPayment successful. Thank you for using our parking system!")    
        
        
    def daily_collection_report(self):
        def generate_report():
            date = date_entry.get()
            sql = """
            SELECT SUM(p.charges)
            FROM payment p
            JOIN vehicles v ON p.vehicle_type = v.vehicle_type
            WHERE DATE(v.entry_time) = %s
            """
            self.cursor.execute(sql, (date,))
            result = self.cursor.fetchone()
            report_text.config(state="normal")
            report_text.delete("1.0", "end")
            report_text.insert("1.0", f'Daily Collection Report for {date}\n')
            report_text.insert("end", '-' * 50 + '\n')
            report_text.insert("end", f'Total Collection: {result[0]} rupees\n')
            report_text.config(state="disabled")

        report_window = tk.Toplevel(self)
        report_window.title("Daily Collection Report")

        date_label = tk.Label(report_window, text="Enter date for collection report (yyyy-mm-dd):")
        date_label.grid(row=0, column=0, padx=10, pady=5)
        date_entry = tk.Entry(report_window)
        date_entry.grid(row=0, column=1, padx=10, pady=5)

        generate_report_button = tk.Button(report_window, text="Click to Generate Report", command=generate_report)
        generate_report_button.grid(row=1, columnspan=2, padx=10, pady=10)

        report_text = tk.Text(report_window, height=10, width=50)
        report_text.grid(row=2, columnspan=2, padx=10, pady=5)

    def availability_report(self):
        def generate_report():
            sql = "SELECT vehicle_type, COUNT(*) FROM vehicles WHERE exit_time IS NULL GROUP BY vehicle_type"
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            availability_text.config(state="normal")
            availability_text.delete("1.0", "end")
            availability_text.insert("1.0", 'Availability Report\n')
            availability_text.insert("end", '-' * 50 + '\n')
            for row in results:
                availability_text.insert("end", f'{row[0]}: {row[1]}\n')
            availability_text.config(state="disabled")

        report_window = tk.Toplevel(self)
        report_window.title("Availability Report")

        availability_text = tk.Text(report_window, height=10, width=50)
        availability_text.grid(row=0, columnspan=2, padx=10, pady=5)

        generate_report_button = tk.Button(report_window, text="Click to check Availability Report", command=generate_report)
        generate_report_button.grid(row=1, columnspan=2, padx=10, pady=10)


if __name__ == "__main__":
    app = ParkingSystem()
    app.mainloop()
