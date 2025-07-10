import json
import os

# List of county files
county_files = [
    ("arlington_county_va_qwi_response_proper.json", "Arlington County, VA"),
    ("fairfax_county_va_qwi_response_proper.json", "Fairfax County, VA"),
    ("loudoun_county_va_qwi_response_proper.json", "Loudoun County, VA"),
    ("prince_william_county_va_qwi_response_proper.json", "Prince William County, VA"),
    ("montgomery_county_md_qwi_response_proper.json", "Montgomery County, MD"),
    ("howard_county_md_qwi_response_proper.json", "Howard County, MD"),
    ("washington_dc_qwi_response_proper.json", "Washington, DC")
]

def load_county_data(filename, county_name):
    """Load QWI data for a county"""
    if not os.path.exists(filename):
        print(f"❌ File not found: {filename}")
        return None
    
    with open(filename, 'r') as file:
        data = json.load(file)
    
    # Convert string values to integers where appropriate
    for record in data:
        for key in ['Emp', 'Sep', 'HirA']:
            if key in record:
                try:
                    record[key] = int(record[key])
                except (ValueError, TypeError):
                    record[key] = 0
    
    return data

def analyze_employment_trends():
    """Analyze employment trends across all counties"""
    print("=" * 80)
    print("QUARTERLY WORKFORCE INDICATORS ANALYSIS")
    print("=" * 80)
    
    all_county_data = {}
    
    # Load all county data
    for filename, county_name in county_files:
        data = load_county_data(filename, county_name)
        if data:
            all_county_data[county_name] = data
            print(f"✅ Loaded {len(data)} records for {county_name}")
        else:
            print(f"❌ Failed to load data for {county_name}")
    
    print(f"\n📊 Loaded data for {len(all_county_data)} counties")
    
    # Analyze employment trends
    print("\n" + "=" * 80)
    print("EMPLOYMENT TRENDS BY COUNTY (2022-Q4 to 2023-Q4)")
    print("=" * 80)
    
    for county_name, data in all_county_data.items():
        print(f"\n{county_name.upper()}")
        print("-" * 60)
        print(f"{'Quarter':<12} {'Employment':<12} {'Separations':<12} {'Hires':<12} {'Net Change':<12}")
        print("-" * 60)
        
        # Sort by time period
        sorted_data = sorted(data, key=lambda x: x['time'])
        
        prev_emp = None
        for record in sorted_data:
            emp = record['Emp']
            sep = record['Sep']
            hir = record['HirA']
            quarter = record['time']
            
            # Calculate net change
            if prev_emp is not None:
                net_change = emp - prev_emp
                net_change_str = f"{net_change:+,}"
            else:
                net_change_str = "N/A"
            
            print(f"{quarter:<12} {emp:<12,} {sep:<12,} {hir:<12,} {net_change_str:<12}")
            prev_emp = emp
    
    # Compare counties by latest employment
    print("\n" + "=" * 80)
    print("COUNTY COMPARISON - LATEST EMPLOYMENT (2023-Q4)")
    print("=" * 80)
    
    latest_employment = []
    for county_name, data in all_county_data.items():
        # Find the latest quarter (should be 2023-Q4)
        latest_record = None
        for record in data:
            if record['time'] == '2023-Q4':
                latest_record = record
                break
        
        if latest_record:
            latest_employment.append((county_name, latest_record['Emp']))
    
    # Sort by employment (descending)
    latest_employment.sort(key=lambda x: x[1], reverse=True)
    
    print(f"{'Rank':<6} {'County':<25} {'Employment':<12} {'% of Total':<12}")
    print("-" * 60)
    
    total_employment = sum(emp for _, emp in latest_employment)
    
    for rank, (county_name, employment) in enumerate(latest_employment, 1):
        percentage = (employment / total_employment) * 100 if total_employment > 0 else 0
        print(f"{rank:<6} {county_name:<25} {employment:<12,} {percentage:<11.1f}%")
    
    print(f"{'TOTAL':<6} {'':<25} {total_employment:<12,} {'100.0%':<12}")

def main():
    analyze_employment_trends()
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    main() 