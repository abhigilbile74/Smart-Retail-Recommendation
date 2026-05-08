import streamlit as st
import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from src.preprocess import (
    load_data,
    create_transactions,
    encode_transactions
)

from src.apriori_model import (
    generate_frequent_itemsets,
    generate_rules
)

from src.recommend import (
    get_product_recommendations
)

from src.visualize import (
    top_items_chart,
    support_confidence_chart
)


def get_fallback_products(basket, selected_product, n=6):

    top_items = (
        basket.sum()
        .sort_values(ascending=False)
        .drop(labels=[selected_product], errors='ignore')
        .head(n)
    )

    return [
        {
            "Product": item,
            "Reason": "Top selling product",
            "Support": round(float(top_items[item]), 2)
        }
        for item in top_items.index
    ]


# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Smart Basket Recommendation",
    page_icon="🛒",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>

.main {
    background-color: #f5f7fa;
}

.block-container {
    padding-top: 2rem;
}

.recommend-card {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 15px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
}

.big-font {
    font-size: 22px;
    font-weight: bold;
    color: #1f77b4;
}

.metric-text {
    font-size: 16px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------

st.sidebar.header("⚙️ Model Settings")

support = st.sidebar.slider(
    "Minimum Support",
    0.01,
    0.5,
    0.02
)

confidence = st.sidebar.slider(
    "Minimum Confidence",
    0.1,
    1.0,
    0.3
)

max_recommendations = st.sidebar.slider(
    "Max Recommendations",
    1,
    12,
    6
)

# ---------------- LOAD DATA ----------------

# Construct data path relative to this script
APP_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(APP_DIR)
DATA_PATH = os.path.join(PROJECT_ROOT, "data", "grocerie.csv")

# Load and process data with error handling
try:
    df = load_data(DATA_PATH)
    transactions = create_transactions(df)
    basket = encode_transactions(transactions)
except FileNotFoundError:
    st.error(f"❌ Data file not found at: {DATA_PATH}")
    st.info("Please ensure 'data/grocerie.csv' exists in the project directory.")
    st.stop()
except Exception as e:
    st.error(f"❌ Error loading data: {str(e)}")
    st.stop()

# ---------------- MODEL ----------------

try:
    frequent_items = generate_frequent_itemsets(
        basket,
        support
    )

    rules = generate_rules(
        frequent_items,
        confidence
    )
except Exception as e:
    st.error(f"❌ Error generating model: {str(e)}")
    st.info("Try adjusting the support and confidence thresholds.")
    st.stop()

# ---------------- KPI ----------------

col1, col2, col3 = st.columns(3)

col1.metric(
    "Transactions",
    len(df)
)

col2.metric(
    "Frequent Itemsets",
    len(frequent_items)
)

col3.metric(
    "Rules Generated",
    len(rules)
)

st.divider()

# ---------------- PRODUCT SELECTOR ----------------

st.subheader("🔍 Product Recommendation Engine")

selected_product = st.selectbox(
    "Choose a Product",
    sorted(basket.columns)
)

# ---------------- RECOMMENDATIONS ----------------

recommendation_df = get_product_recommendations(
    rules,
    selected_product,
    max_recommendations=max_recommendations
)

if not recommendation_df.empty:

    st.success(
        f"Recommendations based on '{selected_product}'"
    )

    cols = st.columns(3)

    for idx, row in recommendation_df.iterrows():

        with cols[idx % 3]:

            st.markdown(f"""
            <div class="recommend-card">

            <div class="big-font">
            {row['Product']}
            </div>

            <br>

            <div class="metric-text">
            🔁 Type:
            <b>{row['Direction']}</b>
            </div>

            <div class="metric-text">
            📌 Rule:
            <b>{row['Reason']}</b>
            </div>

            <div class="metric-text">
            📈 Confidence:
            <b>{row['Confidence']}</b>
            </div>

            <div class="metric-text">
            🚀 Lift:
            <b>{row['Lift']}</b>
            </div>

            <div class="metric-text">
            📊 Support:
            <b>{row['Support']}</b>
            </div>

            <div class="metric-text">
            ⭐ Score:
            <b>{row['Score']}</b>
            </div>

            </div>
            """, unsafe_allow_html=True)

else:

    st.warning(
        "No recommendations found for this product. Try lowering support/confidence or choose another product."
    )

    fallback_items = get_fallback_products(basket, selected_product, n=max_recommendations)

    if fallback_items:
        st.info("Here are some popular alternatives you can consider:")
        cols = st.columns(3)

        for idx, fallback in enumerate(fallback_items):
            with cols[idx % 3]:
                st.markdown(f"""
                <div class="recommend-card">

                <div class="big-font">
                {fallback['Product']}
                </div>

                <br>

                <div class="metric-text">
                📌 Reason:
                <b>{fallback['Reason']}</b>
                </div>

                <div class="metric-text">
                📊 Popularity:
                <b>{fallback['Support']}</b>
                </div>

                </div>
                """, unsafe_allow_html=True)

st.divider()

# ---------------- VISUALIZATION ----------------

st.subheader("📊 Top Selling Products")

try:
    fig1 = top_items_chart(basket)
    st.plotly_chart(fig1, width='stretch')
except Exception as e:
    st.error(f"Error generating chart: {str(e)}")

# ---------------- SCATTER ----------------

st.subheader("📈 Association Rule Insights")

try:
    if not rules.empty:
        fig2 = support_confidence_chart(rules)
        st.plotly_chart(fig2, width='stretch')
    else:
        st.info("No rules generated with current parameters. Try lowering thresholds.")
except Exception as e:
    st.error(f"Error generating insights: {str(e)}")

# ---------------- RULES TABLE ----------------

st.subheader("📄 Association Rules")

display_rules = rules[
    [
        'antecedents',
        'consequents',
        'support',
        'confidence',
        'lift'
    ]
].copy()

display_rules['antecedents'] = (
    display_rules['antecedents']
    .apply(lambda x: ', '.join(list(x)))
)

display_rules['consequents'] = (
    display_rules['consequents']
    .apply(lambda x: ', '.join(list(x)))
)

st.dataframe(
    display_rules,
    width="stretch"
)

# ---------------- DOWNLOAD ----------------

csv = display_rules.to_csv(
    index=False
)

st.download_button(
    label="⬇ Download Association Rules",
    data=csv,
    file_name="association_rules.csv",
    mime="text/csv"
)