import plotly.express as px


def top_items_chart(basket):

    top_items = basket.sum().sort_values(
        ascending=False
    ).head(10)

    fig = px.bar(
        x=top_items.index,
        y=top_items.values,
        color=top_items.values,
        color_continuous_scale="blues",
        labels={
            "x": "Items",
            "y": "Frequency"
        },
        title="Top Selling Items"
    )

    return fig


def support_confidence_chart(rules):

    # Create safe copy
    rules_plot = rules.copy()

    # Convert frozensets into strings
    rules_plot["antecedents"] = rules_plot[
        "antecedents"
    ].apply(
        lambda x: ", ".join(list(x))
    )

    rules_plot["consequents"] = rules_plot[
        "consequents"
    ].apply(
        lambda x: ", ".join(list(x))
    )

    # Create scatter plot
    fig = px.scatter(
        rules_plot,
        x="support",
        y="confidence",
        size="lift",
        color="lift",
        hover_name="antecedents",
        hover_data={
            "antecedents": True,
            "consequents": True,
            "support": True,
            "confidence": True,
            "lift": True
        },
        title="Support vs Confidence"
    )

    return fig