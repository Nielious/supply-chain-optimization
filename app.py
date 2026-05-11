import pandas as pd
from pulp import *
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv(r'C:\Users\Dell\Documents\supply_chain_optimizer\data\superstore_clean.csv')

df['Profit_Margin'] = df['Profit'] / df['Sales']
furniture = df[df['Category'] == 'Furniture']
stats = furniture.groupby('Sub-Category').agg(
    avg_margin=('Profit_Margin', 'mean'),
    avg_discount=('Discount', 'mean'),
    total_sales=('Sales', 'sum')
).reset_index()

# x1, x2, x3, x4 — новые скидки
x1 = LpVariable("discount_Tables",      lowBound=0, upBound=0.5)
x2 = LpVariable("discount_Bookcases",   lowBound=0, upBound=0.5)
x3 = LpVariable("discount_Chairs",      lowBound=0, upBound=0.5)
x4 = LpVariable("discount_Furnishings", lowBound=0, upBound=0.5)

model = LpProblem("Optimization", LpMaximize)

model += (
    stats.loc[stats['Sub-Category']=='Tables',      'total_sales'].values[0] * 
    (stats.loc[stats['Sub-Category']=='Tables',     'avg_margin'].values[0] + 
     stats.loc[stats['Sub-Category']=='Tables',     'avg_discount'].values[0] - x1)
    +
    stats.loc[stats['Sub-Category']=='Bookcases',   'total_sales'].values[0] * 
    (stats.loc[stats['Sub-Category']=='Bookcases',  'avg_margin'].values[0] + 
     stats.loc[stats['Sub-Category']=='Bookcases',  'avg_discount'].values[0] - x2)
    +
    stats.loc[stats['Sub-Category']=='Chairs',      'total_sales'].values[0] * 
    (stats.loc[stats['Sub-Category']=='Chairs',     'avg_margin'].values[0] + 
     stats.loc[stats['Sub-Category']=='Chairs',     'avg_discount'].values[0] - x3)
    +
    stats.loc[stats['Sub-Category']=='Furnishings', 'total_sales'].values[0] * 
    (stats.loc[stats['Sub-Category']=='Furnishings','avg_margin'].values[0] + 
     stats.loc[stats['Sub-Category']=='Furnishings','avg_discount'].values[0] - x4)
)

model += ((stats.loc[stats['Sub-Category']=='Tables',     'avg_margin'].values[0] + 
     stats.loc[stats['Sub-Category']=='Tables',     'avg_discount'].values[0] - x1) >= 0.1)
model += ((stats.loc[stats['Sub-Category']=='Bookcases',  'avg_margin'].values[0] + 
     stats.loc[stats['Sub-Category']=='Bookcases',  'avg_discount'].values[0] - x2) >= 0.1)
model += ((stats.loc[stats['Sub-Category']=='Chairs',     'avg_margin'].values[0] + 
     stats.loc[stats['Sub-Category']=='Chairs',     'avg_discount'].values[0] - x3) >= 0.1)
model += ((stats.loc[stats['Sub-Category']=='Furnishings','avg_margin'].values[0] + 
     stats.loc[stats['Sub-Category']=='Furnishings','avg_discount'].values[0] - x4) >= 0.1)


model += (x1 <= stats.loc[stats['Sub-Category']=='Tables',     'avg_discount'].values[0] + 0.05)
model += (x2 <= stats.loc[stats['Sub-Category']=='Bookcases',  'avg_discount'].values[0] + 0.05)
model += (x3 <= stats.loc[stats['Sub-Category']=='Chairs',     'avg_discount'].values[0] + 0.05)
model += (x4 <= stats.loc[stats['Sub-Category']=='Furnishings','avg_discount'].values[0] + 0.05)


model += (x3 >= stats.loc[stats['Sub-Category']=='Chairs',     'avg_discount'].values[0] - 0.10) 
model += (x4 >= stats.loc[stats['Sub-Category']=='Furnishings','avg_discount'].values[0] - 0.10)

model.solve(PULP_CBC_CMD(msg=0))
print(x1.varValue, x2.varValue, x3.varValue, x4.varValue)






old_profit_tables = stats.loc[stats['Sub-Category']=='Tables', 'total_sales'].values[0] * \
                    stats.loc[stats['Sub-Category']=='Tables', 'avg_margin'].values[0]

new_margin_tables = stats.loc[stats['Sub-Category']=='Tables', 'avg_margin'].values[0] + \
                    stats.loc[stats['Sub-Category']=='Tables', 'avg_discount'].values[0] - x1.varValue

new_profit_tables = stats.loc[stats['Sub-Category']=='Tables', 'total_sales'].values[0] * new_margin_tables





old_profit_bookcases = stats.loc[stats['Sub-Category']=='Bookcases', 'total_sales'].values[0] * \
                    stats.loc[stats['Sub-Category']=='Bookcases', 'avg_margin'].values[0]

new_margin_bookcases = stats.loc[stats['Sub-Category']=='Bookcases', 'avg_margin'].values[0] + \
                    stats.loc[stats['Sub-Category']=='Bookcases', 'avg_discount'].values[0] - x2.varValue

new_profit_bookcases = stats.loc[stats['Sub-Category']=='Bookcases', 'total_sales'].values[0] * new_margin_bookcases




old_profit_chairs = stats.loc[stats['Sub-Category']=='Chairs', 'total_sales'].values[0] * \
                    stats.loc[stats['Sub-Category']=='Chairs', 'avg_margin'].values[0]

new_margin_chairs = stats.loc[stats['Sub-Category']=='Chairs', 'avg_margin'].values[0] + \
                    stats.loc[stats['Sub-Category']=='Chairs', 'avg_discount'].values[0] - x3.varValue

new_profit_chairs = stats.loc[stats['Sub-Category']=='Chairs', 'total_sales'].values[0] * new_margin_chairs




old_profit_furnishings = stats.loc[stats['Sub-Category']=='Furnishings', 'total_sales'].values[0] * \
                    stats.loc[stats['Sub-Category']=='Furnishings', 'avg_margin'].values[0]

new_margin_furnishings = stats.loc[stats['Sub-Category']=='Furnishings', 'avg_margin'].values[0] + \
                    stats.loc[stats['Sub-Category']=='Furnishings', 'avg_discount'].values[0] - x4.varValue

new_profit_furnishings = stats.loc[stats['Sub-Category']=='Furnishings', 'total_sales'].values[0] * new_margin_furnishings



categories = ['Tables', 'Bookcases', 'Chairs', 'Furnishings']
old_profits = [old_profit_tables, old_profit_bookcases, old_profit_chairs, old_profit_furnishings]
new_profits = [new_profit_tables, new_profit_bookcases, new_profit_chairs, new_profit_furnishings]


x = np.arange(len(categories))
width = 0.35
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(x - width/2, old_profits, width, label='Текущая прибыль', color='red', alpha=0.7)
ax.bar(x + width/2, new_profits, width, label='Оптимизированная прибыль', color='green', alpha=0.7)
ax.set_xlabel('Sub-Category')
ax.set_ylabel('Прибыль ($)')
ax.set_title('Furniture: до и после оптимизации скидок')
ax.set_xticks(x)
ax.set_xticklabels(categories)
ax.legend()
ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
plt.tight_layout()
plt.show()
