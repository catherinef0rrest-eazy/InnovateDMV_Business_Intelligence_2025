import json
import os
from collections import defaultdict

# Southwest VA counties (excluding North VA counties)
SOUTHWEST_VA_COUNTIES = [
    "caroline_county_va",
    "clarke_county_va", 
    "fauquier_county_va",
    "greene_county_va",
    "louisa_county_va",
    "prince_george_county_va",
    "spotsylvania_county_va",
    "stafford_county_va",
    "warren_county_va",
    "westmoreland_county_va",
    "york_county_va",
    "fredericksburg_city_va"
]

def safe_int(val):
    """Safely convert value to integer"""
    try:
        return int(val) if val else 0
    except (ValueError, TypeError):
        return 0

def analyze_county_industries(filename, county_name):
    """Analyze industries for a specific county"""
    if not os.path.exists(filename):
        print(f"❌ File not found: {filename}")
        return None
    
    with open(filename, 'r') as f:
        data = json.load(f)
    
    # Filter out records with no employment and sort by employment
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
    
    # Sort by employment (descending)
    industries.sort(key=lambda x: x['emp'], reverse=True)
    
    return industries

def get_industry_category(naics_code, label):
    """Categorize industries into broader sectors"""
    if not naics_code:
        return "Other"
    
    # Manufacturing
    if naics_code.startswith(('31', '32', '33')):
        return "Manufacturing"
    
    # Retail Trade
    elif naics_code.startswith('44') or naics_code.startswith('45'):
        return "Retail Trade"
    
    # Health Care
    elif naics_code.startswith('62'):
        return "Health Care"
    
    # Professional Services
    elif naics_code.startswith('54'):
        return "Professional Services"
    
    # Construction
    elif naics_code.startswith('23'):
        return "Construction"
    
    # Accommodation & Food Services
    elif naics_code.startswith('72'):
        return "Accommodation & Food Services"
    
    # Transportation & Warehousing
    elif naics_code.startswith('48') or naics_code.startswith('49'):
        return "Transportation & Warehousing"
    
    # Finance & Insurance
    elif naics_code.startswith('52'):
        return "Finance & Insurance"
    
    # Real Estate
    elif naics_code.startswith('53'):
        return "Real Estate"
    
    # Educational Services
    elif naics_code.startswith('61'):
        return "Educational Services"
    
    # Public Administration
    elif naics_code.startswith('92'):
        return "Public Administration"
    
    # Agriculture
    elif naics_code.startswith('11'):
        return "Agriculture"
    
    # Mining
    elif naics_code.startswith('21'):
        return "Mining"
    
    # Utilities
    elif naics_code.startswith('22'):
        return "Utilities"
    
    # Wholesale Trade
    elif naics_code.startswith('42'):
        return "Wholesale Trade"
    
    # Information
    elif naics_code.startswith('51'):
        return "Information"
    
    # Administrative Services
    elif naics_code.startswith('56'):
        return "Administrative Services"
    
    # Arts & Entertainment
    elif naics_code.startswith('71'):
        return "Arts & Entertainment"
    
    # Other Services
    elif naics_code.startswith('81'):
        return "Other Services"
    
    else:
        return "Other"

def main():
    print("=" * 100)
    print("SOUTHWEST VIRGINIA COUNTY INDUSTRY ANALYSIS")
    print("=" * 100)
    
    for county_file in SOUTHWEST_VA_COUNTIES:
        filename = f"{county_file}_cbp_response_proper.json"
        county_name = county_file.replace('_', ' ').title()
        
        print(f"\n{'='*80}")
        print(f"📊 {county_name.upper()}")
        print(f"{'='*80}")
        
        industries = analyze_county_industries(filename, county_name)
        if not industries:
            continue
        
        # Show top 10 industries by employment
        print(f"\n🏆 TOP 10 INDUSTRIES BY EMPLOYMENT:")
        print(f"{'Rank':<4} {'Employment':<12} {'Industry':<60} {'NAICS':<8}")
        print("-" * 90)
        
        total_emp = 0
        for i, industry in enumerate(industries[:10], 1):
            emp = industry['emp']
            total_emp += emp
            label = industry['label'][:58] + "..." if len(industry['label']) > 60 else industry['label']
            print(f"{i:<4} {emp:<12,} {label:<60} {industry['naics']:<8}")
        
        print("-" * 90)
        print(f"Total Employment: {total_emp:,}")
        
        # Industry sector analysis
        print(f"\n📈 INDUSTRY SECTOR BREAKDOWN:")
        sector_employment = defaultdict(int)
        sector_establishments = defaultdict(int)
        
        for industry in industries:
            category = get_industry_category(industry['naics'], industry['label'])
            sector_employment[category] += industry['emp']
            sector_establishments[category] += industry['estab']
        
        # Sort sectors by employment
        sorted_sectors = sorted(sector_employment.items(), key=lambda x: x[1], reverse=True)
        
        print(f"{'Sector':<25} {'Employment':<12} {'% of Total':<10} {'Estab':<8}")
        print("-" * 60)
        
        for sector, emp in sorted_sectors[:8]:  # Top 8 sectors
            pct = (emp / total_emp * 100) if total_emp > 0 else 0
            estab = sector_establishments[sector]
            print(f"{sector:<25} {emp:<12,} {pct:<10.1f}% {estab:<8,}")
        
        # Economic indicators
        total_estab = sum(industry['estab'] for industry in industries)
        total_payann = sum(industry['payann'] for industry in industries)
        avg_payroll_per_emp = total_payann / total_emp if total_emp > 0 else 0
        
        print(f"\n💰 ECONOMIC INDICATORS:")
        print(f"  • Total Establishments: {total_estab:,}")
        print(f"  • Total Employment: {total_emp:,}")
        print(f"  • Total Annual Payroll: ${total_payann:,}k")
        print(f"  • Average Payroll per Employee: ${avg_payroll_per_emp:,.0f}")
        
        # Special focus on key industries
        print(f"\n🎯 KEY INDUSTRY INSIGHTS:")
        
        # Find largest employer
        if industries:
            largest = industries[0]
            print(f"  • Largest Employer: {largest['label']} ({largest['emp']:,} employees)")
        
        # Find highest paying industry (by average payroll per employee)
        high_pay_industries = []
        for industry in industries:
            if industry['emp'] > 0:
                avg_pay = industry['payann'] / industry['emp']
                high_pay_industries.append((avg_pay, industry))
        
        if high_pay_industries:
            high_pay_industries.sort(reverse=True)
            highest_pay = high_pay_industries[0][1]
            avg_pay = high_pay_industries[0][0]
            print(f"  • Highest Paying Industry: {highest_pay['label']} (${avg_pay:,.0f} avg)")
        
        # Find industry with most establishments
        most_estab = max(industries, key=lambda x: x['estab'])
        print(f"  • Most Establishments: {most_estab['label']} ({most_estab['estab']:,} establishments)")

if __name__ == "__main__":
    main() 