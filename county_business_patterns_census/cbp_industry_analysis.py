import json
import os
from collections import defaultdict

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

# Define the focused NAICS codes by sector
FOCUSED_NAICS = {
    "AI/ML & Software R&D": [
        "541715",  # Research and Development in Physical, Engineering, and Life Sciences
        "541511",  # Custom Computer Programming Services
        "541512",  # Computer Systems Design Services
        "541519",  # Other Computer Related Services
        "518210",  # Computing Infrastructure Providers, Data Processing, Web Hosting
    ],
    "Cleantech": [
        "221114",  # Solar Electric Power Generation
        "221115",  # Wind Electric Power Generation
        "221116",  # Geothermal Electric Power Generation
        "221117",  # Biomass Electric Power Generation
        "221118",  # Other Electric Power Generation
        "541620",  # Environmental Consulting Services
        "541715",  # R&D in Physical/Engineering/Life Sciences
        "334413",  # Semiconductor and Related Device Manufacturing
    ],
    "Big Data": [
        "518210",  # Data Processing, Hosting, and Related Services
        "541511",  # Custom Computer Programming Services
        "541512",  # Computer Systems Design Services
        "541519",  # Other Computer Related Services
        "541611",  # Administrative Management and General Management Consulting
    ],
    "Cybersecurity": [
        "541512",  # Computer Systems Design Services
        "541519",  # Other Computer Related Services
        "541513",  # Computer Facilities Management Services
        "541690",  # Other Scientific and Technical Consulting Services
        "561621",  # Security Systems Services
        "541715",  # R&D in Physical/Engineering/Life Sciences
    ],
    "IT Services": [
        "541511",  # Custom Computer Programming Services
        "541512",  # Computer Systems Design Services
        "541513",  # Computer Facilities Management Services
        "541519",  # Other Computer Related Services
    ],
    "Professional Services": [
        "541611",  # Administrative Management and General Management Consulting
        "541612",  # Human Resources Consulting Services
        "541618",  # Other Management Consulting Services
        "541310",  # Architectural Services
        "541330",  # Engineering Services
        "541690",  # Other Scientific and Technical Consulting
        "541990",  # All Other Professional, Scientific, and Technical Services
    ]
}

def safe_int(val):
    try:
        return int(val)
    except (ValueError, TypeError):
        return 0

def load_county_data(filename):
    if not os.path.exists(filename):
        return None
    with open(filename, 'r') as f:
        return json.load(f)

def analyze_full_industry_breakdown():
    print("=" * 80)
    print("FULL INDUSTRY BREAKDOWN BY COUNTY")
    print("=" * 80)
    
    for filename, county_name in files:
        data = load_county_data(filename)
        if not data:
            continue
            
        print(f"\n{county_name.upper()}")
        print("-" * 60)
        
        # Sort by employment (descending) and show top 15 industries
        industries = []
        for row in data:
            emp = safe_int(row.get("EMP", 0))
            if emp > 0:
                industries.append({
                    'naics': row.get("NAICS2017", ""),
                    'label': row.get("NAICS2017_LABEL", ""),
                    'emp': emp,
                    'estab': safe_int(row.get("ESTAB", 0)),
                    'payann': safe_int(row.get("PAYANN", 0))
                })
        
        industries.sort(key=lambda x: x['emp'], reverse=True)
        
        print(f"{'NAICS':<8} {'Industry':<50} {'Employment':<12} {'Establishments':<15} {'Payroll ($1K)':<15}")
        print("-" * 100)
        
        for i, industry in enumerate(industries[:15]):
            print(f"{industry['naics']:<8} {industry['label'][:48]:<50} {industry['emp']:<12,} {industry['estab']:<15,} {industry['payann']:<15,}")

def analyze_focused_sectors():
    print("\n" + "=" * 80)
    print("FOCUSED SECTOR ANALYSIS")
    print("=" * 80)
    
    # Collect data for each sector across all counties
    sector_data = defaultdict(lambda: defaultdict(lambda: {'emp': 0, 'estab': 0, 'payann': 0}))
    
    for filename, county_name in files:
        data = load_county_data(filename)
        if not data:
            continue
            
        for row in data:
            naics = row.get("NAICS2017", "")
            emp = safe_int(row.get("EMP", 0))
            estab = safe_int(row.get("ESTAB", 0))
            payann = safe_int(row.get("PAYANN", 0))
            
            # Check which sector this NAICS belongs to
            for sector, naics_codes in FOCUSED_NAICS.items():
                if naics in naics_codes:
                    sector_data[sector][county_name]['emp'] += emp
                    sector_data[sector][county_name]['estab'] += estab
                    sector_data[sector][county_name]['payann'] += payann
    
    # Print analysis for each sector
    for sector, counties in sector_data.items():
        print(f"\n{sector.upper()}")
        print("-" * 60)
        print(f"{'County':<25} {'Employment':<12} {'Establishments':<15} {'Payroll ($1K)':<15}")
        print("-" * 70)
        
        # Sort counties by employment for this sector
        sorted_counties = sorted(counties.items(), key=lambda x: x[1]['emp'], reverse=True)
        
        for county, metrics in sorted_counties:
            if metrics['emp'] > 0:  # Only show counties with employment in this sector
                print(f"{county:<25} {metrics['emp']:<12,} {metrics['estab']:<15,} {metrics['payann']:<15,}")
        
        # Calculate totals for this sector
        total_emp = sum(m['emp'] for m in counties.values())
        total_estab = sum(m['estab'] for m in counties.values())
        total_payann = sum(m['payann'] for m in counties.values())
        print(f"{'TOTAL':<25} {total_emp:<12,} {total_estab:<15,} {total_payann:<15,}")

def main():
    analyze_full_industry_breakdown()
    analyze_focused_sectors()
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    main() 