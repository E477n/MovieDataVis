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


## Data Collecting
Up to 90% of data in database was collected from BoxOfficeMojo, and the python scrapy file can be found in dataCollect/collect_boxOfficeMojo.py. Manual collecting was also adopted since a little part of data was missing.