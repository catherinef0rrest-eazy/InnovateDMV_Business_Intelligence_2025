# Market Analysis Files - Comprehensive Analysis

This repository contains comprehensive market analysis of the Washington DC metropolitan area, focusing on County Business Patterns (CBP) and Quarterly Workforce Indicators (QWI) data from the US Census Bureau.

##  Analysis Overview

### Target Counties Analyzed
- **Virginia:** Arlington County, Fairfax County, Loudoun County, Prince William County
- **Maryland:** Montgomery County, Howard County  
- **District of Columbia:** Washington, DC

##  County Business Patterns (CBP) Analysis

### Data Sources
- **Census API:** County Business Patterns (CBP) data
- **Time Period:** Most recent available data
- **Coverage:** All establishments, employment, and payroll data by county

### Key Findings

#### General Summary
- **Total Establishments:** Analyzed across all counties
- **Employment Levels:** Comprehensive employment data by county
- **Payroll Information:** Total payroll figures by county

#### Industry Breakdown Analysis
**Focus Sectors:**
- **AI/ML Technologies** (NAICS codes: 511210, 541715, 541720)
- **Cleantech** (NAICS codes: 221110, 221120, 237130)
- **Big Data** (NAICS codes: 518210, 541715, 541720)
- **Cybersecurity** (NAICS codes: 541715, 541720, 561612)
- **IT Services** (NAICS codes: 541511, 541512, 541519)
- **Professional Services** (NAICS codes: 541110, 541120, 541330)

**Analysis Results:**
- Employment levels by sector
- Payroll data by industry
- County comparisons for each sector
- Growth trends in technology sectors

##  Quarterly Workforce Indicators (QWI) Analysis

### Data Sources
- **Census API:** Quarterly Workforce Indicators (QWI)
- **Time Period:** 2023-Q1 to 2024-Q3 (7 quarters)
- **Metrics:** Employment (Emp), Separations (Sep), Hires (HirA)

### Key Findings

#### Employment Growth Analysis (2023-Q1 to 2024-Q3)

**Growth Rankings:**
1. **Loudoun County, VA** - 7.2% growth (+13,503 jobs)
2. **Prince William County, VA** - 6.3% growth (+8,563 jobs)  
3. **Fairfax County, VA** - 5.2% growth (+34,734 jobs)
4. **Arlington County, VA** - 3.4% growth (+5,294 jobs)
5. **Washington, DC** - 2.7% growth (+15,196 jobs)
6. **Montgomery County, MD** - 2.4% growth (+10,914 jobs)
7. **Howard County, MD** - 2.2% growth (+6,494 jobs)

**Summary Statistics:**
- **Average Growth Rate:** 4.2%
- **Highest Growth:** 7.2% (Loudoun County)
- **Lowest Growth:** 2.2% (Howard County)
- **Growth Range:** 5.0 percentage points

#### Key Insights
- **Virginia counties** are leading employment growth
- **Loudoun County** shows the strongest percentage growth
- **Fairfax County** had the largest absolute job growth (+34,734 jobs)
- All counties showed positive employment growth over the 7-quarter period

##  File Structure

```
Market Analysis Files/
├── dc_cbp_response_proper.json          # DC CBP data (proper format)
├── md_mc_response.json                  # Montgomery County CBP data
├── convert_to_proper_json.py           # JSON conversion script
├── quarterly_workforce_indicators_census/
│   ├── proper_json/                     # QWI data files (proper format)
│   │   ├── arlington_county_va_qwi_response_proper.json
│   │   ├── arlington_county_va_qwi_2024_response_proper.json
│   │   ├── fairfax_county_va_qwi_response_proper.json
│   │   ├── fairfax_county_va_qwi_2024_response_proper.json
│   │   ├── loudoun_county_va_qwi_response_proper.json
│   │   ├── loudoun_county_va_qwi_2024_response_proper.json
│   │   ├── prince_william_county_va_qwi_response_proper.json
│   │   ├── prince_william_county_va_qwi_2024_response_proper.json
│   │   ├── montgomery_county_md_qwi_response_proper.json
│   │   ├── montgomery_county_md_qwi_2024_response_proper.json
│   │   ├── howard_county_md_qwi_response_proper.json
│   │   ├── howard_county_md_qwi_2024_response_proper.json
│   │   ├── washington_dc_qwi_response_proper.json
│   │   └── washington_dc_qwi_2024_response_proper.json
│   ├── scripts/                        # Analysis and fetch scripts
│   │   ├── qwi_analysis_2023_2024.py  # QWI analysis script
│   │   ├── qwi_visualization_analysis.py # Visualization script
│   │   └── [various fetch scripts]
│   └── analysis_outputs/               # Analysis results
└── qwi_visualization_analysis_fixed.py # Main visualization script
```

## ️ Scripts and Tools

### Data Processing Scripts
- **convert_to_proper_json.py:** Converts raw JSON responses to proper key-value format
- **Various fetch scripts:** Individual county data retrieval from Census APIs

### Analysis Scripts
- **qwi_analysis_2023_2024.py:** Comprehensive QWI data analysis
- **qwi_visualization_analysis_fixed.py:** Interactive visualization and growth analysis

### Visualization Features
The main visualization script creates three interactive charts:
1. **Employment Trends Chart** - Line chart showing employment over time by county
2. **Growth Rates Chart** - Bar chart comparing growth rates across counties  
3. **Quarterly Changes Heatmap** - Color-coded matrix showing quarterly employment changes

##  Data Sources and APIs

### Census Bureau APIs Used
1. **County Business Patterns (CBP) API**
   - Endpoint: `https://api.census.gov/data/timeseries/cbp`
   - Variables: Employment, establishments, payroll
   - Geographic level: County

2. **Quarterly Workforce Indicators (QWI) API**
   - Endpoint: `https://api.census.gov/data/timeseries/qwi`
   - Variables: Emp (employment), Sep (separations), HirA (hires)
   - Geographic level: County
   - Time periods: 2023-Q1 to 2024-Q3

##  Key Business Insights

### Regional Growth Patterns
- **Northern Virginia** is experiencing the strongest employment growth
- **Loudoun County** leads with 7.2% growth, likely driven by technology sector expansion
- **Fairfax County** shows the largest absolute job growth, indicating strong economic activity

### Sector Analysis
- Technology sectors (AI/ML, Big Data, Cybersecurity) show strong presence
- Professional services remain a significant employment driver
- Cleantech and IT services sectors are growing steadily

### Market Opportunities
- **Loudoun County** presents the highest growth potential
- **Fairfax County** offers the largest market size with strong growth
- Technology and professional services sectors show consistent demand

##  Technical Requirements

### Python Dependencies
```bash
pip install requests matplotlib pandas numpy
```

### Running Analysis
```bash
# Run QWI visualization and analysis
python qwi_visualization_analysis_fixed.py

# Run CBP analysis (if scripts are available)
python cbp_analysis.py
```

##  Data Quality Notes

- All data sourced from official US Census Bureau APIs
- Data converted to proper JSON format for analysis
- Missing data points handled gracefully in analysis scripts
- Growth calculations based on consistent time periods

##  Future Analysis Opportunities

### Potential Extensions
1. **Longitudinal Analysis:** Extend QWI analysis to include more historical data
2. **Sector-Specific QWI:** Analyze workforce indicators by industry sector
3. **Comparative Analysis:** Compare with other metropolitan areas
4. **Economic Impact Analysis:** Correlate employment data with economic indicators
5. **Forecasting Models:** Develop predictive models based on historical trends

### Additional Data Sources
- **American Community Survey (ACS)** for demographic insights
- **Business Dynamics Statistics (BDS)** for business formation/closure data
- **Economic Census** for detailed industry analysis
- **Local Economic Development Data** for policy insights

---

*This analysis provides a comprehensive view of the Washington DC metropolitan area's business and employment landscape, supporting strategic decision-making for business development and investment opportunities.* 