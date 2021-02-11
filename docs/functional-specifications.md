# Functional Specification

## Background

The results of American elections seem to matter now more than ever. Significant time, money, and effort is spent in the analysis and prediction of voter behavior, as unpredictable turnout can mean the downfall of political candidates and parties. But little attention is given to the closely-related issue of voter suppression: the combination of factors that hinder every citizen’s ability to vote freely. It can be difficult to wholly define voter suppression. Sound arguments attribute many factors to inhibited turnout. Some are easily measured, such as constituency wealth, polling location sparsity, or population demographics. Others are harder to quantify, like wait times, insufficient staffing, and malicious ID laws. Such simple and complex factors are included (or at least acknowledged) in this project. There are issues outside of our scope, too: for example, the absent voting rights of populations that live in US “territories.”

The ultimate aim of this project is to provide users with an interactive visualization, which overlays our analysis onto a navigable US map. Interactivity stems from the users' ability to navigate the shifting clusters over time and view accompanying statistics. Importantly, our project also aims to help users explore state-wise differences in our results, and recognize key contributors to voter suppression.

## User Profiles

Anticipated users include anyone interested in learning about the factors inhibiting voter turnout, or the variation in voting experiences across the U.S (and over time). Users may also be state-level legislators in charge of the redistricting process. These policy-makers need a good understanding of the citizen populations in each constituency to carry out this role. To that end, the data represented in our visualization may also be useful. 

In any case, users must be able to clone a GitHub repository and follow a minimal set of installation instructions (*e.g.,* running Python scripts) in a Linux environment. Users should also be able to navigate map applications resembling those found on popular websites (e.g., Google Maps) via hover, point-and-click, pan, and scrolling operations. Given appropriate direction, they must be able to clone a Git repository and run Python scripts to access and launch our visualization. 

## Data Sources

- [Official Returns for the 2018 Midterm Elections](https://github.com/MEDSL/2018-elections-official)
    - Provider: MIT Election Lab
    - Structure: Redundant .CSV files representing the same data, for each regional granularity (state, county, district, and precinct). Attributes of interest include:
        - office
        - party 
        - stage 
        - votes 
- [Voting and Registration in the Election of November 2018](https://www.census.gov/data/tables/time-series/demo/voting-and-registration/p20-583.html)
    - Provider: U.S. Census Bureau
    - Structure: Distinct .CSV files, each quantifying the rate of voter turnout among some central target demographic. Interesting demographics (each with their own file) include:
        - race
        - age
        - sex
        - income/worker status
    - Notes:
        - each file has two primary variable types: percent registered to vote, and percent voted
        - additional files recording voting method, and reasons for not voting, were also used

## Use Cases

1. A user wants to compare the change in state groupings on the map, from one year to the next. 
    - User: Adjusts slider for 'year' variable
        - Map: Updates to reflect color-coded grouping of states for that year, from backend analysis
    - User: Moves slider for 'year' variable forward by one unit
        - Map: Updates to reflect subsequent grouping of states 
        
        
2. A user wants to compare the difference in attributes among state groupings on the map, within one year.
    - User: Hovers over and selects one state in a given year
        - Map: highlights this state and all states belonging to its cluster
        - Map: displays relative attributes for this state (compared to national aggregates) via pop-up
        - Map: displays relative attributes for the cluster via pop-up
        - Map: provides additional anecdotes (voting methods, ID laws, court cases) if available via pop-up
    - User: Without changing the year, selects a state from another grouping
        - Map: highlights this state and all states belonging to its cluster
        - Map: displays relative attributes for this state (compared to national aggregates) via pop-up
        - Map: displays relative attributes for the cluster via pop-up
        - Map: provides additional anecdotes (voting methods, ID laws, court cases) if available via pop-up 
