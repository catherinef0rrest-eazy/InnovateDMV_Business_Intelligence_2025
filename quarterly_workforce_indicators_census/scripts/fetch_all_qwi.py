import subprocess
import sys
import os

# List of all QWI scripts to run
scripts = [
    'fetch_qwi_arlington.py',
    'fetch_qwi_fairfax.py', 
    'fetch_qwi_loudoun.py',
    'fetch_qwi_prince_william.py',
    'fetch_qwi_montgomery_md.py',
    'fetch_qwi_howard.py',
    'fetch_qwi_dc.py'
]

def run_script(script_name):
    """Run a single script and return success status"""
    try:
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, text=True, check=True)
        print(f"✅ {script_name}: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {script_name}: {e.stderr.strip()}")
        return False

def main():
    print("🚀 Starting to fetch QWI data for all counties...")
    print("=" * 60)
    
    success_count = 0
    total_scripts = len(scripts)
    
    for script in scripts:
        if run_script(script):
            success_count += 1
        print("-" * 40)
    
    print("=" * 60)
    print(f"📊 Summary: {success_count}/{total_scripts} scripts completed successfully")
    
    if success_count == total_scripts:
        print("🎉 All QWI data fetched successfully!")
    else:
        print("⚠️  Some scripts failed. Check the output above for details.")

if __name__ == "__main__":
    main() 