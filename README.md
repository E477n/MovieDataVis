# Decision Making of Movie Release Date

## Introduction
A mathematical model for the decision making of movie release date. 

Visualizations of movie data have also been done to provide a better cooperation between human decision and machine decision. 

## Problem Analysis
The decision making of movie release date is a multi dimension problem. Factors that impact the decision making process can be decomposed to 
- Historical Box Office Receipts
- Competitors
- Performance of movies in same genre
- Franchise
- Budget

Other factors like casting, director and studio can also be effective influencers, but they are not considered at the moment.

Thus the model needs to consider all these factors comprehensively to give a convincing result. AHP has been used in this case to construct the model, while the RCP included in this process can be used to calculate the weight vector for the final Weighted Sum Model.

## Algorithm
### Analytic Hierarchy Model
There are 5 factors impact the goal, which is finding the best date to release a movie, so M = 5. And there could be N choices of date (every Friday in the chosen time period). So the AHM can be constructed as a M * N matrix, where M is the number of criteria, and N is the number of alternatives.
### Linear Scale
The simple linear scale was used for quantifying each factor. (see algoMerge/algoMerge.py)
### Real Continuous Pairwise Comparison
RCP method was adopted here to calculate the weight of 5 factors. Saaty’s 1-9 Scale of Pairwise Comparisons was used to compare the importance between each two factors to build the RCP matrix. 

After the 5*5 matrix was built, there was consistency checking needed to make sure that the largest eigenvalues and corresponding eigenvectors of the matrix are effective to be set as weight of factors.
Here we use

<center> CR = CI/RI </center>

to do the consistency checking. CI = (λ-n)/(n-1), λ is the largest eigenvalue of the built 5 * 5 matrix, while RI, the Random Consistency Index, equals 1.12 when index = 5.

The consistency checking can be passed if CR < 0.1 . Otherwise the RCP matrix need to be rebuilt until it passes the consistency checking. Then we could use the normalized eigenvector corresponding to the largest eigenvalue as the weight vector for the Weighted Sum Model.

## Process Data
### Collecting
Up to 90% of data in database was collected from BoxOfficeMojo, and the python scrapy file can be found in dataCollect/collect_boxOfficeMojo.py. Manual collecting was also adopted since a little part of data was missing.
### Cleaning
Data collected at the first stage was not consistent enough to be put into formulas executing calculation. So different data cleaning method was executed for each collection to transfer date to week number, stirng to number, thousand to million, etc.
### Quantifying
The model uses different linear scale for each factor to quantify irregular data to calculable numbers.
### Merge
Use the weight vector which has been calculated by RCP matrix as the weight vector for all the factors. Then we have the final grading of each alternatives(Fridays)
## User Interface
### Input Field
- movie name
- start date & end date
- movie genres
- franchise (optional)
- production budget
![](img/input.png)

### Output
- grading table of final results and each factor in descending order
- grading heat map of final results and each factor
![](img/final%20result.png)

### Data Charts
![](img/factor1.png)
![](img/factor2.png)
![](img/factor5.png)

## Installation
### Dependencies
- dash
- pymongo
- pyquery
- numpy
- statsmodels
### Database
Install mongodb in local environment, use 'movie_db' as the database name and import all the json files in json directory as collections.

## References
[1] Saptarshi Sasmal, K. Ramanjaneyulu and Nagesh R. Iyer, “Condition Ranking and Rating of Bridges Using Fuzzy Logic”, March, 2012.

[2] Ben-Arieh, D. & Triantaphyllou, E. (1992). Quantifying data for group technology with weighted fuzzy features, Int. J. of Production Research, Vol. 30, pp. 1285-1299. 

[3] Bridgman, P. W. (1922). Dimensional analysis. New Haven, CT: Yale University Press.

[4] Saaty, T.L. (1994). Fundamentals of decision making and priority theory with the AHP, RWS 
Publications, Pittsburgh.

[5] Nihar B. Shah, Martin J (2018). Wainwright. Simple, Robust and Optimal Ranking from Pairwise Comparisons, Journal of Machine Learning Research 18 (2018) 1-38