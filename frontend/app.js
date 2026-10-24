
"use strict";

const API_URL = "/api/recommendations";

const departmentSelect = document.getElementById("department");
const classSelect = document.getElementById("product-class");
const preferenceForm = document.getElementById("preference-form");
const productGrid = document.getElementById("product-grid");
const messageBox = document.getElementById("message");
const resultSummary = document.getElementById("result-summary");

const classesByDepartment = {
    Tops: ["Blouses", "Fine gauge", "Knits", "Layering", "Sweaters"],
    Dresses: ["Dresses"],
    Bottoms: ["Casual bottoms", "Jeans", "Pants", "Shorts", "Skirts"],
    Jackets: ["Jackets", "Outerwear"],
    Intimate: [
        "Chemises", "Intimates", "Layering", "Legwear",
        "Lounge", "Sleep", "Swim"
    ],
    Trend: ["Trend"]
};

function showMessage(text, type = "") {
    messageBox.textContent = text;
    messageBox.className = "message";

    if (type) {
        messageBox.classList.add(type);
    }
}

function updateClassOptions() {
    const department = departmentSelect.value;
    const previousValue = classSelect.value;

    classSelect.replaceChildren();

    const allOption = document.createElement("option");
    allOption.value = "";
    allOption.textContent = "All categories";
    classSelect.appendChild(allOption);

    let classes = [];

    if (department) {
        classes = classesByDepartment[department] || [];
    } else {
        classes = [
            ...new Set(Object.values(classesByDepartment).flat())
        ].sort((a, b) => a.localeCompare(b));
    }

    classes.forEach((item) => {
        const option = document.createElement("option");
        option.value = item;
        option.textContent = item;
        classSelect.appendChild(option);
    });

    if (classes.includes(previousValue)) {
        classSelect.value = previousValue;
    }
}

function createProductCard(product) {
    const card = document.createElement("article");
    card.className = "product-card";

    
const visual = document.createElement("div");
visual.className = "product-visual";

const visualLabel = document.createElement("span");
visualLabel.className = "visual-label";
visualLabel.textContent = product.Class_Name || "Fashion";

const visualIcon = document.createElement("span");
visualIcon.className = "visual-icon";
visualIcon.setAttribute("aria-hidden", "true");

const categoryName = String(product.Class_Name || "").toLowerCase();

if (categoryName.includes("dress")) {
    visualIcon.textContent = "♧";
} else if (categoryName.includes("knit") || categoryName.includes("sweater")) {
    visualIcon.textContent = "◇";
} else if (categoryName.includes("jacket") || categoryName.includes("outerwear")) {
    visualIcon.textContent = "✧";
} else if (categoryName.includes("skirt") || categoryName.includes("bottom")) {
    visualIcon.textContent = "⌁";
} else {
    visualIcon.textContent = "✳";
}

visual.append(visualIcon, visualLabel);


    const details = document.createElement("div");
    details.className = "product-details";

    const category = document.createElement("div");
    category.className = "product-category";
    category.textContent =
        `${product.Department_Name} / ${product.Class_Name}`;

    const title = document.createElement("h3");
    title.textContent = `Fashion Item #${product["Clothing ID"]}`;

    const meta = document.createElement("div");
    meta.className = "product-meta";

    const rating = document.createElement("span");
    rating.textContent =
        `★ ${Number(product.Average_Rating).toFixed(2)} / 5`;

    const reviews = document.createElement("span");
    reviews.textContent =
        `${product.Review_Count} review(s)`;

    const score = document.createElement("div");
    score.className = "product-score";

    const recommendationRate = document.createElement("span");
    recommendationRate.textContent =
        `${Number(product.Recommendation_Rate).toFixed(2)}% recommend`;

    const finalScore = document.createElement("div");
    finalScore.textContent =
        `Recommendation score: ${
            Number(product.Final_Robust_Score).toFixed(4)
        }`;

    meta.append(rating, reviews);
    score.append(recommendationRate, finalScore);
    details.append(category, title, meta, score);
    card.append(visual, details);

    return card;
}

async function loadRecommendations(event) {
    if (event) {
        event.preventDefault();
    }

    productGrid.replaceChildren();
    resultSummary.textContent = "Finding matching products...";
    showMessage("Connecting to the StyleSense AI recommendation engine...");

    const formData = new FormData(preferenceForm);
    const params = new URLSearchParams();

    for (const [key, value] of formData.entries()) {
        if (value !== "") {
            params.set(key, value);
        }
    }

    params.set("top_n", "5");

    try {
        const response = await fetch(`${API_URL}?${params.toString()}`);
        const data = await response.json();

        if (!response.ok || data.status !== "ok") {
            throw new Error(data.message || "Could not load recommendations.");
        }

        if (!data.recommendations || data.recommendations.length === 0) {
            resultSummary.textContent = "No matching products found.";
            showMessage(
                "No products match all these filters. Try a lower minimum rating, recommendation rate, or review count.",
                "error"
            );
            return;
        }

        data.recommendations.forEach((product) => {
            productGrid.appendChild(createProductCard(product));
        });

        resultSummary.textContent =
            `${data.count} product(s) match your selected preferences.`;

        showMessage(
            "Recommendations loaded successfully.",
            "success"
        );
    } catch (error) {
        resultSummary.textContent = "Recommendations are unavailable.";
        showMessage(
            `${error.message} Make sure the StyleSense AI Flask server is running.`,
            "error"
        );
    }
}

departmentSelect.addEventListener("change", updateClassOptions);
preferenceForm.addEventListener("submit", loadRecommendations);

updateClassOptions();
