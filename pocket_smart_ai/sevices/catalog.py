from urllib.parse import quote


def search_url(
    platform: str,
    query: str
) -> str:

    encoded = quote(query)

    templates = {

        "Amazon":
            f"https://www.amazon.in/s?k={encoded}",

        "Flipkart":
            f"https://www.flipkart.com/search?q={encoded}",

        "IKEA":
            f"https://www.ikea.com/in/en/search/?q={encoded}",

        "Swiggy":
            f"https://www.swiggy.com/search?query={encoded}",

        "Zomato":
            f"https://www.zomato.com/search?query={encoded}",

        "OYO":
            f"https://www.oyorooms.com/search?location={encoded}",
    }

    return templates.get(
        platform,
        f"https://www.google.com/search?q={encoded}"
    )


HOME_CATALOG = [

    (
        "LED Ceiling Light",
        "Lighting",
        "Amazon",
        1299
    ),

    (
        "Modern Ceiling Fan",
        "Electrical",
        "Amazon",
        2499
    ),

    (
        "Minimal Wall Art Set",
        "Decor",
        "IKEA",
        1499
    ),

    (
        "Compact Side Table",
        "Furniture",
        "IKEA",
        2999
    ),

    (
        "Dining Chair",
        "Furniture",
        "IKEA",
        3499
    ),

    (
        "Storage Cabinet",
        "Storage",
        "Flipkart",
        4999
    ),

    (
        "Area Rug",
        "Decor",
        "Amazon",
        1999
    ),

    (
        "Table Lamp",
        "Lighting",
        "IKEA",
        999
    )
]


PARTY_CATALOG = [

    (
        "Party catering package",
        "Food",
        "Swiggy",
        450
    ),

    (
        "Family restaurant booking idea",
        "Food",
        "Zomato",
        600
    ),

    (
        "Balloon and backdrop set",
        "Decoration",
        "Amazon",
        1800
    ),

    (
        "Disposable dinnerware set",
        "Supplies",
        "Amazon",
        900
    ),

    (
        "LED party lights",
        "Decoration",
        "Flipkart",
        1200
    ),

    (
        "Guest accommodation search",
        "Stay",
        "OYO",
        2200
    )
]


JEWELRY_CATALOG = [

    (
        "Pearl drop earrings",
        "Earrings",
        "Amazon",
        899
    ),

    (
        "Minimal gold-tone necklace",
        "Necklace",
        "Flipkart",
        1299
    ),

    (
        "Kundan-style choker",
        "Necklace",
        "Amazon",
        2499
    ),

    (
        "Stone-stud earrings",
        "Earrings",
        "Flipkart",
        999
    ),

    (
        "Delicate bracelet",
        "Bracelet",
        "Amazon",
        799
    ),

    (
        "Statement jhumka",
        "Earrings",
        "Flipkart",
        1499
    )
]


def fallback_recommendations(
    planner: str,
    budget: float,
    preferences: dict
) -> dict:

    catalogs = {
        "home": HOME_CATALOG,
        "party": PARTY_CATALOG,
        "jewelry": JEWELRY_CATALOG
    }

    rows = catalogs[planner]

    chosen = []

    running = 0.0

    for (
        name,
        category,
        platform,
        price
    ) in rows:

        if (
            running + price
            <= budget * 0.95
            or not chosen
        ):

            chosen.append({

                "name": name,

                "category": category,

                "platform": platform,

                "estimated_price": price,

                "reason": (
                    "Budget-friendly fallback "
                    "option based on the "
                    "selected planner."
                ),

                "search_url": search_url(
                    platform,
                    name
                ),

                "priority":
                    "high"
                    if len(chosen) < 2
                    else "medium"
            })

            running += price

        if len(chosen) >= 6:
            break

    if planner == "home":

        plan = [

            {
                "category": "Furniture",
                "percentage": 35,
                "amount": round(
                    budget * 0.35,
                    2
                )
            },

            {
                "category": "Lighting",
                "percentage": 20,
                "amount": round(
                    budget * 0.20,
                    2
                )
            },

            {
                "category": "Decor",
                "percentage": 25,
                "amount": round(
                    budget * 0.25,
                    2
                )
            },

            {
                "category": "Storage",
                "percentage": 20,
                "amount": round(
                    budget * 0.20,
                    2
                )
            }
        ]

    elif planner == "party":

        plan = [

            {
                "category": "Food",
                "percentage": 45,
                "amount": round(
                    budget * 0.45,
                    2
                )
            },

            {
                "category": "Decoration",
                "percentage": 20,
                "amount": round(
                    budget * 0.20,
                    2
                )
            },

            {
                "category": "Entertainment",
                "percentage": 20,
                "amount": round(
                    budget * 0.20,
                    2
                )
            },

            {
                "category": "Contingency",
                "percentage": 15,
                "amount": round(
                    budget * 0.15,
                    2
                )
            }
        ]

    else:

        plan = [

            {
                "category": "Necklace",
                "percentage": 40,
                "amount": round(
                    budget * 0.40,
                    2
                )
            },

            {
                "category": "Earrings",
                "percentage": 35,
                "amount": round(
                    budget * 0.35,
                    2
                )
            },

            {
                "category": "Bracelet",
                "percentage": 15,
                "amount": round(
                    budget * 0.15,
                    2
                )
            },

            {
                "category": "Contingency",
                "percentage": 10,
                "amount": round(
                    budget * 0.10,
                    2
                )
            }
        ]

    return {

        "planner": planner,

        "budget": budget,

        "budget_plan": plan,

        "summary": (
            "Fallback recommendations are "
            "shown because the AI service is "
            "unavailable or returned unusable data."
        ),

        "recommendations": chosen,

        "tips": [

            "Compare the final seller price, "
            "delivery fee, and return policy "
            "before buying.",

            "Treat displayed prices as estimates "
            "and verify them on the linked platform.",

            "Keep a small contingency amount "
            "instead of spending the entire budget."
        ],

        "source": "fallback",

        "image_insight": None
    }