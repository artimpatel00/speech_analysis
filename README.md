# speech_analysis

The data for the project was web scraped from the Federal Reserve Website [1] using a GitHub scraper [2]. Both current and archived speeches and press releases were scraped dating from 1996 to present. VIX data was retrieved from yahoo finance historical data [3]. Recessionary dates were found from Wikipedia [4]. All the csv files were saved in order to easily import them when needed.

 The speeches and archived speeches were both filtered to only include those relevant to monetary policy. The archived speeches, press releases and archived press releases were then concatenated into one dataframe. The VIX data was imported and merged with the rest of the data. Any dates of speeches/press releases that were weekend dates were converted to the following weekday date. Since this is a classification task, any VIX level above 25 was indicated as a positive class and anything below was negative. For the recession labels, dates from Wikipedia were used to identify if the date of the speech/press release was a recessionary date. These labels were chosen in order to find speeches related to each other based on the state of the economy and policies implemented.

The goal in building this model was to extract learned word embeddings to then see if certain words or phrases cluster together. Cosine similarity for word embeddings and vectors for phrases and entire speeches were used to find which words/phrases are most associated with higher VIX levels and recessionary times.

[1] https://www.federalreserve.gov/newsevents/speeches.htm
[2] https://github.com/kathrinv/what-do-you-mean/blob/master/webscraping_and_data_preparation.ipynb
