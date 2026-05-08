import pandas as pd


def get_product_recommendations(rules, selected_product, max_recommendations=6):

    recommendations = []

    for _, row in rules.iterrows():

        antecedents = sorted(list(row['antecedents']))
        consequents = sorted(list(row['consequents']))

        if selected_product in antecedents:
            for item in consequents:
                if item == selected_product:
                    continue
                recommendations.append({
                    "Product": item,
                    "Direction": "Also Bought",
                    "Reason": f"{', '.join(antecedents)} → {', '.join(consequents)}",
                    "Confidence": round(row['confidence'], 2),
                    "Lift": round(row['lift'], 2),
                    "Support": round(row['support'], 2),
                    "Score": round(row['confidence'] * row['lift'], 4)
                })

        if selected_product in consequents:
            for item in antecedents:
                if item == selected_product:
                    continue
                recommendations.append({
                    "Product": item,
                    "Direction": "Frequently Bought Before",
                    "Reason": f"{', '.join(antecedents)} → {', '.join(consequents)}",
                    "Confidence": round(row['confidence'], 2),
                    "Lift": round(row['lift'], 2),
                    "Support": round(row['support'], 2),
                    "Score": round(row['confidence'] * row['lift'], 4)
                })

    recommendation_df = pd.DataFrame(recommendations)

    if recommendation_df.empty:
        return recommendation_df

    recommendation_df = (
        recommendation_df
        .sort_values(
            by=["Score", "Lift", "Confidence"],
            ascending=False
        )
        .drop_duplicates(subset=["Product"])
        .reset_index(drop=True)
    )

    if max_recommendations is not None:
        recommendation_df = recommendation_df.head(max_recommendations)

    return recommendation_df
