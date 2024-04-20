from django.http import HttpResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination


class ProductListAPIView(APIView):
    def get(self, request):
        products = Producto.objects.all()
        serializer = ProductoSerializer(products, many=True)
        return Response(serializer.data)


class DetalleProductoAPIView(APIView):
    def get(self, request):
        detalle = Detalle.objects.all()[:10]
        serializer = DetalleProductoSerializer(detalle, many=True)
        return Response(serializer.data)


class DetallesPorCategoriaAPIView(APIView):
    serializer_class = DetalleProductoSerializer


# Category views
class CategoryCreateAPIView(APIView):
    def post(self, request):
        serializer = CategoriaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryListAPIView(APIView):
    def get(self, request):
        categories = Categoria.objects.all()
        serializer = CategoriaSerializer(categories, many=True)
        return Response(serializer.data)


class CategoryDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Categoria.objects.get(pk=pk)
        except Categoria.DoesNotExist:
            raise NotFound(detail="Category not found", code=status.HTTP_404_NOT_FOUND)

    def get_pk(self, request):
        pk = request.query_params.get("pk")
        if pk is None:
            raise Response(
                {"error": 'without "pk" in request params'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return pk

    def get(self, request):
        pk = self.get_pk(request)
        category = self.get_object(pk)
        if category is None:
            return Response(
                {"error": "category not found"}, status=status.HTTP_404_NOT_FOUND
            )
        category_name = category.nombre
        return Response({"nombre": category_name})

    def put(self, request):
        pk = self.get_pk(request)
        category = self.get_object(pk)
        if category:
            serializer = CategoriaSerializer(category, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request):
        pk = self.get_pk(request)
        category = self.get_object(pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Detail views
class DetailCreateAPIView(APIView):
    def post(self, request):
        serializer = DetalleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DetailListAPIView(APIView):
    def get(self, request):
        details = Detalle.objects.all()
        serializer = DetalleSerializer(details, many=True)
        return Response(serializer.data)


# Experimental APIView, may be useful in the future or not
class DetailPaginatedListAPIView(APIView):
    def get(self, request):
        details = Detalle.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 10
        details_page = paginator.paginate_queryset(details, request)
        serializer = DetalleSerializer(details_page, many=True)
        return paginator.get_paginated_response(serializer.data)


# Experimental APIView, may be useful in the future or not
class DetailImageListAPIView(APIView):
    def get(self, request):
        details = Imagen.objects.all()
        serializer = DetalleImagenSerializer(details, many=True)
        return Response(serializer.data)


class RudDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Detalle.objects.get(pk=pk)
        except Detalle.DoesNotExist:
            raise NotFound(detail="Detail not found", code=status.HTTP_404_NOT_FOUND)

    def get_pk(self, request):
        pk = request.query_params.get("pk")
        if pk is None:
            raise Response(
                {"error": 'without "pk" in request params'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return pk

    def get(self, request):
        pk = self.get_pk(request)
        detail = self.get_object(pk)
        if detail is None:
            return Response(
                {"error": "detail not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = DetalleSerializer(detail)
        return Response(serializer.data)

    def put(self, request):
        pk = self.get_pk(request)
        detail = self.get_object(pk)
        if detail:
            serializer = DetalleSerializer(detail, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {"error": "Detail not found"}, status=status.HTTP_404_NOT_FOUND
            )

    def delete(self, request):
        pk = self.get_pk(request)
        detail = self.get_object(pk)
        detail.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

