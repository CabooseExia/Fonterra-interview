import pandas as pd

# # Sample data frames
# data1 = {
#     'A': [1, 2, 3],
#     'B': [4, 5, 6],
#     'C': [7, 8, 9],
#     'D': [10, 11, 12],
#     'E': [13, 14, 15],
#     'F': [16, 17, 18],
#     'G': [19, 20, 21],
#     'H': [22, 23, 24],
#     'I': [25, 26, 27],
#     'J': [28, 29, 30]
# }

# data2 = {
#     'A': [1, 2, 3],
#     'B': [34, 35, 36],
#     'C': [37, 38, 39],
#     'D': [40, 41, 42],
#     'E': [43, 44, 45],
#     'F': [46, 47, 48],
#     'G': [49, 50, 51],
#     'H': [52, 53, 54],
#     'I': [55, 56, 57],
#     'J': [58, 59, 60]
# }

# df1 = pd.DataFrame(data1)
# df2 = pd.DataFrame(data2)

# # Join the data frames based on the first 9 columns
# result = pd.merge(df1.iloc[:, :9], df2.iloc[:, :9], on=list(df1.columns[:9].tolist()))

# print(result)
# Create a sample DataFrame
data = {'A': [1, 2, 3, 4, 5]}
df = pd.DataFrame(data)

# Define a mapping dictionary to convert numbers to strings
mapping = {1: 'One', 2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five'}

# Replace the 'A' column with strings using the mapping
df['A'] = df['A'].map(mapping)

print(df)