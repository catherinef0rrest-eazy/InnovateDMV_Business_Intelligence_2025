import requests
import json
import os

# Arlington County, Virginia (state: 51, county: 013)
# QWI API endpoint for employment data with time period
base_url = "https://api.census.gov/data/timeseries/qwi/se?get=Emp,Sep,HirA&for=county:013&in=state:51&key=a19b29f73f2fb20843c8e5835a8d4c85c18467e4"

def fetch_qwi_data():
    """Fetch QWI data for Arlington County with time periods"""
    try:
        print("Fetching Quarterly Workforce Indicators data for Arlington County, VA...")
        
        # Try different time periods
        time_periods = ["2023-Q1", "2023-Q2", "2023-Q3", "2023-Q4", "2022-Q4"]
        all_data = []
        
        for period in time_periods:
            url = f"{base_url}&time={period}"
            print(f"Fetching data for {period}...")
            
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if data and len(data) > 1:
                    all_data.extend(data[1:])  # Skip header row
                    print(f"✅ Successfully fetched {len(data)-1} records for {period}")
                else:
                    print(f"⚠️  No data for {period}")
            else:
                print(f"❌ Failed for {period}: {response.status_code}")
        
        if all_data:
            # Add header row
            headers = ['Emp', 'Sep', 'HirA', 'time', 'county', 'state']
            all_data.insert(0, headers)
            
            # Save raw data
            with open('arlington_qwi_response.json', 'w') as file:
                json.dump(all_data, file, indent=2)
            
            print(f"\n✅ Successfully fetched QWI data: {len(all_data)-1} total records")
            print("Headers:", headers)
            return all_data
        else:
            print("❌ No data was successfully fetched")
            return None
        
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
        with open('arlington_qwi_response.json', 'r') as file:
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
        with open('arlington_qwi_response_proper.json', 'w') as file:
            json.dump(json_objects, file, indent=2)
        
        print(f"Converted {len(json_objects)} records to proper JSON format")
        print("Headers:", headers)
        
    except Exception as e:
        print(f"Error converting to proper JSON: {e}")

def main():
    print("=" * 60)
    print("QUARTERLY WORKFORCE INDICATORS DATA FETCHER")
    print("Arlington County, Virginia (Corrected)")
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