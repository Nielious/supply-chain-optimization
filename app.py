import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pulp import *

st.set_page_config(page_title="Supply Chain Optimizer", layout="wide")

st.title("Supply Chain Optimizer")
st.markdown("Анализ и оптимизация скидок для розничного магазина")

uploaded_file = st.file_uploader("Загрузи CSV файл", type=['csv'])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success(f"Файл загружен: {df.shape[0]} строк, {df.shape[1]} колонок")

    df['Profit_Margin'] = df['Profit'] / df['Sales']

    # Block 3 - Анализ
    st.header("Анализ по категориям")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Прибыль по категориям")
        category_profit = df.groupby('Category')['Profit'].sum().sort_values()
        st.bar_chart(category_profit)
    
    with col2:
        st.subheader("Средняя маржа и скидка")
        stats_cat = df.groupby('Category')[['Profit_Margin', 'Discount']].mean()
        st.dataframe(stats_cat.style.format("{:.1%}"))

    # Block 4 - Оптимизация
    st.header("Оптимизация скидок — Furniture")
    
    if st.button("Запустить оптимизацию"):
        furniture = df[df['Category'] == 'Furniture']
        stats = furniture.groupby('Sub-Category').agg(
            avg_margin=('Profit_Margin', 'mean'),
            avg_discount=('Discount', 'mean'),
            total_sales=('Sales', 'sum')
        ).reset_index()

        model = LpProblem("Furniture_Discount_Optimization", LpMaximize)
        discount_vars = {
            row['Sub-Category']: LpVariable(
                f"discount_{row['Sub-Category']}", 
                lowBound=0, upBound=0.5
            )
            for _, row in stats.iterrows()
        }

        model += lpSum([
            stats.loc[stats['Sub-Category']==cat, 'total_sales'].values[0] * 
            (stats.loc[stats['Sub-Category']==cat, 'avg_margin'].values[0] + 
             stats.loc[stats['Sub-Category']==cat, 'avg_discount'].values[0] - 
             discount_vars[cat])
            for cat in discount_vars
        ])

        for _, row in stats.iterrows():
            cat = row['Sub-Category']
            model += (row['avg_margin'] + row['avg_discount'] - discount_vars[cat] >= 0.01,
                      f"min_margin_{cat}")
            model += (discount_vars[cat] <= row['avg_discount'] + 0.05,
                      f"max_discount_{cat}")
            if row['avg_margin'] > 0:
                model += (discount_vars[cat] >= row['avg_discount'] - 0.10,
                          f"min_discount_{cat}")

        model.solve(PULP_CBC_CMD(msg=0))

        results = []
        for cat, var in discount_vars.items():
            old = stats.loc[stats['Sub-Category']==cat, 'avg_discount'].values[0]
            new = var.varValue
            old_profit = stats.loc[stats['Sub-Category']==cat, 'total_sales'].values[0] * \
                         stats.loc[stats['Sub-Category']==cat, 'avg_margin'].values[0]
            new_margin = stats.loc[stats['Sub-Category']==cat, 'avg_margin'].values[0] + \
                         stats.loc[stats['Sub-Category']==cat, 'avg_discount'].values[0] - new
            new_profit = stats.loc[stats['Sub-Category']==cat, 'total_sales'].values[0] * new_margin
            results.append({
                'Товар': cat,
                'Старая скидка': f"{old:.1%}",
                'Новая скидка': f"{new:.1%}",
                'Старая прибыль': f"${old_profit:,.0f}",
                'Новая прибыль': f"${new_profit:,.0f}"
            })

        results_df = pd.DataFrame(results)
        st.dataframe(results_df)
        st.success(f"Статус модели: {LpStatus[model.status]}")

else:
    st.info("Загрузи файл чтобы начать анализ")