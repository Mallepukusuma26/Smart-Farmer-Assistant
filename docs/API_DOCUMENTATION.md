# Smart Farmer Assistant — API Documentation

## REST API Endpoints

The application provides local REST JSON endpoints for interactive frontend AJAX widgets and external integrations.

### 1. Calculate Real-Time Soil Score
- **Endpoint**: `POST /api/soil-score`
- **Request Body**:
  ```json
  {
    "ph": 6.5,
    "nitrogen": 140,
    "phosphorus": 50,
    "potassium": 200,
    "organic_carbon": 0.75,
    "electrical_conductivity": 0.5
  }
  ```
- **Response**:
  ```json
  {
    "health_score": 88.5
  }
  ```

### 2. Crop Recommendation API
- **Endpoint**: `POST /api/crop-recommend`
- **Request Body**:
  ```json
  {
    "n": 90,
    "p": 40,
    "k": 40,
    "temperature": 25,
    "humidity": 75,
    "ph": 6.5,
    "rainfall": 150
  }
  ```
- **Response**: Returns top 3 crop recommendations with suitability scores.

### 3. Financial Summary API
- **Endpoint**: `GET /api/financial-summary`
- **Requires Authentication**: Yes (`FARMER` role)
- **Response**: Returns total revenue, expenses, net profit, and category breakdown dictionary.
