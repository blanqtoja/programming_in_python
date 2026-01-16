import json
from http import HTTPStatus
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, JsonResponse
from .services import delete_record, create_record, list_records
from .serializers import parse_predict_input, serialize_records
from .forms import RecordForm, PredictForm
from .models import Record
from .predictor import predict_category


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
            return JsonResponse(
                {
                    "error": str(e),
                    "message": "Invalid data",
                },
                status=HTTPStatus.BAD_REQUEST
            )
    else:
        return JsonResponse(
            {
                "message": "Invalid method",
            },
            status=HTTPStatus.BAD_REQUEST
        )


def api_delete(request, record_id):
    if request.method == "DELETE":
        try:
            rec_id = delete_record(record_id)
            return JsonResponse({"record_id": rec_id}, status=HTTPStatus.OK)
        except Http404 as e:
            return JsonResponse(
                {
                    "error": str(e),
                    "message": "Record not found",
                },
                status=HTTPStatus.NOT_FOUND
            )
    else:
        return JsonResponse(
            {
                "message": "Invalid method",
            },
            status=HTTPStatus.BAD_REQUEST
        )


def predict(request):
    if request.method == "POST":
        form = PredictForm(request.POST)
        if form.is_valid():
            try:
                prediction = predict_category(
                    float1=form.cleaned_data["float1"],
                    float2=form.cleaned_data["float2"],
                )
                return render(request, "datahub/predict_result.html", {"predicted_category": prediction})
            except ValueError as e:
                return render(request, "datahub/error_400_no_records.html", {"error_message": str(e)}, status=HTTPStatus.BAD_REQUEST)

        return render(request, "datahub/predict.html", {"form": form}, status=HTTPStatus.BAD_REQUEST)

    else:
        form = PredictForm()
        return render(request, "datahub/predict.html", {"form": form})


def api_predict(request):
    if request.method == "GET":
        try:
            data = {
                'continuous_feature1': request.GET.get('continuous_feature1'),
                'continuous_feature2': request.GET.get('continuous_feature2'),
            }
            float1, float2 = parse_predict_input(data)
            prediction = predict_category(float1, float2)
            return JsonResponse({"predicted_category": int(prediction)}, status=HTTPStatus.OK)
        except (ValueError, KeyError, TypeError) as e:
            return JsonResponse(
                {
                    "error": str(e),
                    "message": "Invalid data",
                },
                status=HTTPStatus.BAD_REQUEST
            )
    else:
        return JsonResponse(
            {
                "message": "Invalid method",
            },
            status=HTTPStatus.BAD_REQUEST
        )
