from mlxtend.frequent_patterns import (
    apriori,
    association_rules
)


def generate_frequent_itemsets(
        basket,
        min_support=0.02):

    frequent_items = apriori(
        basket,
        min_support=min_support,
        use_colnames=True
    )

    return frequent_items


def generate_rules(
        frequent_items,
        min_confidence=0.3):

    rules = association_rules(
        frequent_items,
        metric="confidence",
        min_threshold=min_confidence
    )

    return rules.sort_values(
        by="lift",
        ascending=False
    )