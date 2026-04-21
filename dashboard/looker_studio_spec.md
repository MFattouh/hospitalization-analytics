# Looker Studio Dashboard Specification

## Data Source
- Connect to BigQuery project
- Use dataset: `hospital_marts`
- Tables available:
  - `fct_bed_occupancy`
  - `fct_patient_satisfaction` 
  - `dim_services`
  - `mrt_kpis`

## Dashboard Layout

### Theme
- Title: "Hospital Bed Operations Dashboard"
- Background: White
- Font: Google Sans / Arial
- Primary Color: #1a73e8 (Google Blue)
- Secondary Colors: #34a853 (Green), #ea4335 (Red), #fbbc04 (Yellow)

### Layout Grid
```
┌──────────────────────────────────────────────────────────────────────────────┐
│ Hospital Bed Operations Dashboard                                          [F] │
│ Service: [All ▼]  Month: [All ▼]  Event Type: [All ▼]  Apply Filters [Button]│
├─────────────────────┬─────────────────────┬─────────────────────┬────────────┤
│  AVG OCCUPANCY      │  TOTAL ADMISSIONS   │  TOTAL REFUSALS     │ AVG SATISF │
│  72.4%              │  12,847             │  3,214              │  78.2      │
├─────────────────────┼─────────────────────┼─────────────────────┼────────────┤
│                                                                              │
│  WEEKLY OCCUPANCY RATE BY SERVICE                           DEMAND vs CAPACITY│
│  [LINE CHART]                                                             [  │
│  X: Week (1-52)                                                           BAR]│
│  Y: Occupancy Rate (0-1)                                                  │
│  Lines: One per service                                                   │
│                                                                              │
│                                                                              │
│  SATISFACTION vs OCCUPANCY              REFUSAL RATE & STAFF MORALE       │
│  [SCATTER PLOT]                                 [DUAL-AXIS CHART]          │
│  X: Occupancy Rate                                                          │
│  Y: Satisfaction (0-100)                                                    │
│  Trend line: Shows correlation                                              │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Components Details

#### 1. KPI Scorecards (Top Row)
Create 4 scorecard components:

**Score 1: Average Occupancy Rate**
- Metric: AVG(occupancy_rate) from `fct_bed_occupancy`
- Format: Percentage (1 decimal place)
- Comparison: None or previous period

**Score 2: Total Admissions**
- Metric: SUM(patients_admitted) from `fct_bed_occupancy`
- Format: Integer
- Comparison: None or previous period

**Score 3: Total Refusals**
- Metric: SUM(patients_refused) from `fct_bed_occupancy`  
- Format: Integer
- Comparison: None or previous period

**Score 4: Average Satisfaction**
- Metric: AVG(patient_satisfaction) from `fct_bed_occupancy`
- Format: Number (1 decimal place)
- Comparison: None or previous period

#### 2. Weekly Occupancy Rate by Service (Left Top Chart)
- Chart Type: Line chart
- Dimension: Week (from `fct_bed_occupancy`)
- Metric: AVG(occupancy_rate) 
- Breakdown Dimension: Service
- Sort: Week ascending
- Show points: Yes
- Line weight: 2px
- Tooltip: Week, Service, Occupancy Rate

#### 3. Bed Demand vs Capacity by Service (Right Top Chart)
- Chart Type: Bar chart (grouped/clustered)
- Dimension: Service
- Metrics: 
  - SUM(patients_request) as "Demand"
  - SUM(available_beds) as "Capacity"
- Sort: Demand descending
- Colors: Demand = #ea4335 (Red), Capacity = #1a73e8 (Blue)
- Tooltip: Service, Demand, Capacity

#### 4. Satisfaction vs Occupancy Correlation (Left Bottom Chart)
- Chart Type: Scatter plot
- X Axis: AVG(occupancy_rate) from `fct_bed_occupancy`
- Y Axis: AVG(patient_satisfaction) from `fct_bed_occupancy`
- Breakdown Dimension: Service (optional, for colored points)
- Trend Line: Show linear trend
- Tooltip: Service, Occupancy Rate, Satisfaction
- X Axis Label: "Occupancy Rate"
- Y Axis Label: "Patient Satisfaction (0-100)"

#### 5. Refusal Rate & Staff Morale Impact (Right Bottom Chart)
- Chart Type: Combo chart (bar + line)
- Dimension: Week (from `fct_bed_occupancy`)
- Bar Metric: AVG(refusal_rate) from `fct_bed_occupancy`
- Line Metric: AVG(staff_morale) from `fct_bed_occupancy`
- Bar Color: #ea4335 (Red)
- Line Color: #34a853 (Green) 
- Line Weight: 3px
- Dual Axis: Left axis = Refusal Rate (0-1), Right axis = Staff Morale (0-100)
- Tooltip: Week, Refusal Rate, Staff Morale

### Filters (Top Right)
Create 3 filter controls:

**Filter 1: Service**
- Type: Dropdown list
- Dimension: Service (from `fct_bed_occupancy`)
- Default: All
- Allow multiple selection: No

**Filter 2: Month** 
- Type: Dropdown list
- Dimension: Month (from `fct_bed_occupancy`)
- Default: All
- Allow multiple selection: No

**Filter 3: Event Type**
- Type: Dropdown list  
- Dimension: Event (from `fct_bed_occupancy`)
- Default: All
- Allow multiple selection: No

**Apply Button**: Optional - set filters to apply on button click rather than automatically

### Styling Notes
- All charts should have:
  - Light grid lines
  - Axis labels with units
  - Legend when applicable
  - Tooltip enabled
  - Animation: None (for professional dashboard)
- Background: White with subtle drop shadow on cards
- Font sizes: 
  - Title: 20px bold
  - Section headers: 16px bold
  - Labels: 12px
  - Values: 14-18px depending on importance
- Spacing: Consistent 16-24px between components

### Data Refresh
- Set data source to refresh every 24 hours (since source data is static annual data)
- Or manually refresh when new data is loaded into BigQuery

### Sharing
- Set sharing to "Anyone with the link can view" for distribution to stakeholders
- Schedule email delivery if needed for executive reports

---

## Implementation Steps

1. In Looker Studio, create a new report
2. Add data source: Connect to BigQuery → Select project → Select `hospital_marts` dataset
3. Add each component as specified above
4. Apply filters consistently across all charts
5. Style according to the theme guidelines
6. Set appropriate default date ranges (show all data)
7. Save and share

The dashboard will show the relationship between hospital bed capacity utilization and patient satisfaction, helping administrators understand how occupancy levels impact patient experience.