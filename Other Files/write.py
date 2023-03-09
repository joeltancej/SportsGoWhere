import pandas as pd
import converter

# this code was used to add 2 new columns that display the latitude and longitude converted from the SVY21 coordinates

file_name = "Datasets/hdbcarparks.xlsx"
df = pd.read_excel(file_name) #Read Excel file as a DataFrame

df['x'] = converter.convertx(df['x_coord'], df['y_coord'])
df['y'] = converter.converty(df['x_coord'], df['y_coord'])
#Display top 5 rows to check if everything looks good
df.head(5)

#To save it back as Excel
df.to_excel("Datasets/converted.xlsx") #Write DateFrame back as Excel file