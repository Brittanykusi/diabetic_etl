# import packages
import pandas as pd
import numpy as np
import uuid

# import datasets
data = pd.read_csv('/Users/brittanykusi-gyabaah/Downloads/diabetic_data (1).csv')
mapping = pd.read_csv('/Users/brittanykusi-gyabaah/Documents/diabetic_etl/Data/IDs_mapping.csv')
print(data)
print(mapping)

#descibe data
data.columns
# Index(['encounter_id', 'patient_nbr', 'race', 'gender', 'age', 'weight',
    #    'admission_type_id', 'discharge_disposition_id', 'admission_source_id',
    #    'time_in_hospital', 'payer_code', 'medical_specialty',
    #    'num_lab_procedures', 'num_procedures', 'num_medications',
    #    'number_outpatient', 'number_emergency', 'number_inpatient', 'diag_1',
    #    'diag_2', 'diag_3', 'number_diagnoses', 'max_glu_serum', 'A1Cresult',
    #    'metformin', 'repaglinide', 'nateglinide', 'chlorpropamide',
    #    'glimepiride', 'acetohexamide', 'glipizide', 'glyburide', 'tolbutamide',
    #    'pioglitazone', 'rosiglitazone', 'acarbose', 'miglitol', 'troglitazone',
    #    'tolazamide', 'examide', 'citoglipton', 'insulin',
    #    'glyburide-metformin', 'glipizide-metformin',
    #    'glimepiride-pioglitazone', 'metformin-rosiglitazone',
    #    'metformin-pioglitazone', 'change', 'diabetesMed', 'readmitted'],
    #   dtype='object')
data.shape
# (101766, 50)

################################################################################################
##### The idea that I have is use extract a sample of qualifying data to do an analysis on #####      
################################################################################################

#drop columns in the table 
df = data.drop(columns=['encounter_id','payer_code','weight', 'examide', 'citoglipton'])
df 

# drop rows with missing values
df.replace('?', pd.np.nan, inplace=True)
df.replace('', pd.np.nan, inplace=True)
df = df.dropna(subset=['medical_specialty'])
df.drop_duplicates()

# data set size
df.shape
#(51817, 45)


# list of all columns names
df.columns
# Index(['race', 'gender', 'age', 'admission_type_id',
#        'discharge_disposition_id', 'admission_source_id', 'time_in_hospital',
#        'medical_specialty', 'num_lab_procedures', 'num_procedures',
#        'num_medications', 'number_outpatient', 'number_emergency',
#        'number_inpatient', 'diag_1', 'diag_2', 'diag_3', 'number_diagnoses',
#        'max_glu_serum', 'A1Cresult', 'metformin', 'repaglinide', 'nateglinide',
#        'chlorpropamide', 'glimepiride', 'acetohexamide', 'glipizide',
#        'glyburide', 'tolbutamide', 'pioglitazone', 'rosiglitazone', 'acarbose',
#        'miglitol', 'troglitazone', 'tolazamide', 'insulin',
#        'glyburide-metformin', 'glipizide-metformin',
#        'glimepiride-pioglitazone', 'metformin-rosiglitazone',
#        'metformin-pioglitazone', 'change', 'diabetesMed', 'readmitted'],
#       dtype='object')


# change patient_nbr to random number so that the frequency af an individuals encounter is still present
new_patient_ids = dict(zip(df['patient_nbr'].unique(), np.random.randint(1, 1000000, size=df['patient_nbr'].nunique())))
# replace old IDs with new random IDs
df['patient_nbr'] = df['patient_nbr'].map(new_patient_ids)
print(df)
df.columns

# if you just want to create encounter IDs with consecutive values
# df['new_id'] = range(1, len(df)+1)
# df.columns
# df[['new_id', 'race', 'gender', 'age', 'admission_type_id',
#        'discharge_disposition_id', 'admission_source_id', 'time_in_hospital',
#        'medical_specialty', 'num_lab_procedures', 'num_procedures',
#        'num_medications', 'number_outpatient', 'number_emergency',
#        'number_inpatient', 'diag_1', 'diag_2', 'diag_3', 'number_diagnoses',
#        'max_glu_serum', 'A1Cresult', 'metformin', 'repaglinide', 'nateglinide',
#        'chlorpropamide', 'glimepiride', 'acetohexamide', 'glipizide',
#        'glyburide', 'tolbutamide', 'pioglitazone', 'rosiglitazone', 'acarbose',
#        'miglitol', 'troglitazone', 'tolazamide', 'insulin',
#        'glyburide-metformin', 'glipizide-metformin',
#        'glimepiride-pioglitazone', 'metformin-rosiglitazone',
#        'metformin-pioglitazone', 'change', 'diabetesMed', 'readmitted']]



## change range to singular values 
# age
age_map = {'[0-10)': 1, '[10-20)': 2, '[20-30)': 3, '[30-40)': 4,
           '[40-50)': 5, '[50-60)': 6, '[60-70)': 7, '[70-80)': 8,
           '[80-90)': 9, '[90-100)': 10}
df['age'] = df['age'].map(age_map)
df
## change words to values
# race
race_map = {'nan': 999, 'AfricanAmerican': 1, 'Asian': 2,
            'Caucasian': 3, 'Hispanic': 4, 'Other': 999}

df['race'] = df['race'].map(race_map)

print(df['race'])

# gender
gender_map = {'Female': 1, 'Male': 2, 'Unknown/Invalid': 999}

df['gender'] = df['gender'].map(gender_map)

print(df['gender'])

# medical specialty
medical_specialty_map = {'AllergyandImmunology': 1,
                         'Anesthesiology': 2,
                         'Anesthesiology-Pediatric': 2,
                         'Cardiology': 3,
                         'Cardiology-Pediatric': 3,
                         'DCPTEAM': 18,
                         'Dentistry': 4,
                         'Dermatology': 5,
                         'Emergency/Trauma': 6,
                         'Endocrinology': 7,
                         'Endocrinology-Metabolism': 7,
                         'Family/GeneralPractice': 11,
                         'Gastroenterology': 8,
                         'Gynecology': 14,
                         'Hematology': 9,
                         'Hematology/Oncology': 9,
                         'Hospitalist': 18,
                         'InfectiousDiseases': 10,
                         'InternalMedicine': 11,
                         'Nephrology': 12,
                         'Neurology': 13,
                         'Neurophysiology': 13,
                         'Obsterics&Gynecology-GynecologicOnco': 14,
                         'Obstetrics': 14,
                         'ObstetricsandGynecology': 14,
                         'Oncology': 9,
                         'Ophthalmology': 15,
                         'Orthopedics': 16,
                         'Orthopedics-Reconstructive': 16,
                         'Osteopath': 17,
                         'Otolaryngology': 19,
                         'OutreachServices': 18,
                         'Pathology': 20,
                         'Pediatrics': 11,
                         'Pediatrics-AllergyandImmunology': 1,
                         'Pediatrics-CriticalCare': 6,
                         'Pediatrics-EmergencyMedicine': 6,
                         'Pediatrics-Endocrinology': 7,
                         'Pediatrics-Hematology-Oncology': 9,
                         'Pediatrics-InfectiousDiseases': 10,
                         'Pediatrics-Neurology': 13,
                         'Pediatrics-Pulmonology': 25,
                         'Perinatology': 14,
                         'PhysicalMedicineandRehabilitation': 21,
                         'PhysicianNotFound': 999,
                         'Podiatry': 22,
                         'Proctology': 23,
                         'Psychiatry': 24,
                         'Psychiatry-Addictive': 24,
                         'Psychiatry-Child/Adolescent': 24,
                         'Psychology': 24,
                         'Pulmonology': 25,
                         'Radiologist': 26,
                         'Radiology': 26,
                         'Resident': 18,
                         'Rheumatology': 27,
                         'Speech': 18,
                         'SportsMedicine': 18,
                         'Surgeon': 28,
                         'Surgery-Cardiovascular':  28,
                         'Surgery-Cardiovascular/Thoracic': 28,
                         'Surgery-Colon&Rectal': 28,
                         'Surgery-General': 28,
                         'Surgery-Maxillofacial': 28,
                         'Surgery-Neuro': 28,
                         'Surgery-Pediatric': 28,
                         'Surgery-Plastic': 28,
                         'Surgery-PlasticwithinHeadandNeck': 28,
                         'Surgery-Thoracic': 28,
                         'Surgery-Vascular': 28,
                         'SurgicalSpecialty': 28,
                         'Urology': 29}

df['medical_specialty'] = df['medical_specialty'].map(medical_specialty_map)

print(df['medical_specialty'])

# change words to  values
df.replace('No', '0', inplace=True)
df.replace('NO', '0', inplace=True)
df.replace('None', '0', inplace=True)
df.replace('Yes', '1', inplace=True)
df.replace('Up', '2', inplace=True)
df.replace('Down', '3', inplace=True)
df.replace('Steady', '4', inplace=True)
df.replace('Norm', '4', inplace=True)
df.replace('Ch', '1', inplace=True) # ch means a chnage has occured
#tester
df['insulin']

### Exporting the data as csv
df.to_csv('Data/cleaned_data.csv', index=False)
