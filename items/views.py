from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.generics import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import views
from rest_framework import viewsets

from . import models
from . import serializers
from . import my_generic


class CategoryListCreateAPIView(generics.ListCreateAPIView):
    """
    Category Create and List View
    :param Limit: int
    """
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer


class ItemListCreateAPIView(generics.ListCreateAPIView):
    queryset = models.Item.objects.all()
    serializer_class = serializers.ItemSerializer


@api_view(http_method_names=["GET", "POST"])
def item_list_create_api_view(request):
    # print(request.query_params)  # /?param=value
    # print(request.data)  # автоматически превращает json формат в python
    # data = [
    #     {
    #         "name": "Codify",
    #         "address": "7 mkr"
    #     }
    # ]
    if request.method == "GET":
        query_set = models.Item.objects.all()
        serializer = serializers.ItemSerializer(query_set, many=True)
        return Response(serializer.data)  # Response сериализует данные в json
    if request.method == "POST":
        serializer = serializers.ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)


@api_view(http_method_names=["GET", "PUT", "DELETE"])
def item_retrieve_update_destroy_api_view(request, pk):
    # try:
    #     item = models.Item.objects.get(pk=pk)
    # except models.Item.DoesNotExist:
    #     return Response({'detail': 'No object'}, status=404)

    item = get_object_or_404(models.Item, pk=pk)  # аналогично try

    if request.method == "GET":
        serializer = serializers.ItemSerializer(instance=item)
        return Response(serializer.data)

    if request.method == "PUT":
        serializer = serializers.ItemSerializer(instance=item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

    if request.method == "DELETE":
        item.delete()
        return Response(status=204)


class ItemListCreateView(my_generic.MyGenericListCreateView):
    queryset = models.Item.objects.all()
    serializer_class = serializers.ItemSerializer


# class ItemRetrieveUpdateDestroyView(views.APIView):
#     def get_object(self, pk):
#         return get_object_or_404(models.Item, pk=pk)
#
#     def get(self, request, pk, *args, **kwargs):
#         serializer = serializers.ItemSerializer(instance=self.get_object(pk))
#         return Response(serializer.data)
#
#     def put(self, request, pk, *args, **kwargs):
#         serializer = serializers.ItemSerializer(instance=self.get_object(pk), data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=400)
#
#     def delete(self, request, pk, *args, **kwargs):
#         self.get_object(pk).delete()
#         return Response(status=204)


class ItemRetrieveUpdateDestroyView(my_generic.MyGenericRetrieveUpdateDestroyView):
    queryset = models.Item.objects.all()
    serializer_class = serializers.ItemSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer

