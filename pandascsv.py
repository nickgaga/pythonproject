import pandas as pd

df = pd.read_csv('orders.csv')

print(df)

media_colonna = df["total_price"].mean()
somma_colonna = df["total_price"].sum()


print("Somma della colonna 'nome_colonna':", somma_colonna)
print("Media della colonna 'nome_colonna':", media_colonna)