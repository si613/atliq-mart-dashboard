# 📊 AtliQ Mart Promotion Effectiveness Dashboard

## 🎯 Objective

To analyze and evaluate the **effectiveness of marketing campaigns** run during **Diwali 2023** and **Sankranti 2024** across AtliQ Mart’s 50+ supermarkets in South India. The goal is to help the **Sales Director** identify which promotions, products, and stores performed best, enabling **data-driven decisions** for future campaigns.

---

## 🧩 Problem Statement (Elaborated)

AtliQ Mart, a leading retail chain in South India, runs multiple promotional campaigns throughout the year to boost product sales and drive footfall to stores. During the festive periods of **Diwali 2023** and **Sankranti 2024**, the company invested significantly in various types of promotions across different stores and product categories.

However, after the campaigns ended, the Sales and Marketing leadership lacked **clear and consolidated insights** on:

- Which **stores** generated the most revenue from promotions?
- Which **promotion types** (Discount, Cashback, BOGOF) were most effective?
- How did **product performance** vary by promotion type?
- Were there **regional trends**, such as certain states or cities responding better to specific types of offers?
- Did these promotions lead to **actual sales uplift**, or simply discount-driven churn?

Without these insights, it is difficult for the company to:

- Justify the **ROI** of their campaigns
- **Optimize future promotional budgets**
- Develop **personalized promotion strategies** per region or product

This dashboard project was initiated to bridge that gap. Using structured data from the company’s transactional database and metadata from products, stores, and campaigns, we performed a comprehensive analysis and presented the results through an interactive, user-friendly dashboard.

---

## 🛠️ Project Architecture

| Layer         | Technologies Used                          |
|---------------|---------------------------------------------|
| Database      | SQLite (`retail_events_db`)                |
| Backend       | Python + SQL                               |
| Data Source   | CSV files (4 dimension + 1 fact table)     |
| Frontend      | Streamlit + Plotly                         |
| Environment   | Local virtual environment (`venv`)         |

---

## 📌 Business Questions Solved

| # | Question                                                                 | Status   |
|---|--------------------------------------------------------------------------|----------|
| 1 | Identify **Top 10 stores** by **Incremental Revenue (IR)**              | ✅ Done   |
| 2 | Identify **Bottom 10 stores** by **Incremental Sold Units (ISU)**       | ✅ Done   |
| 3 | Find **Top 2 promotion types** by **Incremental Revenue**               | ✅ Done   |
| 4 | Find **Bottom 2 promotion types** by **Incremental Sold Units**         | ✅ Done   |
| 5 | Compare **Discount vs BOGOF/Cashback** promotions                       | ✅ Done   |
| 6 | Identify **products/categories** with high responsiveness to promos     | ✅ Done   |
| 7 | Analyze **state-wise and city-wise** performance via heatmaps           | ✅ Done   |
| 8 | Calculate **promotion-wise product response** using total sales lift    | ✅ Done   |

---

## 🔁 Workflow Process

1. **Data Understanding**  
   Explored the schema: `fact_events`, `dim_campaigns`, `dim_stores`, `dim_products`

2. **SQL Query Design**  
   Wrote parameterized and reusable SQL queries to calculate:
   - Incremental Revenue
   - Sales lift
   - Promotion effectiveness
   - City and state performance

3. **Backend Integration**  
   Created Python functions to execute queries and return DataFrames.

4. **Streamlit Frontend**  
   - Developed 4 main tabs:
     - KPI Overview
     - Store Performance
     - Promotion Type Analysis
     - Product & Category Analysis
   - Used Plotly for bar charts, heatmaps, and tables

---

## ⚙️ Challenges and Solutions

| Challenge                                                   | Solution                                                                 |
|-------------------------------------------------------------|--------------------------------------------------------------------------|
| Sales uplift metrics not directly available                 | Created derived metrics (IR, ISU, lift) using SQL and formulae           |
| Handling orientation and missing args in bar charts         | Adjusted Plotly `orientation`, fixed required arguments                  |
| Interpreting promo vs product response across categories    | Created category-promotion matrix to visualize correlation               |
| Handling empty datasets (no data to visualize)              | Added conditional rendering in Streamlit to show `st.info()` messages    |
| Ensuring dynamic filters didn’t break charts                | Used default `sort_values` and included error handling                   |

---

## ✅ Key Features of the Dashboard

- 📈 **Live KPIs**: Total Revenue, Units Sold, Stores Active, Unique Promotions
- 🏪 **Store Insights**: Top & bottom performing stores by revenue and ISU
- 🎁 **Promotion Breakdown**: Effectiveness of discount vs cashback vs BOGOF
- 🛒 **Product & Category Impact**: Which items responded best to promotions


---

## 💼 Real-World Use Cases

| Department     | Use Case                                                                 |
|----------------|--------------------------------------------------------------------------|
| Sales          | Prioritize top-performing store locations for future campaigns          |
| Marketing      | Refine promotion types for best-performing categories                   |
| Product Teams  | Identify products highly responsive to offers for bundling strategies   |
| Strategy       | Understand regional preferences using city/state heatmaps               |

---

## 🚀 Future Improvements

- Add **user-uploaded CSV** functionality to simulate real-time campaign input.
- Incorporate **profitability** metrics, not just units and revenue.
- Enable **drilldowns** by individual store or campaign via dropdowns.
- Add **trend line analysis** to show uplift progression across dates.

---


