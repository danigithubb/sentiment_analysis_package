# PART 5: SENTIMENT ANALYSIS
# input: sentiment_factors.csv, stock_returns_daily.csv
# output: merge df of 1 ticker, report sentiments & scores, daily returns for up to 10 days after 

### TO RUN THIS MODULE CALL:
#   import part5
#   part5.get_merge_df('merge_df.csv')


### PRE-REQUISITES RUN:

# Get table from Part 3b: Yahoo Finance Reference data
#   import ref_data as edgar_data
#   df_returns = edgar_data.get_yahoo_data('2000-01-01', '2020-08-01', 'AAPL')
#   df_returns.to_csv('stock_returns_daily.csv', index=False)


# Get table from Part 4: Sentiment word counts for each stock report
#   import edgar_sentiment_wordcount as edgar_sentiment
#   edgar_sentiment.write_document_sentiments('10k_filings_clean', 'sentiment_factors.csv')

def get_merge_df(sentiment_factors, stock_returns_daily,output_file):
    import pandas as pd
    import os
    ##~~~ open sentiment_factors.csv into a dataframe
    cwd = os.getcwd() #find path name using OS library
    sentiment_factors_df= pd.read_csv(f'{cwd}/{sentiment_factors}',header=None, index_col=0, squeeze=True) #convert to df
    #clean dataframe
    sentiment_factors_df.reset_index(inplace=True)
    sentiment_factors_df.columns = sentiment_factors_df.iloc[0]
    sentiment_factors_df = sentiment_factors_df.drop(sentiment_factors_df.index[[0]])

    ##~~~ open stock_returns_daily file to dataframe 
    cwd = os.getcwd() #find path name using OS library
    stock_returns = pd.read_csv(f'{cwd}/{stock_returns_daily}',header=None, index_col=0, squeeze=True) #convert to df
    stock_returns_df = pd.DataFrame(stock_returns)
    #clean dataframe
    stock_returns_df.reset_index(inplace=True)
    stock_returns_df.columns = stock_returns_df.iloc[0]
    stock_returns_df = stock_returns_df.drop(stock_returns_df.index[[0]])
    #clean and format stock_returns_df date column YYYY-MM-DD
    stock_returns_df['Date']= pd.to_datetime(stock_returns_df['Date'], utc=True)
    stock_returns_df['Date'] = pd.to_datetime(stock_returns_df['Date']).dt.date

    ##~~~ merge two dataframes on DATE column (inner)
    sentiment_factors_df.rename(columns = {'FilingDate':'Date'}, inplace = True)
    sentiment_factors_df['Date'] = pd.to_datetime(sentiment_factors_df['Date']).dt.date
    merge_df = pd.merge(sentiment_factors_df, stock_returns_df, left_on = 'Date', right_on = 'Date', how = 'inner')
    ##~~~ from stock_returns_daily.csv find dates-rows existing in sentiment_factors.csv
    return merge_df.to_csv(output_file)