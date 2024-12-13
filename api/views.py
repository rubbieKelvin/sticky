import pydantic
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import HttpRequest, HttpResponse, QueryDict
from .models import Clipboard


class PushText(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(from_attributes=True)
    text: str
    view_once: bool = True


def index_view(request: HttpRequest) -> HttpResponse:
    return render(request, "paste.html")


class PushApiView(APIView):
    def get(self, request: Request) -> HttpResponse:
        return render(request._request, "paste.html")

    def post(self, request: Request) -> Response | HttpResponse:
        try:
            body = PushText.model_validate(
                request.data.dict()
                if isinstance(request.data, QueryDict)
                else request.data
            )
        except Exception as e:
            raise e

        content = Clipboard.objects.create(text=body.text, view_once=body.view_once)

        format = request.query_params.get("f", "ui")

        if not (format in ["ui", "api"]):
            return Response({"error": "Invalid preview format"}, status=400)

        res = {
            "id": content.public_id,
            "content-length": len(body.text),
            "url": request._request.get_host() + f"/pull/{content.public_id}",
        }
        if format == "ui":
            return render(request._request, "info.html", res)

        return Response(res)


@api_view(["GET"])
def pull_content(request: Request, id: str) -> Response | HttpResponse:

    try:
        content = Clipboard.objects.get(public_id=id)
    except Clipboard.DoesNotExist:
        return Response({"error": "Data not found"}, status=404)

    format = request.query_params.get("f", "ui")

    if not (format in ["ui", "api"]):
        return Response({"error": "Invalid preview format"}, status=400)

    text = content.text

    if content.view_once:
        content.delete()

    data = {"text": text, "deleted": content.view_once}

    if format == "ui":
        return render(request._request, "copy.html", data)

    return Response(
        {"text": text, "deleted": content.view_once},
    )
