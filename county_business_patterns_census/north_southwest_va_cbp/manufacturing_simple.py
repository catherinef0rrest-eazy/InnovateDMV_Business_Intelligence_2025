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

def analyze_manufacturing(filename):
    if not os.path.exists(filename):
        return None
    
    with open(filename, 'r') as f:
        data = json.load(f)
    
    manufacturing = []
    for record in data:
        naics = record.get("NAICS2017", "")
        emp = safe_int(record.get("EMP", 0))
        
        if naics.startswith(('31', '32', '33')) and emp > 0:
            manufacturing.append({
                'naics': naics,
                'label': record.get("NAICS2017_LABEL", ""),
                'emp': emp,
                'estab': safe_int(record.get("ESTAB", 0)),
                'payann': safe_int(record.get("PAYANN", 0))
            })
    
    manufacturing.sort(key=lambda x: x['emp'], reverse=True)
    return manufacturing

def main():
    print("=" * 100)
    print("SOUTHWEST VIRGINIA MANUFACTURING DETAILED ANALYSIS")
    print("=" * 100)
    
    all_manufacturing = []
    
    for county_file in SOUTHWEST_VA_COUNTIES:
        filename = f"{county_file}_cbp_response_proper.json"
        county_name = county_file.replace('_', ' ').title()
        
        print(f"\n{'='*80}")
        print(f"🏭 {county_name.upper()} - MANUFACTURING DETAILS")
        print(f"{'='*80}")
        
        manufacturing = analyze_manufacturing(filename)
        if not manufacturing:
            print("  No manufacturing data found")
            continue
        
        print(f"\n📋 MANUFACTURING INDUSTRIES:")
        print(f"{'Rank':<4} {'Employment':<12} {'NAICS':<8} {'Industry':<60}")
        print("-" * 90)
        
        total_emp = 0
        total_estab = 0
        total_payann = 0
        
        for i, industry in enumerate(manufacturing[:10], 1):  # Show top 10
            emp = industry['emp']
            total_emp += emp
            total_estab += industry['estab']
            total_payann += industry['payann']
            
            label = industry['label'][:58] + "..." if len(industry['label']) > 60 else industry['label']
            print(f"{i:<4} {emp:<12,} {industry['naics']:<8} {label:<60}")
        
        print("-" * 90)
        print(f"Total Manufacturing Employment: {total_emp:,}")
        print(f"Total Manufacturing Establishments: {total_estab:,}")
        print(f"Total Manufacturing Payroll: ${total_payann:,}k")
        
        if total_emp > 0:
            avg_payroll = total_payann / total_emp
            print(f"Average Manufacturing Payroll per Employee: ${avg_payroll:,.0f}")
        
        # Key insights
        print(f"\n🎯 KEY MANUFACTURING INSIGHTS:")
        if manufacturing:
            largest = manufacturing[0]
            print(f"  • Largest Manufacturing Employer: {largest['label']} ({largest['emp']:,} employees)")
            
            # Find highest paying manufacturing industry
            high_pay_industries = []
            for industry in manufacturing:
                if industry['emp'] > 0:
                    avg_pay = industry['payann'] / industry['emp']
                    high_pay_industries.append((avg_pay, industry))
            
            if high_pay_industries:
                high_pay_industries.sort(reverse=True)
                highest_pay = high_pay_industries[0][1]
                avg_pay = high_pay_industries[0][0]
                print(f"  • Highest Paying Manufacturing: {highest_pay['label']} (${avg_pay:,.0f} avg)")
        
        # Add to overall summary
        all_manufacturing.extend([(county_name, industry) for industry in manufacturing])
    
    # Regional summary
    print(f"\n{'='*100}")
    print(f"🏭 REGIONAL MANUFACTURING SUMMARY")
    print(f"{'='*100}")
    
    # Top manufacturing employers by county
    print(f"\n🏆 TOP MANUFACTURING EMPLOYERS BY COUNTY:")
    county_manufacturing = defaultdict(list)
    for county_name, industry in all_manufacturing:
        county_manufacturing[county_name].append(industry)
    
    for county_name, industries in county_manufacturing.items():
        if industries:
            largest = max(industries, key=lambda x: x['emp'])
            print(f"  • {county_name}: {largest['label']} ({largest['emp']:,} employees)")
    
    # Manufacturing by NAICS subsector
    print(f"\n📊 MANUFACTURING BY SUBSECTOR:")
    subsector_employment = defaultdict(int)
    
    for county_name, industry in all_manufacturing:
        naics = industry['naics']
        if naics.startswith('336'):
            subsector = "Transportation Equipment"
        elif naics.startswith('321'):
            subsector = "Wood Products"
        elif naics.startswith('332'):
            subsector = "Fabricated Metal Products"
        elif naics.startswith('333'):
            subsector = "Machinery"
        elif naics.startswith('334'):
            subsector = "Computer & Electronics"
        elif naics.startswith('335'):
            subsector = "Electrical Equipment"
        elif naics.startswith('311'):
            subsector = "Food Manufacturing"
        elif naics.startswith('312'):
            subsector = "Beverage & Tobacco"
        elif naics.startswith('327'):
            subsector = "Nonmetallic Mineral Products"
        elif naics.startswith('337'):
            subsector = "Furniture"
        elif naics.startswith('323'):
            subsector = "Printing"
        else:
            subsector = "Other Manufacturing"
        
        subsector_employment[subsector] += industry['emp']
    
    sorted_subsectors = sorted(subsector_employment.items(), key=lambda x: x[1], reverse=True)
    
    print(f"{'Subsector':<25} {'Employment':<12} {'% of Total':<10}")
    print("-" * 50)
    
    total_regional_emp = sum(subsector_employment.values())
    for subsector, emp in sorted_subsectors:
        pct = (emp / total_regional_emp * 100) if total_regional_emp > 0 else 0
        print(f"{subsector:<25} {emp:<12,} {pct:<10.1f}%")
    
    print("-" * 50)
    print(f"Total Regional Manufacturing: {total_regional_emp:,} employees")

if __name__ == "__main__":
    main()
