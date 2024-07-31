import tkinter as tk
from tkinter import PhotoImage

def update_image_and_entry(*args):
    # Get the current option selected from the list
    selected_drug = drug_var.get()
    
    # Update the image displayed in the label based on the selected drug
    if selected_drug == 'Drug 1':
        image_label.config(image=image1)
    elif selected_drug == 'Drug 2':
        image_label.config(image=image2)
    elif selected_drug == 'Drug 3':
        image_label.config(image=image3)

def calculate_dose():
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

# Create an OptionMenu widget
drugs = ['Drug 1', 'Drug 2', 'Drug 3']
option_menu = tk.OptionMenu(root, drug_var, *drugs)
option_menu.pack()

# Load the images
image1 = PhotoImage(file='AMOXICILLIN-SODIUM-INJECTION.png')
image2 = PhotoImage(file='microsoftteams-image_1.png')
image3 = PhotoImage(file='4db46eec7435e17e7aeafd8092bb1110_large.png')


# Create a Label to display the image
image_label = tk.Label(root, image=image1)
image_label.pack()

# Create an Entry widget for input
input_label = tk.Label(root, text="Enter value:")
input_label.pack()
input_entry = tk.Entry(root)
input_entry.pack()

# Create a Button to calculate the dose
calculate_button = tk.Button(root, text="Calculate Dose", command=calculate_dose)
calculate_button.pack()

# Create a Label to display the dose output
dose_output = tk.Label(root, text="Dose: ")
dose_output.pack()

# Define dosage factors for each drug
dosage_factor = {
    'Drug 1': 10.0,
    'Drug 2': 20.0,
    'Drug 3': 30.0
}

# Trace the variable to call update_image_and_entry whenever it changes
drug_var.trace_add('write', update_image_and_entry)

root.mainloop()
