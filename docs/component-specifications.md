# Component Specification

## Software Components
![](newcomponents.png)

### Raw Data
- Functions: 
    - accumulate all streams of election and demographic data, for all intended years
- Input: 
    - all unchanged .CSV files from MIT and the Census Bureau
- Output: 
    - all .CSV files, renamed for clarity and organization
### Data Processor
- Functions: 
    - load raw data
    - handle malformed values
    - merge legislative and demographic data by year and state
    - aggregate age and demographic data, perform joins with legislative data 
- Input: 
    - all labeled .CSV files
- Output: 
    - processed .CSV file
### Dashboard Manager
- Functions: 
    - generate Altair map views based on filters and joins
    - transmit rendered Altair visualization to output HTML file
- Input: 
    - modeled data as pandas.DataFrame or numpy.ndarray
- Output: 
    - Altair visualization (Python objects, functions, and code) 
### Output
- Input: 
    - user commands and interactions
- Output: 
    - live, updated version of same HTML file 

## Interactions
1. User changes 'year' value using visualization controls on browser.
    - User changes settings of interactive map
    - Dynamic JS within the output HTML file filters data to the desired year
    - HTML file renders new Altair view of the visualization for the changed settings
    
2. User selects a specific state using visualization controls on browser.
    - User changes settings of interactive map to Map Manager
    - Dynamic JS within output HTML file filters data to desired state/cluster and year
    - HTML file renders new Altair view of visualization, for the changed settings

## Preliminary Plan 
1. Create and organize desired package structure in repository
2. Incorporate Git CI and test functionality
3. Write scripts to appropriately process and combine data
4. Write scripts to model and categorize data entries
5. Develop template for Altair map visualization (with interactive features)
6. Write scripts to simplify installation and launch of visualization
7. Revisit model performance and add write-ups, time permitting
