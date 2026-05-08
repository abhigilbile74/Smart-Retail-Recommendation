import streamlit as st
import pandas as pd
import numpy as np

from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules

from sklearn.metrics.pairwise import cosine_similarity

import matplotlib.pyplot as plt
import seaborn as sns

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Grocery Analysis Dashboard",
    page_icon="🛒",
    layout="wide"
)

st.title("🛒 Grocery Association Rule & Similarity Analysis")

# ================= FILE UPLOAD =================
uploaded_file = st.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

# =========================================================
# MAIN
# =========================================================
if uploaded_file is not None:

    # ================= LOAD DATA =================
    try:
        df = pd.read_csv(uploaded_file)

    except Exception as e:
        st.error(f"Error reading file: {e}")
        st.stop()

    # ================= DATA PREVIEW =================
    st.subheader("📄 Dataset Preview")

    st.dataframe(
        df.head(),
        width="stretch"
    )

    col1, col2 = st.columns(2)

    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])

    # =========================================================
    # DATASET FORMAT
    # =========================================================
    st.sidebar.header("⚙️ Dataset Settings")

    dataset_type = st.sidebar.selectbox(
        "Dataset Format",
        [
            "Multiple Item Columns",
            "Transaction ID + Item"
        ]
    )

    transactions = []

    # =========================================================
    # FORMAT 1 -> MULTIPLE ITEM COLUMNS
    # =========================================================
    if dataset_type == "Multiple Item Columns":

        st.info(
            "Each row should contain multiple grocery items."
        )

        transactions = [
            [
                str(item).strip()
                for item in row.dropna().tolist()
                if str(item).strip() != ""
            ]
            for _, row in df.iterrows()
        ]

    # =========================================================
    # FORMAT 2 -> TRANSACTION ID + ITEM
    # =========================================================
    elif dataset_type == "Transaction ID + Item":

        transaction_col = st.sidebar.selectbox(
            "Select Transaction ID Column",
            df.columns
        )

        item_col = st.sidebar.selectbox(
            "Select Item Column",
            df.columns
        )

        grouped = df.groupby(transaction_col)[item_col].apply(list)

        transactions = grouped.tolist()

    # =========================================================
    # SHOW SAMPLE TRANSACTIONS
    # =========================================================
    st.subheader("🧺 Sample Transactions")

    st.write(transactions[:5])

    # =========================================================
    # TRANSACTION ENCODING
    # =========================================================
    try:

        te = TransactionEncoder()

        te_array = te.fit(transactions).transform(transactions)

        basket = pd.DataFrame(
            te_array,
            columns=te.columns_
        ).astype(bool)

    except Exception as e:
        st.error(f"Encoding Error: {e}")
        st.stop()

    # =========================================================
    # ENCODED BASKET
    # =========================================================
    st.subheader("✅ One-Hot Encoded Basket")

    st.dataframe(
        basket.head(),
        width="stretch"
    )

    # =========================================================
    # SIDEBAR SETTINGS
    # =========================================================
    st.sidebar.header("📊 Analysis Parameters")

    min_support = st.sidebar.slider(
        "Minimum Support",
        0.01,
        0.5,
        0.02
    )

    min_confidence = st.sidebar.slider(
        "Minimum Confidence",
        0.1,
        1.0,
        0.3
    )

    # =========================================================
    # APRIORI
    # =========================================================
    frequent_items = apriori(
        basket,
        min_support=min_support,
        use_colnames=True
    )

    st.subheader("📦 Frequent Itemsets")

    st.dataframe(
        frequent_items.head(20),
        width="stretch"
    )

    # =========================================================
    # ASSOCIATION RULES
    # =========================================================
    if len(frequent_items) > 0:

        rules = association_rules(
            frequent_items,
            metric="confidence",
            min_threshold=min_confidence
        )

        if not rules.empty:

            rules["antecedents"] = rules["antecedents"].apply(
                lambda x: ", ".join(list(x))
            )

            rules["consequents"] = rules["consequents"].apply(
                lambda x: ", ".join(list(x))
            )

            rules = rules.sort_values(
                by="lift",
                ascending=False
            )

            st.subheader("📊 Association Rules")

            st.dataframe(
                rules[
                    [
                        "antecedents",
                        "consequents",
                        "support",
                        "confidence",
                        "lift"
                    ]
                ],
                width="stretch"
            )

            # =========================================================
            # TOP ITEMS
            # =========================================================
            st.subheader("🔥 Top Selling Items")

            top_items = basket.sum().sort_values(
                ascending=False
            ).head(10)

            fig1, ax1 = plt.subplots(figsize=(10, 5))

            sns.barplot(
                x=top_items.index,
                y=top_items.values,
                hue=top_items.index,
                legend=False,
                palette="viridis",
                ax=ax1
            )

            ax1.set_xlabel("Items")
            ax1.set_ylabel("Count")

            plt.xticks(rotation=45)

            st.pyplot(fig1, width="stretch")

            # =========================================================
            # LIFT DISTRIBUTION
            # =========================================================
            st.subheader("📈 Lift Distribution")

            fig2, ax2 = plt.subplots(figsize=(8, 4))

            sns.histplot(
                rules["lift"],
                bins=20,
                kde=True,
                color="orange",
                ax=ax2
            )

            ax2.set_xlabel("Lift")
            ax2.set_ylabel("Frequency")

            st.pyplot(fig2, width="stretch")

            # =========================================================
            # ITEM SIMILARITY MATRIX
            # =========================================================
            st.subheader("🔍 Item Similarity Matrix")

            similarity = cosine_similarity(
                basket.T
            )

            similarity_df = pd.DataFrame(
                similarity,
                index=basket.columns,
                columns=basket.columns
            )

            st.dataframe(
                similarity_df.iloc[:20, :20],
                width="stretch"
            )

            # =========================================================
            # HEATMAP
            # =========================================================
            st.subheader("🌡️ Similarity Heatmap")

            fig3, ax3 = plt.subplots(figsize=(12, 8))

            sns.heatmap(
                similarity_df.iloc[:15, :15],
                cmap="coolwarm",
                annot=True,
                fmt=".2f",
                ax=ax3
            )

            st.pyplot(fig3, width="stretch")

            # =========================================================
            # SCATTER PLOT
            # =========================================================
            st.subheader("📉 Support vs Confidence")

            fig4, ax4 = plt.subplots(figsize=(8, 5))

            sns.scatterplot(
                data=rules,
                x="support",
                y="confidence",
                size="lift",
                hue="lift",
                palette="viridis",
                ax=ax4
            )

            st.pyplot(fig4, width="stretch")

        else:
            st.warning(
                "No association rules found. Lower support/confidence."
            )

    else:
        st.warning(
            "No frequent itemsets found. Try lower support."
        )

else:
    st.info("📂 Please upload a CSV dataset to begin analysis.")