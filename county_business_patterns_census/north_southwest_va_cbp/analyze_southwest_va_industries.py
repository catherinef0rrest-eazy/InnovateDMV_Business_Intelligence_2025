import json
import os
from collections import defaultdict

# Southwest VA counties
SOUTHWEST_VA_COUNTIES = [
    "caroline_county_va", "clarke_county_va", "fauquier_county_va", "greene_county_va",
    "louisa_county_va", "prince_george_county_va", "spotsylvania_county_va", "stafford_county_va",
    "warren_county_va", "westmoreland_county_va", "york_county_va", "fredericksburg_city_va"
]

def safe_int(val):
    try:
        return int(val) if val else 0
    except (ValueError, TypeError):
        return 0

def analyze_county_industries(filename):
    if not os.path.exists(filename):
        print(f"❌ File not found: {filename}")
        return None
    
    with open(filename, 'r') as f:
        data = json.load(f)
    
    industries = []
    for record in data:
        emp = safe_int(record.get("EMP", 0))
        if emp > 0:
            industries.append({
                'naics': record.get("NAICS2017", ""),
                'label': record.get("NAICS2017_LABEL", ""),
                'emp': emp,
                'estab': safe_int(record.get("ESTAB", 0)),
                'payann': safe_int(record.get("PAYANN", 0))
            })
    
    industries.sort(key=lambda x: x['emp'], reverse=True)
    return industries

def main():
    print("=" * 80)
    print("SOUTHWEST VIRGINIA COUNTY INDUSTRY ANALYSIS")
    print("=" * 80)
    
    for county_file in SOUTHWEST_VA_COUNTIES:
        filename = f"{county_file}_cbp_response_proper.json"
        county_name = county_file.replace('_', ' ').title()
        
        print(f"\n{'='*60}")
        print(f"📊 {county_name.upper()}")
        print(f"{'='*60}")
        
        industries = analyze_county_industries(filename)
        if not industries:
            continue
        
        print(f"\n🏆 TOP 5 INDUSTRIES BY EMPLOYMENT:")
        print(f"{'Rank':<4} {'Employment':<12} {'Industry':<50}")
        print("-" * 70)
        
        total_emp = 0
        for i, industry in enumerate(industries[:5], 1):
            emp = industry['emp']
            total_emp += emp
            label = industry['label'][:48] + "..." if len(industry['label']) > 50 else industry['label']
            print(f"{i:<4} {emp:<12,} {label:<50}")
        
        print("-" * 70)
        print(f"Total Employment: {total_emp:,}")
        
        # Economic summary
        total_estab = sum(industry['estab'] for industry in industries)
        total_payann = sum(industry['payann'] for industry in industries)
        
        print(f"\n💰 ECONOMIC SUMMARY:")
        print(f"  • Total Establishments: {total_estab:,}")
        print(f"  • Total Employment: {total_emp:,}")
        print(f"  • Total Annual Payroll: ${total_payann:,}k")
        
        if industries:
            largest = industries[0]
            print(f"  • Largest Employer: {largest['label']} ({largest['emp']:,} employees)")

if __name__ == "__main__":
    main()
