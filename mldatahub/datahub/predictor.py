from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler

from .serializers import serialize_records


def train_model(n_neighbors=3):
    records = serialize_records()

    if len(records) < 10:
        raise ValueError("Not enough records. Add more before forecast")

    X = [[rec['continuous_feature1'], rec['continuous_feature2']]
         for rec in records]
    y = [rec['categorical_feature1'] for rec in records]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = KNeighborsClassifier(n_neighbors=n_neighbors)
    model.fit(X_scaled, y)

    return model, scaler


def predict_category(float1, float2):
    model, scaler = train_model()

    X_input = [[float1, float2]]
    X_scaled = scaler.transform(X_input)

    prediction = model.predict(X_scaled)[0]
    return prediction
