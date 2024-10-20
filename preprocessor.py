import pandas as pd

def preprocess(df_till_2016,df_2020,df_2024):


    # Dropping Duplicates From Merge 'df_till_2016','df_2020'& 'df_2024'
    df_till_2016.drop_duplicates(inplace=True)
    df_2020.drop_duplicates(inplace=True)
    df_2024.drop_duplicates(inplace=True)

    # One Hot Encoding Medals
    df_till_2016 = pd.concat([df_till_2016, pd.get_dummies(df_till_2016['Medal'])], axis=1)
    df_2020 = pd.concat([df_2020, pd.get_dummies(df_2020['Medal'])], axis=1)
    df_2024 = pd.concat([df_2024, pd.get_dummies(df_2024['Medal'])], axis=1)

    # Concatenate all & 2020 Data
    df_all = pd.concat([df_till_2016, df_2020])

    # Concatenate all & 2024 Data
    df_all = pd.concat([df_all, df_2024])

    return df_all