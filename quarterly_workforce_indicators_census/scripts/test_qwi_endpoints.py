import requests
import json

# Test different QWI endpoints to see what's available
test_urls = [
    # Test state-level data
    "https://api.census.gov/data/timeseries/qwi/se?get=Emp&for=state:51&key=a19b29f73f2fb20843c8e5835a8d4c85c18467e4",
    
    # Test MSA-level data
    "https://api.census.gov/data/timeseries/qwi/se?get=Emp&for=metropolitan%20statistical%20area:47900&key=a19b29f73f2fb20843c8e5835a8d4c85c18467e4",
    
    # Test with different variables
    "https://api.census.gov/data/timeseries/qwi/se?get=Emp,Sep&for=state:51&key=a19b29f73f2fb20843c8e5835a8d4c85c18467e4",
    
    # Test with time period
    "https://api.census.gov/data/timeseries/qwi/se?get=Emp&for=state:51&time=2023-Q1&key=a19b29f73f2fb20843c8e5835a8d4c85c18467e4"
]

def test_endpoint(url, description):
    """Test a QWI endpoint and return results"""
    try:
        print(f"\nTesting: {description}")
        print(f"URL: {url}")
        
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Found {len(data)} records")
            if data:
                print(f"Headers: {data[0]}")
                if len(data) > 1:
                    print(f"Sample record: {data[1]}")
            return True, data
        else:
            print(f"❌ Failed with status code: {response.status_code}")
            print(f"Response: {response.text[:200]}")
            return False, None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False, None

def main():
    print("=" * 80)
    print("TESTING QWI API ENDPOINTS")
    print("=" * 80)
    
    successful_tests = []
    
    for i, url in enumerate(test_urls):
        descriptions = [
            "State-level employment data (Virginia)",
            "MSA-level employment data (Washington-Arlington-Alexandria)",
            "State-level employment and separations data (Virginia)",
            "State-level employment data with time period (Virginia, 2023-Q1)"
        ]
        
        success, data = test_endpoint(url, descriptions[i])
        if success:
            successful_tests.append((descriptions[i], data))
    
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    
    if successful_tests:
        print(f"✅ {len(successful_tests)} endpoints worked:")
        for desc, data in successful_tests:
            print(f"  - {desc}: {len(data)} records")
    else:
        print("❌ No endpoints worked. The QWI API might be:")
        print("  - Temporarily unavailable")
        print("  - Requiring different parameters")
        print("  - Not supporting the geographic levels we're requesting")

if __name__ == "__main__":
    main() 