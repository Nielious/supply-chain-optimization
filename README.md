# Supply Chain Optimizer

Retail discount optimization using Python, Pandas, and Linear Programming.


## Problem

Cleaned and analyzed retail sales data and revealed that Furniture category among other categories brings minimal profit despite huge sales among of them. This is related to ineffective discount policy and sub-category Tables and Bookcases generates negative profit and offsets all profits of Furniture


## Solution

Built a Linear Programming model using PuLP to find optimal solution for discount policy for all sub-categories of furniture to increase profits and make all sub-categories positive in profit


## Results

Tables   from    -$30,574       to     +$23,503
Bookcases    from    -$14,548    to   +$9,707 
Chairs    from    +$14,419     to      +$47,264
Furnishings     from     +$12,570    to     +$21,740

Total old profit: -18,133 
Total new profit: 102,214
Increase: 120,347

<img width="1000" height="600" alt="Figure1" src="https://github.com/user-attachments/assets/51ee77d3-6194-4648-ab73-b7b7349ab31a" />


## Tech Stack

- Python, Pandas, Matplotlib
- PuLP (Linear Programming)


## Dataset

Superstore Sales Dataset — 9,994 rows, 21 columns, 2014–2017
