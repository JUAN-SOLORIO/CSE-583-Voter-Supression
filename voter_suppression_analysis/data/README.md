### Overview

The data used comes from two sources: the ACLU and US Census Bureau. Note that `/raw` contains data files directly downloaded from source, while `/clean` houses any generated or manually-reformatted versions of raw sheets. Specifically, the US Census Bureau data required major recorrection, as the structure was not conducive to any automated Python pipeline.

#### US Census Bureau: Voting and Registration Data
- two streams, each with individual files for each election year (2000-2018):
  - age: state-by-state breakdown of turnout and registration numbers, among different age groups
  - sex/race: state-by-state breakdown of turnout and registration, by gender *and* among different racial groups
- note that in development, `sex` is often used to represent the inherently combined sex/race datasets 
- [link to source](https://www.census.gov/topics/public-sector/voting/data/tables.2018.html)

#### ACLU: Legislative Data
- two streams (last updated: 2010), manually combined into one set
  - punitive ID laws (IL): one-hot encoding of the suppressing effect of each state's ID laws on voters
  - felony disenfranchisement (FD): numeric degree to which incarcerated candidates are suppressed by law, in each state
- [link to source (IL)](https://www.aclu.org/news/civil-liberties/block-the-vote-voter-suppression-in-2020/)
- [link to source (FD)](https://www.aclu.org/issues/voting-rights/voter-restoration/felony-disenfranchisement-laws-map)
