import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('compressed_data.csv')
df.head()
df.info()

# checking missing values

print(df.isnull().sum())

# Handling missing values

df['last review'] = pd.to_datetime(df['last review'], errors = 'coerce')
df.info()
df.fillna({'reviews per month' : 0, 'last review': df['last review'].min()}, inplace = True)
df.dropna(subset = ['NAME','host name'], inplace = True)
print(df.isnull().sum())
df = df.drop(columns=["license","house_rules"], errors = 'ignore')
df.head()


# Remove dollar signs and convert datatype from object to float

df['price'] = df['price'].replace('[$,]', '', regex=True).astype(float)
df['service fee'] = df['service fee'].replace('[$,]', '', regex=True).astype(float)
df.head()

#remove duplicates

df.drop_duplicates(inplace = True)
df.info()

#descriptive statistics

df.describe()

# visulization
# Distribution listing Prices

plt.figure(figsize = (10,6))
plt.hist(df['price'].dropna(), bins=50,color='red',edgecolor='black')
plt.title('Distribution of listing prices')
plt.xlabel('Price $')
plt.ylabel('Frequency')
plt.show()

#The histrograml shows a fairly even distribution of listing
prices across different ranges, indicating no particular concentration of listings in any 
specific price range.

# How different room types distributed?

df['room type']

plt.figure(figsize = (8,5))
counts = df['room type'].value_counts()

plt.bar(counts.index, counts.values, color="pink")
plt.title('room type distribution')
plt.xlabel('room type')
plt.ylabel('Count')
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

# Listing Distributed across different neighborhoods?

plt.figure(figsize = (12,8))
counts = df['neighbourhood group'].value_counts()

plt.barh(counts.index, counts.values, color="lightgreen")
plt.title('Number of Listings by Neighborhood Group')
plt.xlabel('Counts')
plt.ylabel('Neighbourhood Group')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

# What is the relationship between price and room type

plt.figure(figsize = (10,6))

order = df['room type'].dropna().unique()

data = [df[df['room type']== rt]['price'].dropna() for rt in order]
box = plt.boxplot(data, labels=order, patch_artist=True)
colors = ['#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00']
for patch, color in zip(box['boxes'],colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)
    
plt.title('Price vs Room Type')
plt.xlabel('Room type')
plt.ylabel('Price $')
plt.tight_layout()
plt.show()

# How has the number of reviews change over with time

df['last review'] = pd.to_datetime(df['last review'])

reviews_over_time = df.groupby(df['last review'].dt.to_period('M')).size()

plt.figure(figsize = (12,8))
reviews_over_time.plot(kind='line',color='red')
plt.title('Number of Reviews Over Time')
plt.xlabel('Date')
plt.ylabel('Number of Reviews')
plt.show()