import requests
import json
import os

# Washington, DC (state: 11, county: 001)
# QWI API endpoint for employment data
url = "https://api.census.gov/data/timeseries/qwi/se?get=Emp&for=county:001&in=state:11&key=a19b29f73f2fb20843c8e5835a8d4c85c18467e4"

def fetch_qwi_data():
    """Fetch QWI data for Washington, DC"""
    try:
        print("Fetching Quarterly Workforce Indicators data for Washington, DC...")
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # Save raw data
        with open('dc_qwi_response.json', 'w') as file:
            json.dump(data, file, indent=2)
        
        print(f"Successfully fetched QWI data: {len(data)} records")
        if data:
            print("Headers:", data[0])
            print(f"Sample record: {data[1] if len(data) > 1 else 'No data records'}")
        
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching QWI data: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

def convert_to_proper_json():
    """Convert QWI data to proper JSON format"""
    try:
        # Read the raw data
        with open('dc_qwi_response.json', 'r') as file:
            data = json.load(file)
        
        if not data or len(data) < 2:
            print("Not enough data to convert")
            return
        
        # Extract headers (first row)
        headers = data[0]
        
        # Convert array of arrays to array of objects
        json_objects = []
        for row in data[1:]:  # Skip the header row
            obj = {}
            for i, value in enumerate(row):
                if i < len(headers):
                    obj[headers[i]] = value
            json_objects.append(obj)
        
        # Write the converted data to a new file
        with open('dc_qwi_response_proper.json', 'w') as file:
            json.dump(json_objects, file, indent=2)
        
        print(f"Converted {len(json_objects)} records to proper JSON format")
        print("Headers:", headers)
        
    except Exception as e:
        print(f"Error converting to proper JSON: {e}")

def main():
    print("=" * 60)
    print("QUARTERLY WORKFORCE INDICATORS DATA FETCHER")
    print("Washington, DC")
    print("=" * 60)
    
    # Fetch the data
    data = fetch_qwi_data()
    
    if data:
        # Convert to proper JSON format
        convert_to_proper_json()
        print("\n✅ Data fetch and conversion completed successfully!")
    else:
        print("\n❌ Failed to fetch data")

if __name__ == "__main__":
    main() 