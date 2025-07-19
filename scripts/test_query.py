import sqlite3
import os

from query_engine import (
    get_connection,
    get_top_10_stores_by_ir,
    get_bottom_10_stores_by_isu,
    get_store_count_by_city,
    get_top_2_promo_types_by_ir,
    get_bottom_2_promo_types_by_isu,
    get_discount_vs_cashback_effectiveness_v2,
    get_balanced_promotions,
    get_category_wise_sales_lift,
    get_product_response_analysis
)

def print_result(title, df):
    print("\n" + "="*40)
    print(f"{title}")
    print("="*40)
    print(df)



def main():
    conn = get_connection()

    print_result("1. Top 10 Stores by Incremental Revenue", get_top_10_stores_by_ir(conn))
    print_result("2. Bottom 10 Stores by Incremental Sold Units", get_bottom_10_stores_by_isu(conn))
    print_result("3. Store Count by City", get_store_count_by_city(conn))
    print_result("4. Top 2 Promotion Types by Incremental Revenue", get_top_2_promo_types_by_ir(conn))
    print_result("5. Bottom 2 Promotion Types by Incremental Sold Units", get_bottom_2_promo_types_by_isu(conn))
    print_result("6. Discount vs Cashback/BOGOF Effectiveness", get_discount_vs_cashback_effectiveness_v2(conn))
    print_result("7. Balanced Promotions (ISU & Margin)", get_balanced_promotions(conn))
    print_result("8. Product Category Sales Lift", get_category_wise_sales_lift(conn))
    print_result("9. Product Response (High/Low)", get_product_response_analysis(conn))

    conn.close()

if __name__ == "__main__":
    main()
