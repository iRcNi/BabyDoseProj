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
ser = serial.Serial(port='/dev/ttyUSB0', baudrate=9600)

# Create the Tkinter application
root = tk.Tk()
root.title("Dosage Calculator")

# Create a StringVar to hold the severity level
severity_var = tk.StringVar(root)
severity_var.set('Mild')  # Default severity

# Load and resize the image for the drug
def load_and_resize_image(path, size):
    image = Image.open(path)
    image = image.resize(size, Image.ANTIALIAS)
    return ImageTk.PhotoImage(image)

drug_image_resized = load_and_resize_image('AMOXICILLIN-IMAGE.png', (200, 200))

# Create a Label to display the drug image
image_label = tk.Label(root, image=drug_image_resized)
image_label.pack()

# Create a Label to display the weight
weight_label = tk.Label(root, text="Weight: ")
weight_label.pack()

# Create a StringVar to hold the weight value
weight_var = tk.StringVar(root)

# Create a StringVar to display the net weight (tared weight)
weight_display_var = tk.StringVar(root)
weight_display = tk.Label(root, textvariable=weight_display_var)
weight_display.pack()

# Create a Button to tare the weight
tare_button = tk.Button(root, text="Tare Weight", command=tare_weight_function)
tare_button.pack()

# Create a Label to display the tare weight
tare_output = tk.Label(root, text="Tare Weight: 0.00 kg")
tare_output.pack()

# Create a Label to display the dose output
dose_output = tk.Label(root, text="Dose: ")
dose_output.pack()

# Create RadioButtons for severity levels (now 4 options)
severity_label = tk.Label(root, text="Select Severity:")
severity_label.pack()

severity_frame = tk.Frame(root)
severity_frame.pack()

mild_button = tk.Radiobutton(severity_frame, text="Mild", variable=severity_var, value="Mild", command=calculate_dose)
mild_button.pack(side=tk.LEFT)

moderate_button = tk.Radiobutton(severity_frame, text="Moderate", variable=severity_var, value="Moderate", command=calculate_dose)
moderate_button.pack(side=tk.LEFT)

severe_button = tk.Radiobutton(severity_frame, text="Severe", variable=severity_var, value="Severe", command=calculate_dose)
severe_button.pack(side=tk.LEFT)

critical_button = tk.Radiobutton(severity_frame, text="Critical", variable=severity_var, value="Critical", command=calculate_dose)
critical_button.pack(side=tk.LEFT)

# Define dosage factors for each severity level
dosage_factor = {
    'Mild': 10.0,
    'Moderate': 15.0,
    'Severe': 20.0,
    'Critical': 25.0,
}

# Trace the variable to call calculate_dose whenever it changes
severity_var.trace('w', calculate_dose)

# Start a separate thread to read from the serial port
serial_thread = threading.Thread(target=read_serial, daemon=True)
serial_thread.start()

root.mainloop()
