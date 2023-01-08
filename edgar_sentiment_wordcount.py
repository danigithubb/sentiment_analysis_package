### Takes all the clean text 10-k files in the input folder, 
# counts the number of words in the document belonging to a particular sentiment and 
# outputs the results to the output file.


#input = input folder, reference = sentiment dict

def write_document_sentiments(input_folder, output_file):
    
    # 1 # import sentiment dicitonary(list) for each type & make LOWER
    import pandas as pd
    import os
    import ref_data as edgar_data
    
    key_sentiments = ['Positive','Negative','Uncertainty','Constraining','Litigious','StrongModal','WeakModal']

    big_list = []  #massive list with all words separated in sublists by sentiment
    for item in key_sentiments:
        sublist = edgar_data. get_sentiment_word_dict()[item]
        
        sublist_lower = []
        for item2 in sublist:
            sublist_lower.append(item2.lower())
        
        big_list.append(sublist)

    #reference each sentiment category in big_list as big_list[0]

    # 2 # create empty dataframe
    part4_df = pd.DataFrame(columns = ['Symbol','ReportType','FilingDate','TotalWords','Positive','Negative','Uncertainty','Constraining','Litigious','StrongModal','WeakModal','Positve%Score','Negative%Score','PolarityScore'])

    # 3 # iterate through txt files in input folder
    for item in os.listdir(input_folder):
        path = input_folder
        if '.txt' in item:
            with open(os.path.join(path, item), 'rt',encoding="utf8") as dafile:
                text = dafile.read()
                new_text = text.replace(',',' ').replace('.',' ')
                document_list = new_text.split(sep = ' ')

    # 4 # for each:
    #count positive, negative, uncertainty, litigious, constrianing, superfluous,interesting, modal
    #compare the two lists
        #positive count big_list[0]
        count_pos = 0
        for word in big_list[0]:
            count_pos = count_pos + document_list.count(word)
        #negative count big_list[1]
        count_neg = 0
        for word in big_list[1]:
            count_neg = count_neg + document_list.count(word)
        #uncertainty count big_list[2]
        count_unc = 0
        for word in big_list[2]:
            count_unc = count_unc + document_list.count(word)
        #constraining count big_list[3]
        count_con = 0
        for word in big_list[3]:
            count_con = count_con + document_list.count(word)
        #litigious count big_list[4]
        count_lit = 0
        for word in big_list[4]:
            count_lit = count_lit + document_list.count(word)
        #strongmodal count big_list[5]
        count_smod = 0
        for word in big_list[5]:
            count_smod = count_smod + document_list.count(word)
        #weakmodal count big_list[6]
        count_wmod = 0
        for word in big_list[6]:
            count_wmod = count_wmod + document_list.count(word)
    
    # 5 # populate row in dataframe
    #get SYMBOL, REPORT TYPE, FILING DATE HERE!!!!!!!
        symbol = item[:4]
        type = item[5:9]
        date = item[10:20]
        tot_words = len(document_list)
        pos_score = (count_pos/tot_words)*100
        neg_score = (count_neg/tot_words)*100
        pol_score = (count_pos - count_neg)/tot_words
    #add row to end of DataFrame 
        part4_df.loc[len(part4_df.index)] = [symbol, type, date,tot_words,count_pos, count_neg,count_unc,count_con,count_lit,count_smod,count_wmod,pos_score,neg_score,pol_score ]  

    #output dataframe as a CSV file
    sentiment_counts_table = part4_df.to_csv(output_file)

    return sentiment_counts_table