# Assignment: Machine Learning Data Web Application

## Overview
The task in this assignment is to **develop a web application** storing data that can be used for a machine learning model.

Data stored by the web application are a collection of data points that involve:
* **Two or more continuous features**
* **A single categorical feature**

The exact names and the nature of these features do not matter and can be chosen arbitrarily. The data are supposed to be used for a **classification task** performed by a machine learning model that uses the continuous features to predict the corresponding category. The web application stores the data in a **relational database** consisting of a single table that holds individual data points as records.

### Versions of the Application
* **Basic version:** Data points can be retrieved from, added to, and deleted from the database.
* **Extended version:** It is also possible to make predictions of the most likely category based on submitted values of the continuous features using a machine learning model.

The web application consists of two parts: a **website** and an **API**. The website involves HTML pages to be rendered in a browser, whereas the API involves data transfer directly over HTTP.

---

## Requirements for the maximum grade of 4

Using a **web framework** (such as Flask, Django, FastAPI, etc.) and a **database management system** (such as SQLite, PostgreSQL, MySQL, MariaDB, etc.), implement the website part of the basic version of the web application.

### Database Specification
The database should consist of a **single table** with the following columns:
* **Primary key:** represented as integers.
* **Continuous features:** two or more columns (one per feature, represented as floating-point numbers).
* **Categorical feature:** one column (represented as integers).

### Website Paths
* `/` – **Home page**: displays all data points in a table. The table should include sequence numbers, columns for each continuous feature, and a column for the categorical feature. It should also allow the user to invoke deletion of a record via the `/delete/<record_id>` path.
* `/add` – **Add data**: contains an HTML form for a new data point.
    * Submitted via **HTTP POST**.
    * Validation: If successful, add record and redirect to home. If failed, return **400 HTTP status** and an error page.
* `/delete/<record_id>` – **Delete data**:
    * Accepts only **HTTP POST** requests.
    * Validation: Check if record exists. If successful, delete and redirect to home. If failed, return **404 HTTP status** and an error page.

### API Endpoints
* `GET /api/data` – Returns all data points as a **JSON list of dictionaries**.
* `POST /api/data` – Adds a new data point via **JSON**. Returns the primary key of the new record or a **400 error** with a message.
* `DELETE /api/data/<record_id>` – Deletes a data point. Returns the primary key of the deleted record or a **404 error**.

> **Note:** Use **Object-Relational Mapping (ORM)** (e.g., SQLAlchemy, Peewee) for both website and API parts.

---

## Requirements for the maximum grade of 5

All requirements for the grade of 4 must be satisfied.

### Extended Website Part
* `/predict` – Predicts a category based on features.
    * Contains an HTML form for continuous features.
    * Submitted via **HTTP POST**.
    * Success: Feed values to the ML model and display the predicted category.
    * Failure: Return **400 HTTP status** and an error page.

### Machine Learning Model
* **Classifier:** k-nearest neighbors (k-NN).
* **Parameter:** $k$ parameter should not be larger than 5 ($k \le 5$).
* **Training:** Trained on all data points currently in the database.
* **Preprocessing:** Each continuous feature must be **standardized** before training and before prediction.
* **Package:** Use `scikit-learn`.

### Extended API Part
* `GET /api/predictions` – Predicts a category.
    * Values are passed via **query parameters**.
    * Success: Returns **JSON** with the predicted category.
    * Failure: Return **400 HTTP status** and a JSON error message.

---
*It is recommended to use the **Requests** package for testing the API.*