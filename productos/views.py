from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from .models import *
from .serializers import *
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404

class ProductosDetalleAPIView(APIView):
    def get(self, request):
        productos = Producto.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 20
        productos_paginados = paginator.paginate_queryset(productos, request)
        serializer = ProductoDetalleImagenSerializer(productos_paginados, many=True)
        return paginator.get_paginated_response(serializer.data)
class ProductListAPIView(APIView):#eliminar esta
    def get(self, request):
        products = Producto.objects.all()
        serializer = ProductoSerializer(products, many=True)
        return Response(serializer.data)


class ProductoDetalleAPIView(APIView):
    def get(self, request, *args, **kwargs):
        producto_id = kwargs.get('producto_id')
        producto = get_object_or_404(Producto, pk=producto_id)
        serializer = ProductoDetalleImagenSerializer(producto, many=False)
        return Response(serializer.data)


class DetallesPorCategoriaAPIView(APIView):
    serializer_class = ProductoDetalleImagenSerializer

    def get(self, request, *args, **kwargs):
        categoria_id = kwargs.get('categoria_id')  #
        #categoria = get_object_or_404(Categoria, pk=categoria_id)
        if categoria_id is None:
            return Response({"message": "El ID de la categoría es necesario"}, status=status.HTTP_400_BAD_REQUEST)

        productos = Producto.objects.filter(categoria_id=categoria_id)
        paginator = PageNumberPagination()
        paginator.page_size = 20
        detalles_paginados = paginator.paginate_queryset(productos, request)
        serializer = self.serializer_class(detalles_paginados, many=True)
        return paginator.get_paginated_response(serializer.data)


# Category views
class CategoryCreateAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = CategoriaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailAPIView(APIView):
    permission_classes = [AllowAny]
    def get_object(self, pk):
        try:
            return Categoria.objects.get(pk=pk)
        except Categoria:
            raise NotFound(detail="Category not found", code=status.HTTP_404_NOT_FOUND)

    def get(self, request):
        pk = request.query_params.get("pk")
        category = self.get_object(pk)
        if category is None:
            return Response(
                {"error": "category not found"}, status=status.HTTP_404_NOT_FOUND
            )
        category_name = category.nombre
        return Response({"nombre": category_name})

    def put(self, request):
        pk = request.query_params.get("pk")
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
        pk = request.query_params.get("pk")
        category = self.get_object(pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CategoryListAPIView(APIView):
    def get(self, request):
        categories = Categoria.objects.all()
        serializer = CategoriaSerializer(categories, many=True)
        return Response(serializer.data)


class ProductSearchAPIView(APIView):
    def get(self, request):
        search_term = request.query_params.get('q', '')
        if search_term:
            detalles = Producto.objects.filter(nombre__icontains=search_term)
            paginator = PageNumberPagination()
            paginator.page_size = 20
            detalles_paginados = paginator.paginate_queryset(detalles, request)
            serializer = ProductoDetalleImagenSerializer(detalles_paginados, many=True)
            return paginator.get_paginated_response(serializer.data)
        else:
            return Response("No se proporcionó un término de búsqueda", status=status.HTTP_400_BAD_REQUEST)