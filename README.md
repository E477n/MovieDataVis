# Decision Making of Movie Release Date
## Dependencies
- dash
- pymongo
- pyquery
- statsmodels
## Introduction
A mathematical model for the decision making of movie release date. 
And the visualizations of movie data have also been done to provide a better cooperation between human decision and machine decision. 

## Problem Analysis
The decision making of movie release date is a multi dimension problem. Factors that impact the decision making process can be decomposed to 
- Historical Box Office Receipts
- Competitors
- Performance of movies in same genre
- Franchise
- Budget

Other factors like casting, director and studio can also be effective influencers, but they are not considered at the moment.

## Algorithm
### Analytic Hierarchy Model
There are 5 factors impact the goal, which is finding the best date to release a movie, so M = 5. And there could be N choices of date (every Friday in the chosen time period). So the AHM can be constructed as a M * N model, where M is the number of criteria, and N is the number of alternatives.
### Linear Scale
The simple linear scale was used for quantifying each factor.
### Real Continuous Comparison
RCP method was adopted here to calculate the weight of 5 factors. Saaty’s 1-9 Scale of Pairwise Comparisons was used to compare the importance between each two factors to build the RCP matrix. 

After the 5*5 matrix was built, there was consistency checking needed to make sure that the largest eigenvalues and corresponding eigenvectors of the matrix are effective to be set as weight of factors.
Here we use
 
CR = CI/RI


to do this. CI = (λ-n)/(n-1), λ is the largest eigenvalue of the built 5 * 5 matrix, while RI, the Random Consistency Index, is 1.12 when index = 5.

The consistency checking can be passed if CR < 0.1 . Otherwise the RCP matrix need to be rebuilt until it passes the consistency checking. Then we could use the normalized eigenvector corresponding to the largest eigenvalue as the weight vector for the Weighted Sum Model.

## Process Data
### Collecting
Up to 90% of data in database was collected from BoxOfficeMojo, and the python scrapy file can be found in dataCollect/collect_boxOfficeMojo.py. Manual collecting was also adopted since a little part of data was missing.
### Cleaning
Data collected at the first stage was not consistent enough to be put into formulas executing calculation. So different data cleaning method was executed for each collection to transfer date to week number, stirng to number, thousand to million, etc.
### Quantifying
### Merge

## Input & Output
### Input
### Output

## User Interface
