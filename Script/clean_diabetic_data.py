# import packages
import pandas as pd
import numpy as np

data = pd.read_csv('/Users/brittanykusi-gyabaah/Downloads/diabetic_data (1).csv')
print(data)

# drop rows will missing values
data = data.dropna()
data.replace('?', pd.np.nan, inplace=True)
data.replace('', pd.np.nan, inplace=True)
# drop columns with missing values
data = data.dropna(axis=1)
data

# list of all columns names
data.columns

# create a data dictonary for desired columns
columns = ['gender', 'age', 'admission_type_id', 
           'discharge_disposition_id', 'admission_source_id', 'time_in_hospital', 
           'num_lab_procedures', 'num_procedures', 'num_medications', 
           'number_outpatient', 'number_emergency', 'number_inpatient', 
           'number_diagnoses', 'max_glu_serum', 'A1Cresult', 'metformin', 
           'insulin', 'change', 'diabetesMed', 'readmitted']
# function for creating the data dictionary
def create_data_dictionary(data, columns):
    data_dictionaries = {}
    for col in columns:
        unique_values = data[col].unique()
        data_dict = dict(zip(unique_values, range(len(unique_values))))
        data_dictionaries[col] = data_dict
        print(f"Data Dictionary for df.{col}:")
        print(data_dict)
        print()
    return data_dictionaries

data_dictionaries = create_data_dictionary(data, columns)

# Converting the categorical variables to numerical variables
data.replace(data_dictionaries, inplace=True)

# Counting the number of NaN values remaining in each column to ensure dataset was cleaned properly
print(data.isna().sum())

# Exporting the data dictionary to a csv file
df = pd.DataFrame(data_dictionaries)

df.to_csv ('data/diabetic_data_dictionaries.csv', index = False, header=True)
print (df)

# Reformatting Categorical Columns with their corresponding dictionary values
for col, data_dict in data_dictionaries.items():
    data[col].replace(data_dict, inplace=True)
data
### Exporting the data dictionaries to an Excel file
writer = pd.ExcelWriter('data/diabetic_data_dictionaries.xlsx')
for col, data_dict in data_dictionaries.items():
    pandas.DataFrame.from_dict(data_dict, orient="index").to_excel(writer, sheet_name=col)
writer.save()