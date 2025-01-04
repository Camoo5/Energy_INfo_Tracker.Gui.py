from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

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
        content = f"Title: {title}\n\nKey Content:\n\n"
        content += "\n\n".join(key_paragraphs)  # Add extra newline for readability

        return content
    except requests.exceptions.RequestException as e:
        return f"Error: Unable to fetch data - {e}"
    except Exception as e:
        return f"Error: Parsing error - {e}"

@app.route('/')
def index():
    return render_template('index.html', information_for_consumers=information_for_consumers, environmental_schemes=environmental_schemes)

@app.route('/fetch', methods=['POST'])
def fetch():
    category = request.form.get('category')
    option = request.form.get('option')
    if category == "consumers":
        url = information_for_consumers.get(option)
    elif category == "schemes":
        url = environmental_schemes.get(option)
    else:
        url = None
    data = fetch_data(url) if url else "Invalid option selected."
    return render_template('index.html', data=data, 
                        information_for_consumers=information_for_consumers, 
                        environmental_schemes=environmental_schemes)


if __name__ == '__main__':
    app.run(debug=True)
