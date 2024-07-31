import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk

def update_image_and_entry(selected_drug):
    # Update the image displayed in the label based on the selected drug
    if selected_drug == 'Drug 1':
        image_label.config(image=image1_resized)
    elif selected_drug == 'Drug 2':
        image_label.config(image=image2_resized)
    elif selected_drug == 'Drug 3':
        image_label.config(image=image3_resized)
    
    # Set the selected drug
    drug_var.set(selected_drug)
    # Calculate the dose
    calculate_dose()

def calculate_dose(*args):
    # Get the current option selected from the list
    selected_drug = drug_var.get()
    # Get the input value
    input_value = input_entry.get()
    
    # Perform dose calculation based on the selected drug and input value
    try:
        dose = float(input_value) * dosage_factor[selected_drug]
        dose_output.config(text=f'Dose: {dose:.2f} mg')
    except ValueError:
        dose_output.config(text='Invalid input! Please enter a number.')

root = tk.Tk()
root.title("Dosage Calculator")

# Create a StringVar to hold the current option selected from the list
drug_var = tk.StringVar(root)
drug_var.set('Drug 1')  # Set the default option

# Load the images and resize them
def load_and_resize_image(path, size):
    image = Image.open(path)
    image = image.resize(size)
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

# Create an Entry widget for input
input_label = tk.Label(root, text="Enter value:")
input_label.pack()
input_entry = tk.Entry(root)
input_entry.pack()
input_entry.bind('<KeyRelease>', calculate_dose)  # Calculate dose on key release

# Create a Label to display the dose output
dose_output = tk.Label(root, text="Dose: ")
dose_output.pack()

# Define dosage factors for each drug
dosage_factor = {
    'Drug 1': 10.0,
    'Drug 2': 20.0,
    'Drug 3': 30.0
}

# Trace the variable to call calculate_dose whenever it changes
drug_var.trace('w', calculate_dose)

root.mainloop()
