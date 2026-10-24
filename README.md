# StyleSense AI — Fashion Recommendation System

## 1. Project Overview

StyleSense AI is a fashion recommendation web application that recommends clothing products based on user-selected preferences. It uses customer reviews, product categories, ratings, recommendation rates, sentiment information, and review confidence to rank suitable products.

**Project type:** Machine Learning / Recommendation System  
**Backend:** Python and Flask  
**Frontend:** HTML, CSS, JavaScript  
**Dataset:** Women's E-Commerce Clothing Reviews

## 2. Project Objectives

- Analyze and clean the clothing reviews dataset.
- Perform Exploratory Data Analysis (EDA).
- Engineer useful features from customer reviews.
- Develop a product-ranking and recommendation pipeline.
- Allow users to filter products by department, category, rating, and recommendation rate.
- Display ranked recommendations through a web interface.

## 3. Dataset

The project uses one primary raw CSV dataset:

`data/raw/Womens Clothing E-Commerce Reviews.csv`

The dataset contains customer review information, including clothing IDs, ratings, review text, recommendation indicators, and product categories.

The raw data is processed into cleaned, feature-engineered, machine-learning-ready, and product-level modeling files.

**Dataset limitation:** The local dataset does not currently contain the original product photographs. The website therefore uses decorative category-based visuals rather than verified product images.

## 4. Main Project Structure

- `data/raw/` — Original dataset
- `data/processed/` — Cleaned data, engineered features, model artifacts, and recommendation outputs
- `notebooks/` — EDA, modeling, evaluation, and test scripts
- `backend/app.py` — Flask application entry point
- `backend/recommendation_service.py` — Recommendation logic
- `backend/recommendation_routes.py` — Recommendation API
- `frontend/index.html` — Website structure
- `frontend/style.css` — Website styling
- `frontend/app.js` — Preference handling and API integration

## 5. Recommendation Workflow

1. The user selects department and product category.
2. The user sets minimum rating, recommendation rate, and review count.
3. The frontend sends the preferences to the Flask API.
4. The backend filters eligible products.
5. The recommendation service ranks matching products.
6. The frontend displays the highest-ranked results.

## 6. Technology Stack

- Python
- Pandas and NumPy
- Flask
- HTML
- CSS
- JavaScript
- Machine Learning and recommendation techniques
- Text analysis and feature engineering

## 7. How to Run the Application

### Requirements

Install Python and the project dependencies used by the application. Flask and Pandas are required by the current backend and recommendation service.

Open a terminal in the project root and install the required packages if they are not already installed:

```bash
python -m pip install -r requirements.txt
```

### Start the backend

In the terminal, run:

```bat
cd backend
python app.py
```

Keep the server running.

### Open the website

Open this address in Chrome:

`http://127.0.0.1:5000/`

Choose your preferences and click **Find my recommendations**.

## 8. API Endpoints

- `GET /` — Serves the homepage
- `GET /api/health` — Checks application health
- `GET /api/recommendations` — Returns ranked recommendations
- `GET /style.css` — Serves the stylesheet
- `GET /app.js` — Serves frontend JavaScript

Example request:

`http://127.0.0.1:5000/api/recommendations?department=Tops&class=Knits&minimum_rating=4&minimum_recommendation_rate=80&minimum_reviews=1&top_n=5`

## 9. Testing and Validation

The project has passed the following reported checks:

- API endpoint availability
- Invalid-input rejection
- Empty recommendation results
- Recommendation limits
- Required product fields
- Category and rating filters
- Descending recommendation-score order
- Frontend structure and API integration
- Department-dependent category dropdown
- Mobile-sized browser layout
- Final required-file integrity audit

The final integrity audit found all 18 checked files present. The product modeling dataset contains 1,206 unique Clothing IDs and 14 columns.

## 10. Known Limitations

- Original product photographs are not available in the local dataset.
- The system uses review-derived information rather than live shopping inventory.
- Price, size, color, season, and occasion are not currently verified product attributes in the recommendation interface.
- The recommendation scores are model-generated ranking values, not guaranteed probabilities of user satisfaction.
- The Flask development server is intended for local development, not production deployment.

## 11. Future Enhancements

- Add verified product photographs when a reliable matching image source becomes available.
- Improve recommendation evaluation using suitable offline metrics and held-out data.
- Add user accounts and saved preferences.
- Improve recommendation explanations and accessibility.
- Deploy the application with a production-ready server after appropriate security testing.

## 12. Conclusion

StyleSense AI demonstrates an end-to-end fashion recommendation workflow using one primary customer-review dataset, from data preparation and feature engineering to recommendation ranking and a Flask-based web interface.

The application has passed the documented endpoint, recommendation, frontend, and file-integrity checks. Further evaluation and deployment preparation can be performed as separate stages.
