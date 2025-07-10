import json
import os

# List of (filename, county name) pairs
files = [
    ("arlington_county_response_proper.json", "Arlington County, VA"),
    ("fairfax_county_response_proper.json", "Fairfax County, VA"),
    ("loudoun_county_response_proper.json", "Loudoun County, VA"),
    ("prince_william_county_response_proper.json", "Prince William County, VA"),
    ("montgomery_county_md_response_proper.json", "Montgomery County, MD"),
    ("howard_county_response_proper.json", "Howard County, MD"),
    ("dc_response_proper.json", "Washington, DC"),
]

def safe_int(val):
    try:
        return int(val)
    except (ValueError, TypeError):
        return 0

def summarize_county(filename, county_name):
    if not os.path.exists(filename):
        print(f"❌ File not found: {filename}")
        return None
    with open(filename, 'r') as f:
        data = json.load(f)
    total_estab = sum(safe_int(row.get("ESTAB")) for row in data)
    total_emp = sum(safe_int(row.get("EMP")) for row in data)
    total_payann = sum(safe_int(row.get("PAYANN")) for row in data)
    return {
        "county": county_name,
        "establishments": total_estab,
        "employment": total_emp,
        "annual_payroll": total_payann
    }

def main():
    print("County Business Patterns General Summary:\n")
    print(f"{'County':35} | {'Establishments':>15} | {'Employment':>12} | {'Annual Payroll ($1,000s)':>24}")
    print("-" * 92)
    for filename, county_name in files:
        summary = summarize_county(filename, county_name)
        if summary:
            print(f"{summary['county']:35} | {summary['establishments']:15,} | {summary['employment']:12,} | {summary['annual_payroll']:24,}")
    print("\nAll values are totals across all NAICS codes for each county.")

if __name__ == "__main__":
    main() 