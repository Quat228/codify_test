from rest_framework import views
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404


class MyGenericListCreateView(views.APIView):
    queryset = None
    serializer_class = None

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.queryset.all(), many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)


class MyGenericRetrieveUpdateDestroyView(views.APIView):
    queryset = None
    serializer_class = None

    def get_object(self, pk):
        return get_object_or_404(self.queryset.all(), pk=pk)

    def get(self, request, pk, *args, **kwargs):
        serializer = self.serializer_class(instance=self.get_object(pk))
        return Response(serializer.data)

    def put(self, request, pk, *args, **kwargs):
        serializer = self.serializer_class(instance=self.get_object(pk), data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

    def delete(self, request, pk, *args, **kwargs):
        self.get_object(pk).delete()
        return Response(status=204)
