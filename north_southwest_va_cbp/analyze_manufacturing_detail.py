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

def get_manufacturing_category(naics_code, label):
    """Categorize manufacturing into specific subsectors"""
    if not naics_code:
        return "Other Manufacturing"
    
    # Food Manufacturing
    if naics_code.startswith('311'):
        return "Food Manufacturing"
    
    # Beverage and Tobacco Product Manufacturing
    elif naics_code.startswith('312'):
        return "Beverage & Tobacco Manufacturing"
    
    # Textile Mills
    elif naics_code.startswith('313'):
        return "Textile Mills"
    
    # Textile Product Mills
    elif naics_code.startswith('314'):
        return "Textile Product Mills"
    
    # Apparel Manufacturing
    elif naics_code.startswith('315'):
        return "Apparel Manufacturing"
    
    # Leather and Allied Product Manufacturing
    elif naics_code.startswith('316'):
        return "Leather & Allied Products"
    
    # Wood Product Manufacturing
    elif naics_code.startswith('321'):
        return "Wood Product Manufacturing"
    
    # Paper Manufacturing
    elif naics_code.startswith('322'):
        return "Paper Manufacturing"
    
    # Printing and Related Support Activities
    elif naics_code.startswith('323'):
        return "Printing & Related Activities"
    
    # Petroleum and Coal Products Manufacturing
    elif naics_code.startswith('324'):
        return "Petroleum & Coal Products"
    
    # Chemical Manufacturing
    elif naics_code.startswith('325'):
        return "Chemical Manufacturing"
    
    # Plastics and Rubber Products Manufacturing
    elif naics_code.startswith('326'):
        return "Plastics & Rubber Products"
    
    # Nonmetallic Mineral Product Manufacturing
    elif naics_code.startswith('327'):
        return "Nonmetallic Mineral Products"
    
    # Primary Metal Manufacturing
    elif naics_code.startswith('331'):
        return "Primary Metal Manufacturing"
    
    # Fabricated Metal Product Manufacturing
    elif naics_code.startswith('332'):
        return "Fabricated Metal Products"
    
    # Machinery Manufacturing
    elif naics_code.startswith('333'):
        return "Machinery Manufacturing"
    
    # Computer and Electronic Product Manufacturing
    elif naics_code.startswith('334'):
        return "Computer & Electronic Products"
    
    # Electrical Equipment, Appliance, and Component Manufacturing
    elif naics_code.startswith('335'):
        return "Electrical Equipment & Appliances"
    
    # Transportation Equipment Manufacturing
    elif naics_code.startswith('336'):
        return "Transportation Equipment Manufacturing"
    
    # Furniture and Related Product Manufacturing
    elif naics_code.startswith('337'):
        return "Furniture & Related Products"
    
    # Miscellaneous Manufacturing
    elif naics_code.startswith('339'):
        return "Miscellaneous Manufacturing"
    
    else:
        return "Other Manufacturing"

def analyze_manufacturing_detail(filename, county_name):
    """Analyze manufacturing industries for a specific county"""
    if not os.path.exists(filename):
        print(f"❌ File not found: {filename}")
        return None
    
    with open(filename, 'r') as f:
        data = json.load(f)
    
    # Filter for manufacturing industries (NAICS codes 31-33)
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
    
    # Sort by employment (descending)
    manufacturing.sort(key=lambda x: x['emp'], reverse=True)
    
    return manufacturing

def main():
    print("=" * 100)
    print("SOUTHWEST VIRGINIA MANUFACTURING INDUSTRY DETAILED ANALYSIS")
    print("=" * 100)
    
    all_manufacturing = []
    
    for county_file in SOUTHWEST_VA_COUNTIES:
        filename = f"{county_file}_cbp_response_proper.json"
        county_name = county_file.replace('_', ' ').title()
        
        print(f"\n{'='*80}")
        print(f"🏭 {county_name.upper()} - MANUFACTURING DETAILS")
        print(f"{'='*80}")
        
        manufacturing = analyze_manufacturing_detail(filename, county_name)
        if not manufacturing:
            print("  No manufacturing data found")
            continue
        
        # Show all manufacturing industries
        print(f"\n📋 ALL MANUFACTURING INDUSTRIES:")
        print(f"{'Rank':<4} {'Employment':<12} {'NAICS':<8} {'Industry':<60}")
        print("-" * 90)
        
        total_emp = 0
        total_estab = 0
        total_payann = 0
        
        for i, industry in enumerate(manufacturing, 1):
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
        
        # Manufacturing subsector breakdown
        print(f"\n🏭 MANUFACTURING SUBSECTOR BREAKDOWN:")
        subsector_employment = defaultdict(int)
        subsector_establishments = defaultdict(int)
        subsector_payroll = defaultdict(int)
        
        for industry in manufacturing:
            category = get_manufacturing_category(industry['naics'], industry['label'])
            subsector_employment[category] += industry['emp']
            subsector_establishments[category] += industry['estab']
            subsector_payroll[category] += industry['payann']
        
        # Sort subsectors by employment
        sorted_subsectors = sorted(subsector_employment.items(), key=lambda x: x[1], reverse=True)
        
        print(f"{'Subsector':<35} {'Employment':<12} {'% of Total':<10} {'Estab':<8} {'Avg Pay':<10}")
        print("-" * 80)
        
        for subsector, emp in sorted_subsectors:
            pct = (emp / total_emp * 100) if total_emp > 0 else 0
            estab = subsector_establishments[subsector]
            payroll = subsector_payroll[subsector]
            avg_pay = payroll / emp if emp > 0 else 0
            
            print(f"{subsector:<35} {emp:<12,} {pct:<10.1f}% {estab:<8,} ${avg_pay:<9,.0f}")
        
        # Key insights
        print(f"\n🎯 MANUFACTURING INSIGHTS:")
        if manufacturing:
            largest = manufacturing[0]
            print(f"  • Largest Manufacturing Employer: {largest['label']} ({largest['emp']:,} employees)")
            
            # Highest paying manufacturing industry
            high_pay_manufacturing = []
            for industry in manufacturing:
                if industry['emp'] > 0:
                    avg_pay = industry['payann'] / industry['emp']
                    high_pay_manufacturing.append((avg_pay, industry))
            
            if high_pay_manufacturing:
                high_pay_manufacturing.sort(reverse=True)
                highest_pay = high_pay_manufacturing[0][1]
                avg_pay = high_pay_manufacturing[0][0]
                print(f"  • Highest Paying Manufacturing: {highest_pay['label']} (${avg_pay:,.0f} avg)")
            
            # Most manufacturing establishments
            most_estab = max(manufacturing, key=lambda x: x['estab'])
            print(f"  • Most Manufacturing Establishments: {most_estab['label']} ({most_estab['estab']:,} establishments)")
        
        # Add to overall summary
        all_manufacturing.extend([(county_name, industry) for industry in manufacturing])
    
    # Regional manufacturing summary
    print(f"\n{'='*100}")
    print(f"🏭 REGIONAL MANUFACTURING SUMMARY")
    print(f"{'='*100}")
    
    # Aggregate all manufacturing by subsector
    regional_subsectors = defaultdict(lambda: {'emp': 0, 'estab': 0, 'payroll': 0, 'counties': set()})
    
    for county_name, industry in all_manufacturing:
        subsector = get_manufacturing_category(industry['naics'], industry['label'])
        regional_subsectors[subsector]['emp'] += industry['emp']
        regional_subsectors[subsector]['estab'] += industry['estab']
        regional_subsectors[subsector]['payroll'] += industry['payann']
        regional_subsectors[subsector]['counties'].add(county_name)
    
    total_regional_emp = sum(data['emp'] for data in regional_subsectors.values())
    
    print(f"\n📊 REGIONAL MANUFACTURING SUBSECTORS:")
    print(f"{'Subsector':<35} {'Employment':<12} {'% of Total':<10} {'Estab':<8} {'Counties':<15}")
    print("-" * 85)
    
    sorted_regional = sorted(regional_subsectors.items(), key=lambda x: x[1]['emp'], reverse=True)
    
    for subsector, data in sorted_regional:
        pct = (data['emp'] / total_regional_emp * 100) if total_regional_emp > 0 else 0
        county_count = len(data['counties'])
        print(f"{subsector:<35} {data['emp']:<12,} {pct:<10.1f}% {data['estab']:<8,} {county_count:<15}")
    
    print("-" * 85)
    print(f"Total Regional Manufacturing Employment: {total_regional_emp:,}")
    
    # Top manufacturing employers by county
    print(f"\n🏆 TOP MANUFACTURING EMPLOYERS BY COUNTY:")
    county_manufacturing = defaultdict(list)
    for county_name, industry in all_manufacturing:
        county_manufacturing[county_name].append(industry)
    
    for county_name, industries in county_manufacturing.items():
        if industries:
            largest = max(industries, key=lambda x: x['emp'])
            print(f"  • {county_name}: {largest['label']} ({largest['emp']:,} employees)")

if __name__ == "__main__":
    main() 