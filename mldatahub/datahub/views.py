import json
from http import HTTPStatus
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, JsonResponse, HttpResponseBadRequest
from .models import Record


def index(request):
    records = Record.objects.order_by("id")
    context = {"records": records}
    return render(request, "datahub/index.html", context)


def delete(request, record_id):
    if request.method == "POST":
        try:
            record = get_object_or_404(Record, pk=record_id)
            record.delete()
            return redirect("datahub:index")
        except Http404:
            return render(request, "datahub/error_404.html", status=HTTPStatus.NOT_FOUND)
    else:
        return render(request, "datahub/error_400.html", status=HTTPStatus.BAD_REQUEST)


def add(request):
    if request.method == "POST":
        try:
            continuous_feature1 = float(request.POST.get("float1"))
            continuous_feature2 = float(request.POST.get("float2"))
            categorical_feature1 = int(request.POST.get("int_value"))

            Record.objects.create(
                continuous_feature1=continuous_feature1,
                continuous_feature2=continuous_feature2,
                categorical_feature1=categorical_feature1
            )

            return redirect("datahub:index")
        except (ValueError, TypeError):
            return render(request, "datahub/error_400.html", status=HTTPStatus.BAD_REQUEST)
    else:
        # render form
        return render(request, "datahub/add.html")


def api_data(request):
    if request.method == "GET":
        records = Record.objects.all()
        data = []
        for record in records:
            data.append({
                "id": record.id,
                "continuous_feature1": record.continuous_feature1,
                "continuous_feature2": record.continuous_feature2,
                "categorical_feature1": record.categorical_feature1
            })
        return JsonResponse(data, safe=False)

    elif request.method == "POST":
        try:
            body = json.loads(request.body.read())

            record = Record.objects.create(
                continuous_feature1=body["continuous_feature1"],
                continuous_feature2=body["continuous_feature2"],
                categorical_feature1=body["categorical_feature1"]
            )
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
            record = get_object_or_404(Record, pk=record_id)
            record.delete()
            return JsonResponse({"record_id": record.id}, status=HTTPStatus.OK)
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
