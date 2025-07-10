import json
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

# List of county files for 2023 and 2024
county_files = [
    ("../proper_json/arlington_county_va_qwi_response_proper.json", "../proper_json/arlington_county_va_qwi_2024_response_proper.json", "Arlington County, VA"),
    ("../proper_json/fairfax_county_va_qwi_response_proper.json", "../proper_json/fairfax_county_va_qwi_2024_response_proper.json", "Fairfax County, VA"),
    ("../proper_json/loudoun_county_va_qwi_response_proper.json", "../proper_json/loudoun_county_va_qwi_2024_response_proper.json", "Loudoun County, VA"),
    ("../proper_json/prince_william_county_va_qwi_response_proper.json", "../proper_json/prince_william_county_va_qwi_2024_response_proper.json", "Prince William County, VA"),
    ("../proper_json/montgomery_county_md_qwi_response_proper.json", "../proper_json/montgomery_county_md_qwi_2024_response_proper.json", "Montgomery County, MD"),
    ("../proper_json/howard_county_md_qwi_response_proper.json", "../proper_json/howard_county_md_qwi_2024_response_proper.json", "Howard County, MD"),
    ("../proper_json/washington_dc_qwi_response_proper.json", "../proper_json/washington_dc_qwi_2024_response_proper.json", "Washington, DC")
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

def create_employment_chart(all_county_data):
    """Create line chart for employment trends by county"""
    plt.figure(figsize=(14, 8))
    
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2']
    
    for i, (county_name, data) in enumerate(all_county_data.items()):
        quarters_list = [record['time'] for record in data]
        employment_list = [record['Emp'] for record in data]
        
        plt.plot(quarters_list, employment_list, marker='o', linewidth=2, 
                label=county_name, color=colors[i % len(colors)])
    
    plt.title('Employment Trends by County (2023-Q1 to 2024-Q3)', fontsize=16, fontweight='bold')
    plt.xlabel('Quarter', fontsize=12)
    plt.ylabel('Employment', fontsize=12)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def create_growth_rate_chart(all_county_data):
    """Create bar chart for growth rates by county"""
    growth_rates = {}
    
    for county_name, data in all_county_data.items():
        if len(data) >= 2:
            first_emp = data[0]['Emp']
            last_emp = data[-1]['Emp']
            growth_rate = ((last_emp - first_emp) / first_emp) * 100
            growth_rates[county_name] = growth_rate
    
    counties = list(growth_rates.keys())
    rates = list(growth_rates.values())
    
    plt.figure(figsize=(12, 6))
    bars = plt.bar(counties, rates, color='skyblue', edgecolor='navy', alpha=0.7)
    
    # Add value labels on bars
    for bar, rate in zip(bars, rates):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                f'{rate:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    plt.title('Employment Growth Rate by County (2023-Q1 to 2024-Q3)', fontsize=16, fontweight='bold')
    plt.xlabel('County', fontsize=12)
    plt.ylabel('Growth Rate (%)', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.show()

def create_quarterly_change_chart(all_county_data):
    """Create heatmap showing quarterly changes by county"""
    # Create a matrix of quarterly changes
    counties = list(all_county_data.keys())
    quarterly_changes = []
    
    for county_name, data in all_county_data.items():
        county_changes = []
        for i in range(1, len(data)):
            change = data[i]['Emp'] - data[i-1]['Emp']
            county_changes.append(change)
        quarterly_changes.append(county_changes)
    
    # Create the heatmap
    plt.figure(figsize=(12, 8))
    im = plt.imshow(quarterly_changes, cmap='RdYlGn', aspect='auto')
    
    # Add labels
    plt.xticks(range(len(quarters)-1), [f'{q1}→{q2}' for q1, q2 in zip(quarters[:-1], quarters[1:])], rotation=45)
    plt.yticks(range(len(counties)), counties)
    
    # Add colorbar
    cbar = plt.colorbar(im)
    cbar.set_label('Employment Change', rotation=270, labelpad=20)
    
    # Add text annotations
    for i in range(len(counties)):
        for j in range(len(quarters)-1):
            if i < len(quarterly_changes) and j < len(quarterly_changes[i]):
                text = plt.text(j, i, f'{quarterly_changes[i][j]:+,}', 
                               ha="center", va="center", color="black", fontsize=8)
    
    plt.title('Quarterly Employment Changes by County', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.show()

def analyze_growth_rates(all_county_data):
    """Analyze and print growth rates for all counties"""
    print("=" * 80)
    print("GROWTH RATE ANALYSIS (2023-Q1 to 2024-Q3)")
    print("=" * 80)
    
    growth_data = []
    
    for county_name, data in all_county_data.items():
        if len(data) >= 2:
            first_emp = data[0]['Emp']
            last_emp = data[-1]['Emp']
            total_change = last_emp - first_emp
            growth_rate = ((last_emp - first_emp) / first_emp) * 100
            
            # Calculate quarterly average growth
            quarterly_changes = []
            for i in range(1, len(data)):
                change = data[i]['Emp'] - data[i-1]['Emp']
                quarterly_changes.append(change)
            
            avg_quarterly_change = sum(quarterly_changes) / len(quarterly_changes) if quarterly_changes else 0
            
            growth_data.append({
                'County': county_name,
                'Start Employment': first_emp,
                'End Employment': last_emp,
                'Total Change': total_change,
                'Growth Rate (%)': growth_rate,
                'Avg Quarterly Change': avg_quarterly_change
            })
    
    # Sort by growth rate (descending)
    growth_data.sort(key=lambda x: x['Growth Rate (%)'], reverse=True)
    
    print(f"{'Rank':<6} {'County':<25} {'Start':<10} {'End':<10} {'Change':<10} {'Growth %':<10} {'Avg Q Change':<12}")
    print("-" * 90)
    
    for rank, data in enumerate(growth_data, 1):
        total_change_str = f"{data['Total Change']:+,}"
        avg_change_str = f"{data['Avg Quarterly Change']:+,}"
        print(f"{rank:<6} {data['County']:<25} {data['Start Employment']:<10,} {data['End Employment']:<10,} "
              f"{total_change_str:<10} {data['Growth Rate (%)']:<9.1f}% {avg_change_str:<12}")
    
    # Summary statistics
    print("\n" + "=" * 80)
    print("SUMMARY STATISTICS")
    print("=" * 80)
    
    growth_rates = [data['Growth Rate (%)'] for data in growth_data]
    avg_growth = sum(growth_rates) / len(growth_rates)
    max_growth = max(growth_rates)
    min_growth = min(growth_rates)
    
    print(f"Average Growth Rate: {avg_growth:.1f}%")
    print(f"Highest Growth Rate: {max_growth:.1f}%")
    print(f"Lowest Growth Rate: {min_growth:.1f}%")
    print(f"Growth Rate Range: {max_growth - min_growth:.1f}%")

def main():
    print("=" * 80)
    print("QWI VISUALIZATION AND GROWTH ANALYSIS")
    print("=" * 80)
    
    # Load all county data
    all_county_data = {}
    for file_2023, file_2024, county_name in county_files:
        data = load_county_data(file_2023, file_2024, county_name)
        if data:
            all_county_data[county_name] = data
            print(f"✅ Loaded {len(data)} records for {county_name}")
        else:
            print(f"❌ Failed to load data for {county_name}")
    
    print(f"\n📊 Loaded data for {len(all_county_data)} counties")
    
    # Create visualizations
    print("\n📈 Creating employment trends chart...")
    create_employment_chart(all_county_data)
    
    print("\n📊 Creating growth rates chart...")
    create_growth_rate_chart(all_county_data)
    
    print("\n🔥 Creating quarterly changes heatmap...")
    create_quarterly_change_chart(all_county_data)
    
    # Analyze growth rates
    print("\n📋 Analyzing growth rates...")
    analyze_growth_rates(all_county_data)
    
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    main() 