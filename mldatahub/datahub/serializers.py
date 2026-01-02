from .services import list_records


def record_to_dict(record):
    return {
        "id": record.id,
        "continuous_feature1": record.continuous_feature1,
        "continuous_feature2": record.continuous_feature2,
        "categorical_feature1": record.categorical_feature1,
    }


def serialize_records():
    records = list_records()
    return [record_to_dict(rec) for rec in records]


def parse_predict_input(data):
    float1 = float(data['continuous_feature1'])
    float2 = float(data['continuous_feature2'])
    return float1, float2
