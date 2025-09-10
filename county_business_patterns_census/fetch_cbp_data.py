import requests
import json
import os
from datetime import datetime

# FIPS codes provided by the user
FIPS_CODES = [
    # Northern Virginia
    "51013",  # Arlington County, VA
    "51059",  # Fairfax County, VA
    "51107",  # Loudoun County, VA
    "51153",  # Prince William County, VA
    "51510",  # Alexandria City, VA
    "51600",  # City of Fairfax, VA
    "51610",  # City of Falls Church, VA
    "51683",  # City of Manassas, VA
    "51685",  # City of Manassas Park, VA
    
    # Southwest Virginia
    "51021",  # Bland County, VA
    "51027",  # Buchanan County, VA
    "51035",  # Carroll County, VA
    "51051",  # Dickenson County, VA
    "51077",  # Grayson County, VA
    "51105",  # Lee County, VA
    "51167",  # Russell County, VA
    "51169",  # Scott County, VA
    "51173",  # Smyth County, VA
    "51185",  # Tazewell County, VA
    "51191",  # Washington County, VA
    "51195",  # Wise County, VA
    "51197",  # Wythe County, VA
    "51640",  # Galax City, VA
    "51520",  # Bristol City, VA
    "51720",  # Norton City, VA
    
    # Other Virginia counties (existing)
    "51061",  # Fauquier County, VA
    "51179",  # Stafford County, VA
    "51157",  # Prince George County, VA
    "51023",  # Caroline County, VA
    "51043",  # Clarke County, VA
    "51079",  # Greene County, VA
    "51111",  # Louisa County, VA
    "51177",  # Spotsylvania County, VA
    "51187",  # Warren County, VA
    "51193",  # Westmoreland County, VA
    "51199",  # York County, VA
    "51197",  # Fredericksburg city, VA
]

# Remove duplicates and sort
FIPS_CODES = sorted(list(set(FIPS_CODES)))

# Census API key (using the same key from QWI scripts)
API_KEY = "a19b29f73f2fb20843c8e5835a8d4c85c18467e4"

# CBP API base URL
BASE_URL = "https://api.census.gov/data/2021/cbp"

# Variables to fetch
VARIABLES = [
    "ESTAB",      # Number of establishments
    "EMP",        # Employment
    "PAYANN",     # Annual payroll ($1,000s)
    "NAICS2017",  # NAICS code
    "NAICS2017_LABEL"  # NAICS description
]

def get_county_name(fips_code):
    """Get county name from FIPS code"""
    # Extract state and county codes
    state_code = fips_code[:2]
    county_code = fips_code[2:]
    
    # County name mapping (complete)
    county_names = {
        # Northern Virginia
        "51013": "Arlington County, VA",
        "51059": "Fairfax County, VA", 
        "51107": "Loudoun County, VA",
        "51153": "Prince William County, VA",
        "51510": "Alexandria City, VA",
        "51600": "City of Fairfax, VA",
        "51610": "City of Falls Church, VA",
        "51683": "City of Manassas, VA",
        "51685": "City of Manassas Park, VA",
        
        # Southwest Virginia
        "51021": "Bland County, VA",
        "51027": "Buchanan County, VA",
        "51035": "Carroll County, VA",
        "51051": "Dickenson County, VA",
        "51077": "Grayson County, VA",
        "51105": "Lee County, VA",
        "51167": "Russell County, VA",
        "51169": "Scott County, VA",
        "51173": "Smyth County, VA",
        "51185": "Tazewell County, VA",
        "51191": "Washington County, VA",
        "51195": "Wise County, VA",
        "51197": "Wythe County, VA",
        "51640": "Galax City, VA",
        "51520": "Bristol City, VA",
        "51720": "Norton City, VA",
        
        # Other Virginia counties
        "51061": "Fauquier County, VA",
        "51179": "Stafford County, VA",
        "51157": "Prince George County, VA",
        "51023": "Caroline County, VA",
        "51043": "Clarke County, VA",
        "51079": "Greene County, VA",
        "51111": "Louisa County, VA",
        "51177": "Spotsylvania County, VA",
        "51187": "Warren County, VA",
        "51193": "Westmoreland County, VA",
        "51199": "York County, VA",
        "51197": "Fredericksburg city, VA",
    }
    
    return county_names.get(fips_code, f"County {county_code}, State {state_code}")

def fetch_cbp_data(fips_code):
    """Fetch CBP data for a specific FIPS code"""
    county_name = get_county_name(fips_code)
    print(f"\n📊 Fetching CBP data for {county_name} (FIPS: {fips_code})...")
    
    # Construct the API URL
    variables_str = ",".join(VARIABLES)
    url = f"{BASE_URL}?get={variables_str}&for=county:{fips_code[2:]}&in=state:{fips_code[:2]}&key={API_KEY}"
    
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            
            if data and len(data) > 1:
                # Extract headers and data
                headers = data[0]
                records = data[1:]
                
                # Convert to list of dictionaries
                json_objects = []
                for record in records:
                    obj = {}
                    for i, value in enumerate(record):
                        if i < len(headers):
                            obj[headers[i]] = value
                    json_objects.append(obj)
                
                # Save raw data
                raw_filename = f"{county_name.lower().replace(', ', '_').replace(' ', '_')}_cbp_response.json"
                with open(raw_filename, 'w') as file:
                    json.dump(data, file, indent=2)
                
                # Save processed data
                proper_filename = f"{county_name.lower().replace(', ', '_').replace(' ', '_')}_cbp_response_proper.json"
                with open(proper_filename, 'w') as file:
                    json.dump(json_objects, file, indent=2)
                
                # Calculate summary statistics
                total_estab = sum(int(record.get("ESTAB", 0)) for record in json_objects)
                total_emp = sum(int(record.get("EMP", 0)) for record in json_objects)
                total_payann = sum(int(record.get("PAYANN", 0)) for record in json_objects)
                
                print(f"  ✅ Success: {len(json_objects)} records")
                print(f"  📈 Total establishments: {total_estab:,}")
                print(f"  👥 Total employment: {total_emp:,}")
                print(f"  💰 Total annual payroll: ${total_payann:,}k")
                print(f"  💾 Saved: {raw_filename} and {proper_filename}")
                
                return {
                    "success": True,
                    "county": county_name,
                    "fips": fips_code,
                    "records": len(json_objects),
                    "establishments": total_estab,
                    "employment": total_emp,
                    "payroll": total_payann
                }
            else:
                print(f"  ⚠️  No data returned")
                return {"success": False, "county": county_name, "fips": fips_code, "error": "No data"}
        else:
            print(f"  ❌ API request failed: {response.status_code}")
            print(f"  📄 Response: {response.text[:200]}...")
            return {"success": False, "county": county_name, "fips": fips_code, "error": f"HTTP {response.status_code}"}
            
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return {"success": False, "county": county_name, "fips": fips_code, "error": str(e)}

def main():
    print("=" * 80)
    print("CENSUS COUNTY BUSINESS PATTERNS (CBP) DATA FETCHER")
    print("=" * 80)
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🎯 Target FIPS codes: {len(FIPS_CODES)} counties")
    print(f"🔑 API Key: {API_KEY[:10]}...")
    print(f"🌐 Base URL: {BASE_URL}")
    print("=" * 80)
    
    results = []
    success_count = 0
    
    for fips_code in FIPS_CODES:
        result = fetch_cbp_data(fips_code)
        results.append(result)
        if result["success"]:
            success_count += 1
    
    # Print summary
    print("\n" + "=" * 80)
    print("SUMMARY REPORT")
    print("=" * 80)
    print(f"✅ Successful: {success_count}/{len(FIPS_CODES)} counties")
    print(f"❌ Failed: {len(FIPS_CODES) - success_count} counties")
    
    if success_count > 0:
        print(f"\n📊 ECONOMIC SUMMARY:")
        print(f"{'County':<30} | {'Estab':>8} | {'Emp':>10} | {'Payroll ($k)':>12}")
        print("-" * 70)
        
        total_estab = 0
        total_emp = 0
        total_payroll = 0
        
        for result in results:
            if result["success"]:
                print(f"{result['county']:<30} | {result['establishments']:8,} | {result['employment']:10,} | {result['payroll']:12,}")
                total_estab += result['establishments']
                total_emp += result['employment']
                total_payroll += result['payroll']
        
        print("-" * 70)
        print(f"{'TOTAL':<30} | {total_estab:8,} | {total_emp:10,} | {total_payroll:12,}")
    
    # Print failed counties
    failed_counties = [r for r in results if not r["success"]]
    if failed_counties:
        print(f"\n❌ FAILED COUNTIES:")
        for result in failed_counties:
            print(f"  • {result['county']} (FIPS: {result['fips']}): {result.get('error', 'Unknown error')}")
    
    print(f"\n🎉 Data fetching completed!")
    print(f"📁 Check the current directory for JSON files with '_cbp_response' suffix")

if __name__ == "__main__":
    main() 