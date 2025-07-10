import json
import os
from collections import defaultdict

# List of county files for 2023 and 2024
county_files = [
    ("arlington_county_va_qwi_response_proper.json", "arlington_county_va_qwi_2024_response_proper.json", "Arlington County, VA"),
    ("fairfax_county_va_qwi_response_proper.json", "fairfax_county_va_qwi_2024_response_proper.json", "Fairfax County, VA"),
    ("loudoun_county_va_qwi_response_proper.json", "loudoun_county_va_qwi_2024_response_proper.json", "Loudoun County, VA"),
    ("prince_william_county_va_qwi_response_proper.json", "prince_william_county_va_qwi_2024_response_proper.json", "Prince William County, VA"),
    ("montgomery_county_md_qwi_response_proper.json", "montgomery_county_md_qwi_2024_response_proper.json", "Montgomery County, MD"),
    ("howard_county_md_qwi_response_proper.json", "howard_county_md_qwi_2024_response_proper.json", "Howard County, MD"),
    ("washington_dc_qwi_response_proper.json", "washington_dc_qwi_2024_response_proper.json", "Washington, DC")
]

quarters = [
    "2023-Q1", "2023-Q2", "2023-Q3", "2023-Q4",
    "2024-Q1", "2024-Q2", "2024-Q3"
]

def load_county_data(file_2023, file_2024, county_name):
    """Load and merge QWI data for a county from 2023 and 2024 files"""
    data = []
    for filename in [file_2023, file_2024]:
        if not os.path.exists(filename):
            print(f"❌ File not found: {filename}")
            continue
        with open(filename, 'r') as file:
            records = json.load(file)
            for record in records:
                # Only keep records for the target quarters
                if record.get('time') in quarters:
                    for key in ['Emp', 'Sep', 'HirA']:
                        if key in record:
                            try:
                                record[key] = int(record[key])
                            except (ValueError, TypeError):
                                record[key] = 0
                    data.append(record)
    # Remove duplicates (in case of overlap)
    seen = set()
    unique_data = []
    for rec in data:
        key = (rec['time'], rec.get('county'), rec.get('state'))
        if key not in seen:
            unique_data.append(rec)
            seen.add(key)
    # Sort by quarter
    unique_data.sort(key=lambda x: x['time'])
    return unique_data

def analyze_employment_trends():
    print("=" * 100)
    print("QWI WORKFORCE ANALYSIS: 2023-Q1 THROUGH 2024-Q3")
    print("=" * 100)
    all_county_data = {}
    for file_2023, file_2024, county_name in county_files:
        data = load_county_data(file_2023, file_2024, county_name)
        if data:
            all_county_data[county_name] = data
            print(f"✅ Loaded {len(data)} records for {county_name}")
        else:
            print(f"❌ Failed to load data for {county_name}")
    print(f"\n📊 Loaded data for {len(all_county_data)} counties")
    # Employment trends by county
    print("\n" + "=" * 100)
    print("EMPLOYMENT TRENDS BY COUNTY (2023-Q1 to 2024-Q3)")
    print("=" * 100)
    for county_name, data in all_county_data.items():
        print(f"\n{county_name.upper()}")
        print("-" * 60)
        print(f"{'Quarter':<12} {'Employment':<12} {'Separations':<12} {'Hires':<12} {'Net Change':<12}")
        print("-" * 60)
        prev_emp = None
        for record in data:
            emp = record['Emp']
            sep = record['Sep']
            hir = record['HirA']
            quarter = record['time']
            if prev_emp is not None:
                net_change = emp - prev_emp
                net_change_str = f"{net_change:+,}"
            else:
                net_change_str = "N/A"
            print(f"{quarter:<12} {emp:<12,} {sep:<12,} {hir:<12,} {net_change_str:<12}")
            prev_emp = emp
    # County comparison by quarter
    print("\n" + "=" * 100)
    print("COUNTY COMPARISON BY QUARTER (2023-Q1 to 2024-Q3)")
    print("=" * 100)
    for quarter in quarters:
        print(f"\n{quarter}")
        print("-" * 60)
        print(f"{'Rank':<6} {'County':<25} {'Employment':<12} {'% of Total':<12}")
        print("-" * 60)
        employment_list = []
        for county_name, data in all_county_data.items():
            emp = next((rec['Emp'] for rec in data if rec['time'] == quarter), None)
            if emp is not None:
                employment_list.append((county_name, emp))
        employment_list.sort(key=lambda x: x[1], reverse=True)
        total_emp = sum(emp for _, emp in employment_list)
        for rank, (county_name, emp) in enumerate(employment_list, 1):
            pct = (emp / total_emp) * 100 if total_emp > 0 else 0
            print(f"{rank:<6} {county_name:<25} {emp:<12,} {pct:<11.1f}%")
        print(f"{'TOTAL':<6} {'':<25} {total_emp:<12,} {'100.0%':<12}")

def main():
    analyze_employment_trends()
    print("\n" + "=" * 100)
    print("ANALYSIS COMPLETE")
    print("=" * 100)

if __name__ == "__main__":
    main() 