import json
import os

# Target NAICS codes for clean energy and carbon capture
TARGET_NAICS = {
    "221114": "Solar Electric Power Generation",
    "221115": "Wind Electric Power Generation", 
    "335911": "Storage Battery Manufacturing",
    "333611": "Turbine and Turbine Generator Set Units Manufacturing",
    "325180": "Other Basic Inorganic Chemical Manufacturing, including Carbon Capture Technologies"
}

# All VA counties in our dataset
ALL_VA_COUNTIES = [
    "alexandria_city_va",
    "arlington_county_va", 
    "caroline_county_va",
    "clarke_county_va",
    "fairfax_county_va",
    "fauquier_county_va",
    "fredericksburg_city_va",
    "greene_county_va",
    "loudoun_county_va",
    "louisa_county_va",
    "prince_george_county_va",
    "prince_william_county_va",
    "spotsylvania_county_va",
    "stafford_county_va",
    "warren_county_va",
    "westmoreland_county_va",
    "york_county_va"
]

def safe_int(val):
    try:
        return int(val) if val else 0
    except (ValueError, TypeError):
        return 0

def analyze_clean_energy_industries(filename):
    if not os.path.exists(filename):
        return None
    
    with open(filename, 'r') as f:
        data = json.load(f)
    
    # Filter for target NAICS codes
    clean_energy_industries = []
    for record in data:
        naics = record.get("NAICS2017", "")
        if naics in TARGET_NAICS:
            clean_energy_industries.append({
                'naics': naics,
                'label': record.get("NAICS2017_LABEL", ""),
                'emp': safe_int(record.get("EMP", 0)),
                'estab': safe_int(record.get("ESTAB", 0)),
                'payann': safe_int(record.get("PAYANN", 0))
            })
    
    return clean_energy_industries

def main():
    print("=" * 100)
    print("ALL VIRGINIA COUNTIES - CLEAN ENERGY & CARBON CAPTURE INDUSTRIES ANALYSIS")
    print("=" * 100)
    print("Target NAICS Codes:")
    for naics, description in TARGET_NAICS.items():
        print(f"  • {naics}: {description}")
    print("=" * 100)
    
    all_counties_data = []
    
    for county_file in ALL_VA_COUNTIES:
        filename = f"{county_file}_cbp_response_proper.json"
        county_name = county_file.replace('_', ' ').title()
        
        print(f"\n{'='*80}")
        print(f"🌱 {county_name.upper()} - CLEAN ENERGY INDUSTRIES")
        print(f"{'='*80}")
        
        clean_energy_industries = analyze_clean_energy_industries(filename)
        if not clean_energy_industries:
            print("  ❌ No clean energy industries found")
            all_counties_data.append((county_name, []))
            continue
        
        print(f"\n📊 CLEAN ENERGY INDUSTRIES FOUND:")
        print(f"{'NAICS':<8} {'Industry':<60} {'Estab':<8} {'Emp':<8} {'Payroll ($k)':<12}")
        print("-" * 100)
        
        total_estab = 0
        total_emp = 0
        total_payroll = 0
        
        for industry in clean_energy_industries:
            estab = industry['estab']
            emp = industry['emp']
            payroll = industry['payann']
            
            total_estab += estab
            total_emp += emp
            total_payroll += payroll
            
            label = industry['label'][:58] + "..." if len(industry['label']) > 60 else industry['label']
            print(f"{industry['naics']:<8} {label:<60} {estab:<8,} {emp:<8,} {payroll:<12,}")
        
        print("-" * 100)
        print(f"TOTALS: {total_estab:,} establishments, {total_emp:,} employees, ${total_payroll:,}k payroll")
        
        if total_emp > 0:
            avg_payroll = total_payroll / total_emp
            print(f"Average payroll per employee: ${avg_payroll:,.0f}")
        
        all_counties_data.append((county_name, clean_energy_industries))
    
    # Regional summary
    print(f"\n{'='*100}")
    print(f"🌱 ALL VIRGINIA COUNTIES - CLEAN ENERGY INDUSTRIES SUMMARY")
    print(f"{'='*100}")
    
    # Aggregate by NAICS code
    naics_summary = {}
    for naics in TARGET_NAICS:
        naics_summary[naics] = {
            'description': TARGET_NAICS[naics],
            'total_estab': 0,
            'total_emp': 0,
            'total_payroll': 0,
            'counties': []
        }
    
    for county_name, industries in all_counties_data:
        for industry in industries:
            naics = industry['naics']
            if naics in naics_summary:
                naics_summary[naics]['total_estab'] += industry['estab']
                naics_summary[naics]['total_emp'] += industry['emp']
                naics_summary[naics]['total_payroll'] += industry['payann']
                if county_name not in naics_summary[naics]['counties']:
                    naics_summary[naics]['counties'].append(county_name)
    
    print(f"\n📊 CLEAN ENERGY INDUSTRIES BY NAICS CODE:")
    print(f"{'NAICS':<8} {'Industry':<60} {'Estab':<8} {'Emp':<8} {'Counties':<15}")
    print("-" * 100)
    
    total_regional_estab = 0
    total_regional_emp = 0
    total_regional_payroll = 0
    
    for naics, data in naics_summary.items():
        estab = data['total_estab']
        emp = data['total_emp']
        payroll = data['total_payroll']
        county_count = len(data['counties'])
        
        total_regional_estab += estab
        total_regional_emp += emp
        total_regional_payroll += payroll
        
        description = data['description'][:58] + "..." if len(data['description']) > 60 else data['description']
        print(f"{naics:<8} {description:<60} {estab:<8,} {emp:<8,} {county_count:<15}")
    
    print("-" * 100)
    print(f"REGIONAL TOTALS: {total_regional_estab:,} establishments, {total_regional_emp:,} employees, ${total_regional_payroll:,}k payroll")
    
    # Counties with clean energy industries
    print(f"\n🏆 COUNTIES WITH CLEAN ENERGY INDUSTRIES:")
    counties_with_industries = []
    for county_name, industries in all_counties_data:
        if industries:
            total_estab = sum(industry['estab'] for industry in industries)
            total_emp = sum(industry['emp'] for industry in industries)
            counties_with_industries.append((county_name, total_estab, total_emp))
    
    if counties_with_industries:
        counties_with_industries.sort(key=lambda x: x[2], reverse=True)  # Sort by employment
        for county_name, estab, emp in counties_with_industries:
            print(f"  • {county_name}: {estab:,} establishments, {emp:,} employees")
    else:
        print("  ❌ No counties found with clean energy industries")
    
    # Industry presence summary
    print(f"\n�� INDUSTRY PRESENCE SUMMARY:")
    for naics, data in naics_summary.items():
        if data['total_estab'] > 0:
            print(f"  • {TARGET_NAICS[naics]}: {data['total_estab']:,} establishments in {len(data['counties'])} counties")
        else:
            print(f"  • {TARGET_NAICS[naics]}: No establishments found")
    
    # Economic impact
    if total_regional_emp > 0:
        print(f"\n💰 ECONOMIC IMPACT:")
        print(f"  • Total Clean Energy Employment: {total_regional_emp:,}")
        print(f"  • Total Annual Payroll: ${total_regional_payroll:,}k")
        print(f"  • Average Payroll per Employee: ${total_regional_payroll/total_regional_emp:,.0f}")
        print(f"  • Counties with Clean Energy: {len([c for c, i in all_counties_data if i])}")

if __name__ == "__main__":
    main()
