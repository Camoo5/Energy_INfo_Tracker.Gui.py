from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
from flask_caching import Cache

app = Flask(__name__)

# Configuration for caching
app.config['CACHE_TYPE'] = 'SimpleCache'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300
cache = Cache(app)

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
@cache.memoize()
def fetch_data(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the title
        title = soup.title.string.strip() if soup.title else "No Title Available"

        # Extract paragraphs and filter key paragraphs
        paragraphs = [p.get_text(strip=True) for p in soup.find_all('p')]
        key_paragraphs = [p for p in paragraphs if len(p) > 50 and any(keyword in p.lower() for keyword in ['energy', 'advice', 'bill', 'price', 'usage'])]

        # Combine data with readable key paragraphs, including links and formatting
        content = f"<strong>Title:</strong> {title}<br><br><strong>Key Content:</strong><br><br>"
        content += "<br><br>".join(f"<p>{p}</p>" for p in key_paragraphs)

        return content
    except requests.exceptions.RequestException as e:
        return f"<strong>Error:</strong> Unable to fetch data - {e}"
    except Exception as e:
        return f"<strong>Error:</strong> Parsing error - {e}"

@app.route('/')
def index():
    return render_template('index.html', 
    information_for_consumers=information_for_consumers, 
    environmental_schemes=environmental_schemes)

@app.route('/fetch', methods=['POST'])
def fetch():
    try:
        request_data = request.get_json()  # Parse JSON data
        if not request_data:
            return jsonify({"error": "Invalid input. JSON data is required."}), 415

        category = request_data.get('category')
        option = request_data.get('option')

        if category == "consumers":
            url = information_for_consumers.get(option)
        elif category == "schemes":
            url = environmental_schemes.get(option)
        else:
            return jsonify({"error": "Invalid category selected."}), 400

        if url:
            data = fetch_data(url)
            return jsonify({"data": data})
        else:
            return jsonify({"error": "Invalid option selected."}), 400
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route('/shutdown', methods=['POST'])
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Server shutting down...'

if __name__ == '__main__':
    app.run(debug=True)
