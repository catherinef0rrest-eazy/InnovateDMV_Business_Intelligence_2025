import json
import os
from collections import defaultdict

# Target NAICS codes for clean energy and related industries
TARGET_NAICS_CODES = {
    "221114": "Solar Electric Power Generation",
    "221115": "Wind Electric Power Generation", 
    "335911": "Storage Battery Manufacturing",
    "333611": "Turbine and Turbine Generator Set Units Manufacturing",
    "325180": "Other Basic Inorganic Chemical Manufacturing, including Carbon Capture Technologies"
}

# Define county regions
NORTH_VA_COUNTIES = {
    "arlington_county_va",
    "fairfax_county_va", 
    "loudoun_county_va",
    "prince_william_county_va",
    "alexandria_city_va",
    "city_of_fairfax_va",
    "city_of_falls_church_va",
    "city_of_manassas_va",
    "city_of_manassas_park_va",
    "fredericksburg_city_va"
}

SOUTHWEST_VA_COUNTIES = {
    "bland_county_va",
    "buchanan_county_va",
    "carroll_county_va",
    "dickenson_county_va",
    "grayson_county_va",
    "lee_county_va",
    "russell_county_va",
    "scott_county_va",
    "smyth_county_va",
    "tazewell_county_va",
    "washington_county_va",
    "wise_county_va",
    "wythe_county_va",
    "galax_city_va",
    "bristol_city_va",
    "norton_city_va"
}

def load_county_data(county_name):
    """Load CBP data for a specific county"""
    filename = f"{county_name}_cbp_response_proper.json"
    
    # Try both directories
    possible_paths = [
        filename,
        f"north_southwest_va_cbp/{filename}"
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            try:
                with open(path, 'r') as file:
                    return json.load(file)
            except Exception as e:
                print(f"Error loading {path}: {e}")
                return None
    
    print(f"Could not find data file for {county_name}")
    return None

def analyze_county_clean_energy(county_name, data):
    """Analyze clean energy industries for a specific county"""
    if not data:
        return None
    
    # Track businesses by NAICS code
    businesses_by_naics = defaultdict(list)
    total_businesses = 0
    
    for record in data:
        naics_code = record.get("NAICS2017", "")
        naics_label = record.get("NAICS2017_LABEL", "")
        estab_count = int(record.get("ESTAB", 0))
        emp_count = int(record.get("EMP", 0))
        payroll = int(record.get("PAYANN", 0))
        
        # Check if this NAICS code matches our target codes
        if naics_code in TARGET_NAICS_CODES:
            businesses_by_naics[naics_code].append({
                "naics_label": naics_label,
                "establishments": estab_count,
                "employment": emp_count,
                "payroll": payroll
            })
            total_businesses += estab_count
    
    return {
        "county": county_name,
        "total_businesses": total_businesses,
        "businesses_by_naics": dict(businesses_by_naics),
        "has_any_clean_energy": total_businesses > 0
    }

def main():
    print("=" * 80)
    print("VIRGINIA CLEAN ENERGY INDUSTRY ANALYSIS")
    print("=" * 80)
    print("Target NAICS Codes:")
    for code, description in TARGET_NAICS_CODES.items():
        print(f"  {code}: {description}")
    print("=" * 80)
    
    # Get all county names from the data files
    all_counties = set()
    
    # Check main directory
    for file in os.listdir("."):
        if file.endswith("_cbp_response_proper.json"):
            county_name = file.replace("_cbp_response_proper.json", "")
            all_counties.add(county_name)
    
    # Check north_southwest_va_cbp directory
    if os.path.exists("north_southwest_va_cbp"):
        for file in os.listdir("north_southwest_va_cbp"):
            if file.endswith("_cbp_response_proper.json"):
                county_name = file.replace("_cbp_response_proper.json", "")
                all_counties.add(county_name)
    
    # Filter to only VA counties
    va_counties = [c for c in all_counties if "va" in c.lower()]
    va_counties.sort()
    
    print(f"Found {len(va_counties)} Virginia counties with data")
    print()
    
    # Analyze each county
    county_results = {}
    north_va_total = 0
    southwest_va_total = 0
    
    for county in va_counties:
        data = load_county_data(county)
        result = analyze_county_clean_energy(county, data)
        
        if result:
            county_results[county] = result
            
            # Add to regional totals
            if county in NORTH_VA_COUNTIES:
                north_va_total += result["total_businesses"]
            elif county in SOUTHWEST_VA_COUNTIES:
                southwest_va_total += result["total_businesses"]
    
    # Print results by county
    print("BUSINESSES WITH CLEAN ENERGY NAICS CODES BY COUNTY:")
    print("-" * 80)
    print(f"{'County':<30} | {'Businesses':<12} | {'NAICS Codes Found':<20}")
    print("-" * 80)
    
    for county in va_counties:
        if county in county_results:
            result = county_results[county]
            naics_codes_found = ", ".join(result["businesses_by_naics"].keys())
            print(f"{county.replace('_', ' ').title():<30} | {result['total_businesses']:<12} | {naics_codes_found:<20}")
        else:
            print(f"{county.replace('_', ' ').title():<30} | {'No data':<12} | {'N/A':<20}")
    
    # Print detailed breakdown
    print("\n" + "=" * 80)
    print("DETAILED BREAKDOWN BY COUNTY AND NAICS CODE:")
    print("=" * 80)
    
    for county in va_counties:
        if county in county_results and county_results[county]["total_businesses"] > 0:
            result = county_results[county]
            print(f"\n{county.replace('_', ' ').title()}:")
            print(f"  Total businesses: {result['total_businesses']}")
            
            for naics_code, businesses in result["businesses_by_naics"].items():
                for business in businesses:
                    print(f"    {naics_code} ({TARGET_NAICS_CODES[naics_code]}):")
                    print(f"      - Establishments: {business['establishments']}")
                    print(f"      - Employment: {business['employment']:,}")
                    print(f"      - Annual Payroll: ${business['payroll']:,}k")
    
    # Print regional totals
    print("\n" + "=" * 80)
    print("REGIONAL TOTALS:")
    print("=" * 80)
    print(f"North Virginia: {north_va_total} businesses")
    print(f"Southwest Virginia: {southwest_va_total} businesses")
    print(f"Total Virginia: {north_va_total + southwest_va_total} businesses")
    
    # Print summary by NAICS code across all counties
    print("\n" + "=" * 80)
    print("SUMMARY BY NAICS CODE ACROSS ALL COUNTIES:")
    print("=" * 80)
    
    naics_totals = defaultdict(lambda: {"establishments": 0, "employment": 0, "payroll": 0})
    
    for county in va_counties:
        if county in county_results:
            result = county_results[county]
            for naics_code, businesses in result["businesses_by_naics"].items():
                for business in businesses:
                    naics_totals[naics_code]["establishments"] += business["establishments"]
                    naics_totals[naics_code]["employment"] += business["employment"]
                    naics_totals[naics_code]["payroll"] += business["payroll"]
    
    for naics_code in TARGET_NAICS_CODES:
        totals = naics_totals[naics_code]
        print(f"\n{naics_code}: {TARGET_NAICS_CODES[naics_code]}")
        print(f"  Total establishments: {totals['establishments']}")
        print(f"  Total employment: {totals['employment']:,}")
        print(f"  Total annual payroll: ${totals['payroll']:,}k")

if __name__ == "__main__":
    main() 