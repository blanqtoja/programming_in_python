import json
from django.http import Http404
from django.shortcuts import get_object_or_404

from .models import Record


def list_records():
    return Record.objects.all()


def delete_record(record_id):
    record = get_object_or_404(Record, pk=record_id)
    record.delete()
    return record_id


def create_record(**kwargs):
    return Record.objects.create(
        continuous_feature1=kwargs["continuous_feature1"],
        continuous_feature2=kwargs["continuous_feature2"],
        categorical_feature1=kwargs["categorical_feature1"]
    )
