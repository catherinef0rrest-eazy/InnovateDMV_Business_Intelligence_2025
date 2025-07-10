import requests
import json

# Test different time periods to find the most recent data
test_periods = [
    "2024-Q1", "2024-Q2", "2024-Q3", "2024-Q4",
    "2023-Q1", "2023-Q2", "2023-Q3", "2023-Q4", "2023-Q5",
    "2022-Q1", "2022-Q2", "2022-Q3", "2022-Q4",
    "2021-Q1", "2021-Q2", "2021-Q3", "2021-Q4"
]

def test_period(period):
    """Test if a specific time period has data"""
    url = f"https://api.census.gov/data/timeseries/qwi/se?get=Emp&for=county:013&in=state:51&time={period}&key=a19b29f73f2fb20843c8e5835a8d4c85c18467e4"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 1:
                return True, data[1][0] if data[1] else "No employment data"
            else:
                return False, "No data returned"
        else:
            return False, f"HTTP {response.status_code}"
    except Exception as e:
        return False, str(e)

def main():
    print("=" * 80)
    print("CHECKING MOST RECENT QWI DATA AVAILABILITY")
    print("=" * 80)
    
    available_periods = []
    unavailable_periods = []
    
    for period in test_periods:
        print(f"Testing {period}...", end=" ")
        success, result = test_period(period)
        
        if success:
            try:
                emp_value = int(result) if result != "No employment data" else result
                print(f"✅ Available (Employment: {emp_value:,})" if isinstance(emp_value, int) else f"✅ Available (Employment: {emp_value})")
            except:
                print(f"✅ Available (Employment: {result})")
            available_periods.append((period, result))
        else:
            print(f"❌ Not available ({result})")
            unavailable_periods.append(period)
    
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    
    if available_periods:
        print("✅ Available periods:")
        for period, employment in available_periods:
            try:
                emp_value = int(employment) if employment != "No employment data" else employment
                print(f"  - {period}: {emp_value:,} employees" if isinstance(emp_value, int) else f"  - {period}: {emp_value} employees")
            except:
                print(f"  - {period}: {employment} employees")
        
        # Find the most recent
        most_recent = max(available_periods, key=lambda x: x[0])
        try:
            emp_value = int(most_recent[1]) if most_recent[1] != "No employment data" else most_recent[1]
            print(f"\n🎯 Most recent available data: {most_recent[0]} ({emp_value:,} employees)" if isinstance(emp_value, int) else f"\n🎯 Most recent available data: {most_recent[0]} ({emp_value} employees)")
        except:
            print(f"\n🎯 Most recent available data: {most_recent[0]} ({most_recent[1]} employees)")
    else:
        print("❌ No periods available")
    
    if unavailable_periods:
        print(f"\n❌ Unavailable periods: {', '.join(unavailable_periods)}")

if __name__ == "__main__":
    main() 