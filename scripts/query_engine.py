import sqlite3
import pandas as pd
import os


DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'retail_events_db.sqlite')

def get_connection():
    return sqlite3.connect(DB_PATH)


def get_top_10_stores_by_ir(conn):
    query = """
        SELECT 
            s.store_id,
            s.city,
            SUM(("quantity_sold(after_promo)" - "quantity_sold(before_promo)")  * e.base_price) AS incremental_revenue
        FROM fact_events e
        JOIN dim_stores s ON e.store_id = s.store_id
        GROUP BY s.store_id, s.city
        ORDER BY incremental_revenue DESC
        LIMIT 10;
    """
    return pd.read_sql(query, conn)


def get_bottom_10_stores_by_isu(conn):
    query = """
        SELECT 
            s.store_id,
            s.city,
            SUM("quantity_sold(after_promo)" - "quantity_sold(before_promo)") AS incremental_sold_units
        FROM fact_events e
        JOIN dim_stores s ON e.store_id = s.store_id
        GROUP BY s.store_id, s.city
        ORDER BY incremental_sold_units ASC
        LIMIT 10;
    """
    return pd.read_sql(query, conn)


def get_store_count_by_city(conn):
    query = """
        SELECT 
            city,
            COUNT(store_id) AS store_count
        FROM dim_stores
        GROUP BY city
        ORDER BY store_count DESC;
    """
    return pd.read_sql(query, conn)


def get_top_2_promo_types_by_ir(conn):
    query = """
        SELECT 
            promo_type,
            SUM(("quantity_sold(after_promo)" - "quantity_sold(before_promo)") * base_price) AS incremental_revenue
        FROM fact_events
        GROUP BY promo_type
        ORDER BY incremental_revenue DESC
        LIMIT 2;
    """
    return pd.read_sql(query, conn)


def get_bottom_2_promo_types_by_isu(conn):
    query = """
        SELECT 
            promo_type,
            SUM("quantity_sold(after_promo)" - "quantity_sold(before_promo)") AS incremental_sold_units
        FROM fact_events
        GROUP BY promo_type
        ORDER BY incremental_sold_units ASC
        LIMIT 2;
    """
    return pd.read_sql(query, conn)




def get_sales_lift_by_category(conn):
    query = """
        SELECT 
            p.category,
            SUM(("quantity_sold(after_promo)" - "quantity_sold(before_promo)") AS total_sold_lift
        FROM fact_events e
        JOIN dim_products p ON e.product_code = p.product_code
        GROUP BY p.category
        ORDER BY total_sold_lift DESC;
    """
    return pd.read_sql(query, conn)


def get_top_10_products_by_lift(conn):
    query = """
        SELECT 
            p.product_name,
            SUM(("quantity_sold(after_promo)" - "quantity_sold(before_promo)") AS sold_lift
        FROM fact_events e
        JOIN dim_products p ON e.product_code = p.product_code
        GROUP BY p.product_name
        ORDER BY sold_lift DESC
        LIMIT 10;
    """
    return pd.read_sql(query, conn)


def get_bottom_10_products_by_lift(conn):
    query = """
        SELECT 
            p.product_name,
            SUM(("quantity_sold(after_promo)" - "quantity_sold(before_promo)") AS sold_lift
        FROM fact_events e
        JOIN dim_products p ON e.product_code = p.product_code
        GROUP BY p.product_name
        ORDER BY sold_lift ASC
        LIMIT 10;
    """
    return pd.read_sql(query, conn)


def get_category_promo_effectiveness(conn):
    query = """
        SELECT 
            p.category,
            e.promo_type,
            SUM(("quantity_sold(after_promo)" - "quantity_sold(before_promo)") AS sold_lift
        FROM fact_events e
        JOIN dim_products p ON e.product_code = p.product_code
        GROUP BY p.category, e.promo_type
        ORDER BY p.category, sold_lift DESC;
    """
    return pd.read_sql(query, conn)



def get_balanced_promotions(conn):
    query = """
    SELECT
        promo_type,
        AVG("quantity_sold(after_promo)" - "quantity_sold(before_promo)") AS avg_units_lift,
        AVG(("quantity_sold(after_promo)" - "quantity_sold(before_promo)") * base_price) AS avg_revenue_lift
    FROM fact_events
    GROUP BY promo_type
    HAVING avg_units_lift > 0 AND avg_revenue_lift > 0
    ORDER BY avg_units_lift DESC, avg_revenue_lift DESC;
    """

    return pd.read_sql(query, conn)


def get_category_wise_sales_lift(conn):
    query = """
        SELECT 
            p.category,
            SUM("quantity_sold(after_promo)" - "quantity_sold(before_promo)") AS sales_lift
        FROM fact_events e
        JOIN dim_products p ON e.product_code = p.product_code
        GROUP BY p.category
        ORDER BY sales_lift DESC;
    """
    return pd.read_sql(query, conn)


def get_product_response_analysis(conn):
    query = """
        SELECT 
            p.product_name,
            p.category,
            e.promo_type,
            SUM("quantity_sold(after_promo)" - "quantity_sold(before_promo)") AS total_lift
        FROM fact_events e
        JOIN dim_products p ON e.product_code = p.product_code
        GROUP BY p.product_name, p.category, e.promo_type
        ORDER BY total_lift DESC;
    """
    return pd.read_sql(query, conn)


import pandas as pd

def get_overall_kpis(conn):
    query = """
        WITH campaign_summary AS (
            SELECT 
                c.campaign_id,
                SUM(e."quantity_sold(before_promo)") AS units_before,
                SUM(e."quantity_sold(after_promo)") AS units_after,
                SUM(
                    (e."quantity_sold(after_promo)" - e."quantity_sold(before_promo)") * e.base_price
                ) AS incremental_revenue
            FROM fact_events e
            JOIN dim_campaigns c ON e.campaign_id = c.campaign_id
            GROUP BY c.campaign_id
        )
        SELECT
            COUNT(*) AS total_campaigns,
            SUM(units_before) AS total_units_before,
            SUM(units_after) AS total_units_after,
            SUM(units_after - units_before) AS incremental_units,
            SUM(incremental_revenue) AS incremental_revenue,
            AVG(units_after - units_before) AS avg_lift_per_campaign
        FROM campaign_summary;
    """
    df = pd.read_sql(query, conn)
    return df.iloc[0].to_dict()

def get_discount_vs_bogof_cashback(conn):
    query = """
        SELECT 
            CASE
                WHEN LOWER(promo_type) LIKE 'discount%' THEN 'Discount'
                WHEN LOWER(promo_type) = 'bogof' THEN 'BOGOF'
                WHEN LOWER(promo_type) = 'cashback' THEN 'Cashback'
                ELSE 'Other'
            END AS promo_type_group,
            SUM(("quantity_sold(after_promo)" - "quantity_sold(before_promo)") * base_price) AS incremental_revenue
        FROM fact_events
        GROUP BY promo_type_group
        ORDER BY incremental_revenue DESC;
    """
    return pd.read_sql(query, conn)

def get_top_categories_by_lift(conn):
    query = """
        SELECT 
            dp.category,
            ROUND(SUM("quantity_sold(after_promo)" - "quantity_sold(before_promo)"), 2) AS total_units_lift,
            ROUND(SUM(("quantity_sold(after_promo)" - "quantity_sold(before_promo)") * fe.base_price), 2) AS total_revenue_lift
        FROM fact_events fe
        JOIN dim_products dp ON fe.product_code = dp.product_code
        GROUP BY dp.category
        ORDER BY total_units_lift DESC
        LIMIT 5;
    """
    return pd.read_sql_query(query, conn)


def get_best_performing_products(conn):
    query = """
        SELECT 
            dp.product_name,
            ROUND(SUM("quantity_sold(after_promo)" - "quantity_sold(before_promo)"), 2) AS units_lift,
            ROUND(SUM(("quantity_sold(after_promo)" - "quantity_sold(before_promo)") * fe.base_price), 2) AS revenue_lift
        FROM fact_events fe
        JOIN dim_products dp ON fe.product_code = dp.product_code
        GROUP BY dp.product_name
        HAVING units_lift > 0 AND revenue_lift > 0
        ORDER BY revenue_lift DESC
        LIMIT 10;
    """
    return pd.read_sql_query(query, conn)

def get_worst_performing_products(conn):
    query = """
        SELECT 
            dp.product_name,
            ROUND(SUM("quantity_sold(after_promo)" - "quantity_sold(before_promo)"), 2) AS units_lift,
            ROUND(SUM(("quantity_sold(after_promo)" - "quantity_sold(before_promo)") * fe.base_price), 2) AS revenue_lift
        FROM fact_events fe
        JOIN dim_products dp ON fe.product_code = dp.product_code
        GROUP BY dp.product_name
        HAVING units_lift < 0 OR revenue_lift < 0
        ORDER BY revenue_lift ASC
        LIMIT 10;
    """
    return pd.read_sql_query(query, conn)

def get_category_promo_correlation_data(conn):
    query = """
        SELECT 
            dp.category,
            fe.promo_type,
            ROUND(AVG("quantity_sold(after_promo)" - "quantity_sold(before_promo)"), 2) AS avg_units_lift,
            ROUND(AVG(("quantity_sold(after_promo)" - "quantity_sold(before_promo)") * fe.base_price), 2) AS avg_revenue_lift
        FROM fact_events fe
        JOIN dim_products dp ON fe.product_code = dp.product_code
        GROUP BY dp.category, fe.promo_type;
    """
    return pd.read_sql_query(query, conn)

