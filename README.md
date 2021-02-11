# Voter Suppression Analysis

[![Build Status](https://travis-ci.com/Anmol-Srivastava/voter-suppression-analysis.svg?branch=master)](https://travis-ci.com/Anmol-Srivastava/voter-suppression-analysis)
[![GitHub contributors](https://img.shields.io/github/contributors/Anmol-Srivastava/voter-suppression-analysis)](#contributors)
[![GitHub license](https://img.shields.io/github/license/Anmol-Srivastava/voter-suppression-analysis)](./LICENSE)
[![Coverage Status](https://coveralls.io/repos/github/Anmol-Srivastava/voter-suppression-analysis/badge.svg?branch=packaging)](https://coveralls.io/github/Anmol-Srivastava/voter-suppression-analysis?branch=packaging)

## Overview

*This project is part of an assignment for [DATA 515: Software Engineering for Data Scientists](http://uwseds.github.io).*

The aim of this project is to visualize the state of voter suppression across the US. Chiefly, this project draws on data from the US Census Bureau and the American Civil Liberties Union (ACLU), to create an interactive geographical depiction of voter turnout among various demographics. The central dashboard describes, over several years, each state's turnout by race, sex, and age. This information is accompanied by a visual demarcation of the punitive quality of each state's voting laws. For data-related or other practical reasons, many considerations are left out (*e.g.,* missing income data, or the absent voting rights of US territories). 

Our hope is that this dashboard draws attention to suppressed communities, while encouraging viewers to think critically about any and all factors that inhibit turnout: from voting location sparsity, to misleading, media-disseminated poll results. 

## Installation

*Please note:* the following steps are intended for a Linux environment.

#### Clone and access the repository in a location of your choice:
```
git clone https://github.com/Anmol-Srivastava/voter-suppression-analysis.git
cd voter-suppression-analysis
```

#### One-time set-up and activation of the necessary environment: 
```
conda env create -f environment.yml
conda activate vsa
pip install -e
python setup.py install --user
```

#### Generate the most up-to-date dashboard:

*Please note:* the output should indicate the location of your generated file. Simply launch the `.html` file in your browser of choice, all interactivity and features are pre-loaded into the file's JS scripts.

```
cd voter_suppression_analysis
python generate.py
```

## Structure

- `docs`: early-stage functional and component specifications, technology reviews, presentations, and `pylint` test outputs
- `examples`: guides for exploring the visualizations
- `voter_suppression_analysis`: main module, with python scripts for processing data and generating dashboard 
  - `data`: raw, sanitized, and dummy data, with an addtional `README`
  - `figures`: mid-development and final python-generated figures (dynamic `.html` files)
  - `tests`: python scripts for testing cleaning and visualization steps

## Team

This project was developed by the following team of graduate students in the UW Master's in Data Science (MSDS) program:

- [Andres De La Fuente](https://github.com/Oponn-1)
- [Anmol Srivastava](https://github.com/Anmol-Srivastava)
- [Juan Solorio](https://github.com/JUAN-SOLORIO)

## License

This project is categorized under the [MIT](./LICENSE) license. 
