import tkinter as tk
from tkinter import ttk
import requests
from bs4 import BeautifulSoup
import threading

# URLs for Information for Consumers
information_for_consumers = {
    "Energy Advice for Households": "https://www.ofgem.gov.uk/information-consumers/energy-advice-households",
    "Average Gas and Electricity Use": "https://www.ofgem.gov.uk/average-gas-and-electricity-usage",
    "Understanding Your Bills": "https://www.ofgem.gov.uk/understand-your-electricity-and-gas-bills",
    "Energy Price Cap by Region": "https://www.ofgem.gov.uk/information-consumers/energy-advice-households/get-energy-price-cap-standing-charges-and-unit-rates-region",
    "Switching Energy Supplier": "https://www.ofgem.gov.uk/information-consumers/energy-advice-households/switching-energy-supplier",
}

# URLs for Environmental and Social Schemes
environmental_schemes = {
    "Boiler Upgrade Scheme (BUS)": "https://www.ofgem.gov.uk/environmental-and-social-schemes/boiler-upgrade-scheme-bus",
    "Energy Company Obligation (ECO)": "https://www.ofgem.gov.uk/environmental-and-social-schemes/energy-company-obligation-eco",
    "Green Gas Support Scheme and Green Gas Levy": "https://www.ofgem.gov.uk/environmental-and-social-schemes/green-gas-support-scheme-and-green-gas-levy",
    "Counter Fraud for Environmental and Social Programmes": "https://www.ofgem.gov.uk/environmental-and-social-schemes/counter-fraud-environmental-and-social-programmes",
    "Information on Renewables and CHP Register": "https://www.ofgem.gov.uk/environmental-programmes/information-renewables-and-chp-register",
    "Great British Insulation Scheme": "https://www.ofgem.gov.uk/environmental-and-social-schemes/great-british-insulation-scheme",
    "Warm Home Discount (WHD)": "https://www.ofgem.gov.uk/environmental-and-social-schemes/warm-home-discount-whd",
}

# Function to fetch and parse data
def fetch_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the title
        title = soup.title.string.strip() if soup.title else "No Title Available"

        # Extract paragraphs and filter key paragraphs
        paragraphs = [p.get_text(strip=True) for p in soup.find_all('p')]
        key_paragraphs = [p for p in paragraphs if len(p) > 50 and any(keyword in p.lower() for keyword in ['energy', 'advice', 'bill', 'price', 'usage'])]

        # Combine data with readable key paragraphs
        content = f"Title: {title}\n\n"
        content += "\n\n".join([f"    {p}" for p in key_paragraphs])  # Add indentation and spacing between paragraphs

        return content if key_paragraphs else "No relevant content found."
    except requests.exceptions.RequestException as e:
        return f"Error: Unable to fetch data - {e}"
    except Exception as e:
        return f"Error: Parsing error - {e}"

# Function to fetch and display data
def display_data(option, category):
    def fetch_and_show():
        url = category.get(option)
        if url:
            data = fetch_data(url)
            result_text.set(data)
        else:
            result_text.set("Invalid option selected.")
        # Show the result label after data is set
        result_label.grid()
    threading.Thread(target=fetch_and_show).start()

# Function to exit the application
def exit_app():
    app.quit()

# Create the main application window
app = tk.Tk()
app.title("Energy Info Tracker")
app.geometry("900x700")
app.configure(bg="#e6f7ff")  # Light blue background

# Welcome and Introduction Label
introduction_text = """
Welcome to the Energy Info Tracker App!

The Energy Info Tracker App is a user-friendly tool designed to empower energy consumers by providing easy access to critical information about energy usage, pricing, and sustainability. It serves as a centralized platform to educate and inform users about various aspects of energy consumption and related environmental and social initiatives.

Choose an option from the dropdown menus to get started!

**Instructions:**
- **Fetch Data**: Select an option from the dropdown menu and click the "Fetch Data" button to retrieve information.
- **Exit App**:   Click the last button to "Exit App".
"""

introduction_label = tk.Label(
    app,
    text=introduction_text,
    font=("Helvetica", 14),
    bg="#e6f7ff",
    fg="#003366",
    justify="left",
    wraplength=850,
    padx=10,
    pady=10
)
introduction_label.pack(pady=10)

# Scrollable frame setup
main_frame = tk.Frame(app, bg="#e6f7ff")
main_frame.pack(fill=tk.BOTH, expand=1)

# Create canvas and scrollbar for scrollable frame
canvas = tk.Canvas(main_frame, bg="#e6f7ff")
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

scrollable_frame = tk.Frame(canvas, bg="#e6f7ff")
scrollable_frame.bind(
    "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

# Dropdown menu for Information for Consumers
selected_option1 = tk.StringVar(value="Select an option")
dropdown_label1 = tk.Label(
    scrollable_frame,
    text="Information for Consumers:",
    font=("Helvetica", 16, "bold"),
    bg="#e6f7ff",
    fg="#003366"
)
dropdown_label1.grid(row=1, column=0, columnspan=2, pady=10)

dropdown_menu1 = tk.OptionMenu(
    scrollable_frame, selected_option1, *information_for_consumers.keys()
)
dropdown_menu1.config(width=40)
dropdown_menu1["menu"].config(font=("Helvetica", 14))  # Increase font size for options
dropdown_menu1.grid(row=2, column=0, columnspan=2, pady=20)

# Button to fetch data for Information for Consumers
fetch_button1 = ttk.Button(
    scrollable_frame, 
    text="Fetch Data", 
    command=lambda: display_data(selected_option1.get(), information_for_consumers),
    style="Fetch.TButton"
)
fetch_button1.grid(row=3, column=0, columnspan=2, pady=10, padx=5)

# Dropdown menu for Environmental and Social Schemes
selected_option2 = tk.StringVar(value="Select an option")
dropdown_label2 = tk.Label(
    scrollable_frame,
    text="Environmental and Social Schemes:",
    font=("Helvetica", 16, "bold"),
    bg="#e6f7ff",
    fg="#003366"
)
dropdown_label2.grid(row=4, column=0, columnspan=2, pady=10)

dropdown_menu2 = tk.OptionMenu(
    scrollable_frame, selected_option2, *environmental_schemes.keys()
)
dropdown_menu2.config(width=40)
dropdown_menu2["menu"].config(font=("Helvetica", 14))  # Increase font size for options
dropdown_menu2.grid(row=5, column=0, columnspan=2, pady=20)

# Button to fetch data for Environmental and Social Schemes
fetch_button2 = ttk.Button(
    scrollable_frame, 
    text="Fetch Data", 
    command=lambda: display_data(selected_option2.get(), environmental_schemes),
    style="Fetch.TButton"
)
fetch_button2.grid(row=6, column=0, columnspan=2, pady=10, padx=5)

# Text widget for displaying results (initially hidden)
result_text = tk.StringVar()
result_label = tk.Label(
    scrollable_frame,
    textvariable=result_text,
    wraplength=850,
    justify="left",
    font=("Helvetica", 14),  # Larger font size
    bg="#ffffff",  # White background for text
    fg="#333333",  # Dark gray text color
    padx=10,
    pady=10,
    borderwidth=2,
    relief="groove"
)
result_label.grid(row=7, column=0, columnspan=2, pady=10)
result_label.grid_remove()  # Initially hide the label

# Exit App button
exit_button = ttk.Button(
    scrollable_frame, 
    text="Exit App", 
    command=exit_app,
    style="Exit.TButton"
)
exit_button.grid(row=8, column=0, columnspan=2, pady=20, padx=5)

# Styling for buttons
style = ttk.Style()
style.configure("Fetch.TButton", font=("Helvetica", 14, "bold"), foreground="#ffffff", background="#f0f0f0")
style.map("Fetch.TButton", foreground=[("active", "#007acc")], background=[("active", "#3399ff")])  # Change text color on active
style.configure("Exit.TButton", font=("Helvetica", 14, "bold"), foreground="#ffffff", background="#006400")
style.map("Exit.TButton", foreground=[("active", "#228B22")], background=[("active", "#228B22")])  # Change background color to dark green on active

# Run the application
app.mainloop()

