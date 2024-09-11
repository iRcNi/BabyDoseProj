import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import serial
import threading

# Initialize tare weight
tare_weight = 0.0

# Function to update the image and reset dose calculation based on selected drug
def update_image_and_entry(selected_drug):
    if selected_drug == 'Drug 1':
        image_label.config(image=image1_resized)
    elif selected_drug == 'Drug 2':
        image_label.config(image=image2_resized)
    elif selected_drug == 'Drug 3':
        image_label.config(image=image3_resized)
    
    drug_var.set(selected_drug)
    calculate_dose()

# Function to calculate the dose based on the weight, selected drug, and severity
def calculate_dose(*args):
    selected_drug = drug_var.get()
    selected_severity = severity_var.get()
    try:
        raw_weight = float(weight_var.get())
        net_weight = raw_weight - tare_weight
        weight_display_var.set(f'{net_weight:.2f} kg')
        
        # Calculate the dose based on severity
        dose_ratio = dosage_factor[selected_drug][selected_severity]
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

# Create a StringVar to hold the current option selected from the list
drug_var = tk.StringVar(root)
drug_var.set('Drug 1')  # Set the default option

# Create a StringVar to hold the severity level
severity_var = tk.StringVar(root)
severity_var.set('Mild')  # Default severity

# Load and resize the images
def load_and_resize_image(path, size):
    image = Image.open(path)
    image = image.resize(size, Image.ANTIALIAS)
    return ImageTk.PhotoImage(image)

image1_resized = load_and_resize_image('AMOXICILLIN-IMAGE.png', (200, 200))
image2_resized = load_and_resize_image('IBUPROFEN-IMAGE.png', (200, 200))
image3_resized = load_and_resize_image('TYLENOL-IMAGE.png', (200, 200))

# Create buttons for each drug option
button_frame = tk.Frame(root)
button_frame.pack()

drug1_button = tk.Button(button_frame, text="Drug 1", command=lambda: update_image_and_entry('Drug 1'))
drug1_button.pack(side=tk.LEFT, padx=5)

drug2_button = tk.Button(button_frame, text="Drug 2", command=lambda: update_image_and_entry('Drug 2'))
drug2_button.pack(side=tk.LEFT, padx=5)

drug3_button = tk.Button(button_frame, text="Drug 3", command=lambda: update_image_and_entry('Drug 3'))
drug3_button.pack(side=tk.LEFT, padx=5)

# Create a Label to display the image
image_label = tk.Label(root, image=image1_resized)
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

# Create RadioButtons for severity levels
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

# Define dosage factors for each drug and severity level
dosage_factor = {
    'Drug 1': {'Mild': 10.0, 'Moderate': 15.0, 'Severe': 20.0},
    'Drug 2': {'Mild': 20.0, 'Moderate': 25.0, 'Severe': 30.0},
    'Drug 3': {'Mild': 30.0, 'Moderate': 35.0, 'Severe': 40.0},
}

# Trace the variable to call calculate_dose whenever it changes
drug_var.trace('w', calculate_dose)
severity_var.trace('w', calculate_dose)

# Start a separate thread to read from the serial port
serial_thread = threading.Thread(target=read_serial, daemon=True)
serial_thread.start()

root.mainloop()
