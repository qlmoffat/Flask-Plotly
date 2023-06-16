import json

# Function to generate market size data for a given category, years, and values
def generate_market_size(category, years, values):
    market_size = {
        "researchYear": max(years),
        "geographyId": 1,
        "geographyName": "United States",
        "categoryId": category["categoryId"],
        "categoryName": category["categoryName"],
        "industry": category["industry"],
        "dataTypeId": 1,
        "dataType": "Revenue",
        "unitName": category["unitName"],
        "inflationType": "Adjusted",
        "exchangeRateName": "USD",
        "perCapitaName": "Per Capita",
        "unitMultiplier": 1,
        "data": []
    }

    for year, value in zip(years, values):
        data_entry = {
            "year": year,
            "value": value
        }
        market_size["data"].append(data_entry)

    return market_size

# Configuration options
categories = [
    {
        "categoryId": 1,
        "categoryName": "Cheese",
        "industry": "Food and Beverage",
        "unitName": "Million USD"
    },
    {
        "categoryId": 2,
        "categoryName": "Chocolate",
        "industry": "Food and Beverage",
        "unitName": "Million USD"
    },
    {
        "categoryId": 3,
        "categoryName": "Mobile Phones",
        "industry": "Electronics",
        "unitName": "Million USD"
    },
    {
        "categoryId": 4,
        "categoryName": "Cars",
        "industry": "Automotive",
        "unitName": "Billion USD"
    }
]

countries = [
    {
        "geographyId": 1,
        "geographyName": "United States"
    },
    {
        "geographyId": 2,
        "geographyName": "United Kingdom"
    },
    {
        "geographyId": 3,
        "geographyName": "Germany"
    },
    {
        "geographyId": 4,
        "geographyName": "France"
    },
    {
        "geographyId": 5,
        "geographyName": "Italy"
    }
]

years = [2020, 2021, 2022]
values = [
    [200.0, 220.0, 240.0],   # Cheese
    [400.0, 420.0, 440.0],   # Chocolate
    [1500.0, 1600.0, 1700.0],   # Mobile Phones
    [300.0, 310.0, 320.0]    # Cars
]

# Generate market size data for each category and country
market_sizes = []
for category in categories:
    for country in countries:
        market_size = generate_market_size(category, years, values[category["categoryId"] - 1])
        market_size["geographyId"] = country["geographyId"]
        market_size["geographyName"] = country["geographyName"]
        market_sizes.append(market_size)

# Create JSON object
data = {
    "offset": 0,
    "limit": 0,
    "total": 0,
    "marketSizes": market_sizes
}

# Write JSON data to a file
file_path = "./market_size.json"
with open(file_path, "w") as json_file:
    json.dump(data, json_file)
