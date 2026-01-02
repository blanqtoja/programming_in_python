import json
from http import HTTPStatus
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, JsonResponse, HttpResponseBadRequest

from .services import delete_record, create_record, list_records
from .serializers import serialize_records
from .forms import RecordForm
from .models import Record


def index(request):
    records = list_records()
    context = {"records": records}
    return render(request, "datahub/index.html", context)


def delete(request, record_id):
    if request.method == "POST":
        try:
            rec_id = delete_record(record_id)
            return redirect("datahub:index")
        except Http404:
            return render(request, "datahub/error_404.html", status=HTTPStatus.NOT_FOUND)
    else:
        return render(request, "datahub/error_400.html", status=HTTPStatus.BAD_REQUEST)


def add(request):
    if request.method == "POST":
        form = RecordForm(request.POST)
        if form.is_valid():
            record = create_record(
                continuous_feature1=form.cleaned_data["float1"],
                continuous_feature2=form.cleaned_data["float2"],
                categorical_feature1=form.cleaned_data["int_value1"],
            )
            return redirect("datahub:index")
        return render(request, "datahub/add.html", {"form": form}, status=HTTPStatus.BAD_REQUEST)

    else:
        form = RecordForm()
        return render(request, "datahub/add.html", {"form": form})


def api_data(request):
    if request.method == "GET":
        records = serialize_records()
        return JsonResponse(records, safe=False)

    elif request.method == "POST":
        try:
            body = json.loads(request.body)
            record = create_record(**body)

            return JsonResponse({"record_id": record.id}, status=HTTPStatus.CREATED)
        except (ValueError, TypeError, KeyError) as e:
            return HttpResponseBadRequest(
                {
                    "error": e,
                    "message": "Invalid data",
                }
            )
    else:
        return HttpResponseBadRequest(
            {
                "message": "Invalid method",
            }
        )


# DELETE /api/data/<record_id>
# (where <record_id> stands for the primary key of a record) -
# deletes a data point from the database.
#  The <record_id> should be validated to check if the database contains a record with a matching primary key
# and if the validation succeeds,
#   the corresponding record should be deleted from the database
#   and a response comprising a JSON that contains a dictionary specifying the primary key of the deleted record should follow.
# If the validation fails,
#   a response incorporating the 404 HTTP status code and comprising a JSON that contains a dictionary specifying
#   a relevant error message (e.g., "Record not found") should be generated.

def api_delete(request, record_id):
    if request.method == "DELETE":
        try:
            rec_id = delete_record(record_id)
            return JsonResponse({"record_id": rec_id}, status=HTTPStatus.OK)
        except Http404 as e:
            return JsonResponse(
                {
                    "error": e,
                    "message": "Record not found",
                },
                status=HTTPStatus.NOT_FOUND
            )
    else:
        return HttpResponseBadRequest(
            {
                "message": "Invalid method",
            }
        )
