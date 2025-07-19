import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os
from datetime import datetime

st.set_page_config(
    page_title="AtliQ Mart Dashboard",
    layout="wide",           
    initial_sidebar_state="expanded"
) 

# path to import from scripts
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.query_engine import (
    get_connection,
    get_overall_kpis,
    get_top_10_stores_by_ir,
    get_bottom_10_stores_by_isu,
    get_store_count_by_city,
    get_top_2_promo_types_by_ir,
    get_bottom_2_promo_types_by_isu,
    get_balanced_promotions,
    get_product_response_analysis,
    get_discount_vs_bogof_cashback,
    get_top_categories_by_lift, 
    get_best_performing_products,
    get_worst_performing_products, 
    get_category_promo_correlation_data
)


#Database Connection
conn = get_connection()


# Main Navigation
st.title("🛒 AtliQ Mart Promotion Insights Dashboard")

tabs = st.tabs([
    "📊 Overview & KPIs", 
    "🏬 Store Performance", 
    "🧾 Promotion Analysis", 
    "📦 Product & Category Analysis"
])


# Overview & KPIs (Tab 1)
with tabs[0]:
    st.header("📊 Overview & Key Metrics")

    kpis = get_overall_kpis(conn)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Campaigns", kpis["total_campaigns"])
        st.metric("Avg. Lift per Campaign", f"{kpis['avg_lift_per_campaign']:,.0f}")
    with col2:
        st.metric("Units Sold (Before)", f'{kpis["total_units_before"]:,}')
        st.metric("Units Sold (After)", f'{kpis["total_units_after"]:,}')
    with col3:
        st.metric("Incremental Units", f'{kpis["incremental_units"]:,}')
        st.metric("Incremental Revenue", f'₹ {kpis["incremental_revenue"] / 1e5:.2f} Lakh')

    st.markdown("---")
    st.markdown("These KPIs reflect the total impact of all promotional campaigns run across AtliQ Mart stores.")


# Store Performance (Tab 2)
with tabs[1]:
    st.header("🏬 Store Performance Analysis")

   
    st.subheader("⬆️ Top 10 Stores by Incremental Revenue")
    top_ir_df = get_top_10_stores_by_ir(conn)
    st.dataframe(top_ir_df, use_container_width=True)

    fig_top_ir = px.bar(
        top_ir_df.sort_values("incremental_revenue", ascending=False),
        x="incremental_revenue",
        y="store_id",
        color="city",
        orientation="h",
        text="incremental_revenue",
        labels={"incremental_revenue": "Incremental Revenue", "store_id": "Store ID"},
        title="Top 10 Stores by Incremental Revenue"
    )
    fig_top_ir.update_traces(textposition="outside")
    fig_top_ir.update_layout(yaxis=dict(categoryorder="total ascending"))
    st.plotly_chart(fig_top_ir, use_container_width=True)

    

    st.subheader("⬇️ Bottom 10 Stores by Incremental Units Sold")
    bottom_isu_df = get_bottom_10_stores_by_isu(conn)
    st.dataframe(bottom_isu_df, use_container_width=True)

    fig_bottom_isu = px.bar(
        bottom_isu_df.sort_values("incremental_sold_units", ascending=True),
        x="incremental_sold_units",
        y="store_id",
        color="city",
        orientation="h",
        text="incremental_sold_units",
        labels={"incremental_sold_units": "Incremental Sold Units", "store_id": "Store ID"},
        title="Bottom 10 Stores by Incremental Sold Units"
    )
    fig_bottom_isu.update_traces(textposition="outside")
    fig_bottom_isu.update_layout(yaxis=dict(categoryorder="total ascending"))
    st.plotly_chart(fig_bottom_isu, use_container_width=True)

    

    st.subheader("🏙️ Store Distribution by City")
    store_city_df = get_store_count_by_city(conn)
    st.dataframe(store_city_df, use_container_width=True)

    fig_store_count = px.bar(
        store_city_df.sort_values("store_count", ascending=False),
        x="city",
        y="store_count",
        color="city",
        text="store_count",
        labels={"store_count": "Number of Stores", "city": "City"},
        title="Store Count by City"
    )
    fig_store_count.update_traces(textposition="outside")
    st.plotly_chart(fig_store_count, use_container_width=True)



with tabs[2]:
    st.header("🎯 Promotion Type Analysis")
   
    st.subheader("⬆️ Top 2 Promotion Types by Incremental Revenue")
    top_promos_ir_df = get_top_2_promo_types_by_ir(conn)
    st.dataframe(top_promos_ir_df, use_container_width=True)

    fig_top_promo_ir = px.bar(
        top_promos_ir_df.sort_values("incremental_revenue", ascending=False),
        x="promo_type",
        y="incremental_revenue",
        color="promo_type",
        text="incremental_revenue",
        title="Top 2 Promotion Types by Incremental Revenue"
    )
    fig_top_promo_ir.update_traces(textposition="outside")
    fig_top_promo_ir.update_layout(height=500)
    st.plotly_chart(fig_top_promo_ir, use_container_width=True)

  

    st.subheader("⬇️ Bottom 2 Promotion Types by Incremental Sold Units")
    bottom_promos_isu_df = get_bottom_2_promo_types_by_isu(conn)
    st.dataframe(bottom_promos_isu_df, use_container_width=True)

    fig_bottom_promo_isu = px.bar(
        bottom_promos_isu_df.sort_values("incremental_sold_units", ascending=True),
        x="promo_type",
        y="incremental_sold_units",
        color="promo_type",
        text="incremental_sold_units",
        title="Bottom 2 Promotion Types by Incremental Units Sold"
    )
    fig_bottom_promo_isu.update_traces(textposition="outside")
    fig_bottom_promo_isu.update_layout(height=500)
    st.plotly_chart(fig_bottom_promo_isu, use_container_width=True)



    st.subheader("🔄 Discount vs BOGOF/Cashback Promotions")
    promo_comparison_df = get_discount_vs_bogof_cashback(conn)
    st.dataframe(promo_comparison_df, use_container_width=True)

    fig_compare = px.bar(
        promo_comparison_df.sort_values("incremental_revenue", ascending=False),
        x="promo_type_group",
        y="incremental_revenue",
        color="promo_type_group",
        text="incremental_revenue",
        title="Discount vs BOGOF/Cashback: Revenue Impact"
    )
    fig_compare.update_traces(textposition="outside")
    fig_compare.update_layout(height=500)
    st.plotly_chart(fig_compare, use_container_width=True)

 
    st.subheader("🛒 Top Products by Promotion Effectiveness")

    product_response_df = get_product_response_analysis(conn)

    if not product_response_df.empty:
        product_response_df = product_response_df.sort_values(by="total_lift", ascending=False)
        fig_product_response = px.bar(
            product_response_df,
            y="product_name",               
            x="total_lift",                 
            color="promo_type",
            text_auto=True,
            orientation="h",                
            title="Product Response to Different Promotion Types"
        )

        fig_product_response.update_layout(yaxis=dict(categoryorder='total ascending'))

        st.plotly_chart(fig_product_response, use_container_width=True)
    else:
        st.info("No product response data available.")



    st.subheader("⚖️ Balanced Promotions (Units & Revenue)")
    balanced_promos_df = get_balanced_promotions(conn)
    st.dataframe(balanced_promos_df, use_container_width=True)

    fig_balanced = px.scatter(
    balanced_promos_df,
    x="avg_units_lift",
    y="avg_revenue_lift",
    color="promo_type",
    size="avg_revenue_lift",
    hover_name="promo_type",
    title="Promotion Types Balancing Revenue and Units"
    )

    fig_balanced.update_layout(height=600)
    st.plotly_chart(fig_balanced, use_container_width=True)



with tabs[3]:
    st.header("📦 Product & Category Analysis")


    st.subheader("⬆️ Top 5 Categories by Sales Lift")
    top_categories_df = get_top_categories_by_lift(conn)
    st.dataframe(top_categories_df, use_container_width=True)

    fig_top_cat = px.bar(
        top_categories_df,
        y="category",
        x="total_units_lift",
        color="category",
        title="Top 5 Categories by Incremental Units Sold",
        text_auto=True,
        orientation="h",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig_top_cat.update_layout(yaxis_title=None, xaxis_title="Incremental Units Sold")
    st.plotly_chart(fig_top_cat, use_container_width=True)


    st.subheader("🏆 Top 10 Best Performing Products (by Revenue Lift)")
    best_products_df = get_best_performing_products(conn)
    st.dataframe(best_products_df, use_container_width=True)

    fig_best_products = px.bar(
        best_products_df,
        y="product_name",
        x="revenue_lift",
        color="product_name",
        title="Top 10 Products by Revenue Lift",
        text_auto=True,
        orientation="h",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_best_products.update_layout(yaxis_title=None, xaxis_title="Revenue Lift")
    st.plotly_chart(fig_best_products, use_container_width=True)


    st.subheader("❌ Worst Performing Products (Negative Lift)")
    worst_products_df = get_worst_performing_products(conn)
    st.dataframe(worst_products_df, use_container_width=True)

    fig_worst_products = px.bar(
        worst_products_df,
        y="product_name",
        x="revenue_lift",
        color="product_name",
        title="Bottom 10 Products by Revenue Lift",
        text_auto=True,
        orientation="h",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig_worst_products.update_layout(yaxis_title=None, xaxis_title="Revenue Lift")
    st.plotly_chart(fig_worst_products, use_container_width=True)

   

    st.subheader("🔄 Correlation Between Category & Promo Type Effectiveness")
    category_promo_corr_df = get_category_promo_correlation_data(conn)
    st.dataframe(category_promo_corr_df, use_container_width=True)

    fig_heatmap = px.density_heatmap(
        category_promo_corr_df,
        x="promo_type",
        y="category",
        z="avg_units_lift",
        color_continuous_scale="Viridis",
        title="Average Units Lift by Category and Promotion Type",
        text_auto=True
    )
    fig_heatmap.update_traces(
        hovertemplate="Promo Type: %{x}<br>Category: %{y}<br>Lift: %{z}<extra></extra>",
        showscale=True
    )
    fig_heatmap.update_layout(
        xaxis_title="Promotion Type",
        yaxis_title="Category",
        xaxis=dict(showgrid=True),
        yaxis=dict(showgrid=True)
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)
