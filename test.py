import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import serial
import threading

# Initialize tare weight
tare_weight = 0.0

# Function to calculate the dose based on the weight and selected severity
def calculate_dose(*args):
    selected_severity = severity_var.get()
    try:
        raw_weight = float(weight_var.get())
        if raw_weight < 20:  # Set minimum weight threshold to 20
            raw_weight = 0  # Display as zero if less than 20
        net_weight = raw_weight - tare_weight
        weight_display_var.set(f'{net_weight:.2f} kg')
        
        # Calculate the dose based on severity
        dose_ratio = dosage_factor[selected_severity]
        dose = net_weight * dose_ratio
        dose_output.config(text=f'Dose: {dose:.2f} mg')
    except ValueError:
        dose_output.config(text='Invalid weight!')


# Function to tare the weight
def tare_weight_function():
    global tare_weight
    try:
        tare_weight = float(weight_var.get())
        tare_output.config(text=f'Tare Weight: {tare_weight:.2f} kg')
        calculate_dose()  # Update dose when taring the weight
    except ValueError:
        tare_output.config(text='Tare Weight: Invalid weight!')

# Function to read weight from serial port
def read_serial():
    while True:
        try:
            weight = ser.readline().decode('utf-8').strip()
            weight_var.set(weight)
            calculate_dose()
        except:
            continue

# Setup serial port
ser = serial.Serial(port='/dev/ttyUSB0', baudrate=57600)

# Create the Tkinter application
root = tk.Tk()
root.title("Dosage Calculator")

# Create a StringVar to hold the weight value
weight_var = tk.StringVar(root)

# Create a StringVar to hold the severity level
severity_var = tk.StringVar(root)
severity_var.set('Mild')  # Default severity

# Create a StringVar to display the net weight (tared weight)
weight_display_var = tk.StringVar(root)

# Create a Label to display the drug image on the left side
image_frame = tk.Frame(root)
image_frame.pack(side=tk.LEFT, padx=10)

# Load and resize the image for the drug
def load_and_resize_image(path, size):
    image = Image.open(path)
    image = image.resize(size, Image.ANTIALIAS)
    return ImageTk.PhotoImage(image)

drug_image_resized = load_and_resize_image('AMOXICILLIN-IMAGE.png', (300, 300))  # Adjusted image size
image_label = tk.Label(image_frame, image=drug_image_resized)
image_label.pack()


# Create a frame for all the text and buttons on the right
info_frame = tk.Frame(root)
info_frame.pack(side=tk.RIGHT, padx=10)

# Create a Label to display the weight input
weight_label = tk.Label(info_frame, text="Weight: ", font=("Arial", 14))
weight_label.pack()

# Create an entry to input the weight
weight_entry = tk.Entry(info_frame, textvariable=weight_var, font=("Arial", 14))
weight_entry.pack()

# Create a Label to display the net weight
weight_display = tk.Label(info_frame, textvariable=weight_display_var, font=("Arial", 14))
weight_display.pack()

# Create a Button to tare the weight
tare_button = tk.Button(info_frame, text="Tare Weight", command=tare_weight_function, font=("Arial", 14))
tare_button.pack()

# Create a Label to display the tare weight
tare_output = tk.Label(info_frame, text="Tare Weight: 0.00 kg", font=("Arial", 14))
tare_output.pack()

# Create a Label to display the dose output
dose_output = tk.Label(info_frame, text="Dose: ", font=("Arial", 14))
dose_output.pack()

# Create buttons for severity levels (now 4 options)
severity_label = tk.Label(info_frame, text="Select Severity:", font=("Arial", 14))
severity_label.pack()

severity_frame = tk.Frame(info_frame)
severity_frame.pack()

mild_button = tk.Button(severity_frame, text="Mild", command=lambda: severity_var.set('Mild'), font=("Arial", 14), width=10)
mild_button.grid(row=0, column=0, padx=5, pady=5)  # First row, first column

moderate_button = tk.Button(severity_frame, text="Moderate", command=lambda: severity_var.set('Moderate'), font=("Arial", 14), width=10)
moderate_button.grid(row=0, column=1, padx=5, pady=5)  # First row, second column

severe_button = tk.Button(severity_frame, text="Severe", command=lambda: severity_var.set('Severe'), font=("Arial", 14), width=10)
severe_button.grid(row=1, column=0, padx=5, pady=5)  # Second row, first column

critical_button = tk.Button(severity_frame, text="Critical", command=lambda: severity_var.set('Critical'), font=("Arial", 14), width=10)
critical_button.grid(row=1, column=1, padx=5, pady=5)  # Second row, second column

# Define dosage factors for each severity level
dosage_factor = {
    'Mild': 0.05,
    'Moderate': 0.1,
    'Severe': 0.15,
    'Critical': 0.2,
}

# Trace the variable to call calculate_dose whenever the weight or severity changes
weight_var.trace('w', calculate_dose)
severity_var.trace('w', calculate_dose)

# Start a separate thread to read from the serial port
serial_thread = threading.Thread(target=read_serial, daemon=True)
serial_thread.start()

root.mainloop()
