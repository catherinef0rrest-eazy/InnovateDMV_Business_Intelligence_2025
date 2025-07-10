import requests
import json
import os

# County configurations: (county_code, state_code, county_name)
counties = [
    ("013", "51", "Arlington County, VA"),
    ("059", "51", "Fairfax County, VA"),
    ("107", "51", "Loudoun County, VA"),
    ("153", "51", "Prince William County, VA"),
    ("031", "24", "Montgomery County, MD"),
    ("033", "24", "Howard County, MD"),
    ("001", "11", "Washington, DC")
]

# 2024 time periods to fetch
time_periods = ["2024-Q1", "2024-Q2", "2024-Q3"]

def fetch_county_qwi_data(county_code, state_code, county_name):
    """Fetch QWI data for a specific county"""
    base_url = f"https://api.census.gov/data/timeseries/qwi/se?get=Emp,Sep,HirA&for=county:{county_code}&in=state:{state_code}&key=a19b29f73f2fb20843c8e5835a8d4c85c18467e4"
    
    all_data = []
    
    for period in time_periods:
        url = f"{base_url}&time={period}"
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if data and len(data) > 1:
                    all_data.extend(data[1:])  # Skip header row
                    print(f"  ✅ {period}: {len(data)-1} records")
                else:
                    print(f"  ⚠️  {period}: No data")
            else:
                print(f"  ❌ {period}: Failed ({response.status_code})")
        except Exception as e:
            print(f"  ❌ {period}: Error - {e}")
    
    if all_data:
        # Add header row
        headers = ['Emp', 'Sep', 'HirA', 'time', 'county', 'state']
        all_data.insert(0, headers)
        
        # Save raw data
        filename = f"{county_name.lower().replace(', ', '_').replace(' ', '_')}_qwi_2024_response.json"
        with open(filename, 'w') as file:
            json.dump(all_data, file, indent=2)
        
        # Convert to proper JSON
        json_objects = []
        for row in all_data[1:]:  # Skip the header row
            obj = {}
            for i, value in enumerate(row):
                if i < len(headers):
                    obj[headers[i]] = value
            json_objects.append(obj)
        
        # Save proper JSON
        proper_filename = filename.replace('.json', '_proper.json')
        with open(proper_filename, 'w') as file:
            json.dump(json_objects, file, indent=2)
        
        print(f"  📊 Total: {len(json_objects)} records saved")
        return True
    else:
        print(f"  ❌ No data fetched for {county_name}")
        return False

def main():
    print("=" * 80)
    print("QUARTERLY WORKFORCE INDICATORS - ALL COUNTIES (2024)")
    print("=" * 80)
    
    success_count = 0
    total_counties = len(counties)
    
    for county_code, state_code, county_name in counties:
        print(f"\n📈 Fetching data for {county_name}...")
        if fetch_county_qwi_data(county_code, state_code, county_name):
            success_count += 1
    
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"✅ Successfully fetched data for {success_count}/{total_counties} counties")
    
    if success_count == total_counties:
        print("🎉 All counties completed successfully!")
    else:
        print("⚠️  Some counties failed. Check the output above for details.")

if __name__ == "__main__":
    main() 