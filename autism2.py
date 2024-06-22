import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import adjustText  # You need to install this package: pip install adjustText
syear=2015
eyear=2022
# Load the data
df = pd.read_csv('autism_prevalence_studies_20240621.csv')

# Convert 'Study Years' to string type
df['Study Years'] = df['Study Years'].astype(str)

# Print all unique country names
print("Unique Countries:")
for i, country in enumerate(df['Country'].unique()):
    print(f"{i+1}. {country}")

# Ask the user to select a country
country_num = int(input("Enter the number of the country you want to visualize: "))
country = df['Country'].unique()[country_num-1]

# Filter data for the selected country and the fixed year range
df_country = df[df['Country'] == country]

# Plotting
plt.figure(figsize=(10, 6))
texts = []
for _, row in df_country.iterrows():
    study_years = row['Study Years'].split(',')
    for study_year in study_years:
        if '-' in study_year:  # it's a range
            start_year, end_year = map(int, study_year.split('-'))
            if syear <= start_year <= eyear or syear <= end_year <= eyear:
                plt.hlines(y=row['ASD Prevalence Estimate per 1,000'], xmin=start_year, xmax=end_year, color='k')
                label = f"{row['Age Range']} | {int(row['Number of Cases']) if pd.notnull(row['Number of Cases']) else ''}"
                texts.append(plt.text(start_year, row['ASD Prevalence Estimate per 1,000'], label, ha='right', fontsize=8))
        elif study_year.isdigit():  # it's a single year
            year = int(study_year)
            if syear <= year <= eyear:
                plt.hlines(y=row['ASD Prevalence Estimate per 1,000'], xmin=year-0.25, xmax=year+0.25, color='k')
                label = f"{row['Age Range']} | {int(row['Number of Cases']) if pd.notnull(row['Number of Cases']) else ''}"
                texts.append(plt.text(year, row['ASD Prevalence Estimate per 1,000'], label, ha='right', fontsize=8))

plt.xlabel('Study Years')
plt.ylabel('ASD Prevalence Estimate per 1,000')
plt.title(f'Autism Prevalence Graph for {country}')
adjustText.adjust_text(texts)  # Adjust text positions to minimize overlap
plt.savefig(f"{country}.jpg",dpi=300)
plt.show()

