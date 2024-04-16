from django.http import HttpResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
from rest_framework.exceptions import NotFound


# Product views
class ProductCreateAPIView(APIView):
    def post(self, request):
        product_data = request.data.get('producto', {})
        details_data = request.data.pop('detalles', [])
        images_data = request.data.pop('imagenes', [])

        product_serializer = ProductoSerializer(data=product_data)

        if not product_serializer.is_valid():
            return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        product_instance = product_serializer.save()

        for detail in details_data:
            detail['producto'] = product_instance.pk
            detail_serializer = DetalleSerializer(data=detail)
            if not detail_serializer.is_valid():
                return Response(detail_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            detail_instance = detail_serializer.save(producto=product_instance)
            for img in images_data:
                img['detalle'] = detail_instance.pk
                img_serializer = ImagenSerializer(data=img)
                if img_serializer.is_valid():
                    img_instance = img_serializer.save(detalle=detail_instance)
                    print(img_instance)
                else:
                    return Response(img_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(product_serializer.data, status=status.HTTP_201_CREATED)


class ProductListAPIView(APIView):
    def get(self, request):
        products = Producto.objects.all()
        serializer = ProductoSerializer(products, many=True)
        return Response(serializer.data)

class DetalleProductoApi(APIView):
    def get(self, request):
        detalle = Detalle.objects.all()[:10]
        serializer = DetalleProductoSerializer(detalle, many=True)
        return Response(serializer.data)
class ProductDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Producto.objects.get(pk=pk)
        except Producto.DoesNotExist:
            raise NotFound(detail='Product not found', code=status.HTTP_404_NOT_FOUND)

    def get_pk(self, request):
        pk = request.query_params.get('pk')
        if pk is None:
            raise Response({'error': 'without "pk" in request params'}, status=status.HTTP_400_BAD_REQUEST)
        return pk

    def get(self, request):
        pk = self.get_pk(request)
        product = self.get_object(pk)
        if product is None:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductoSerializer(product)
        return Response(serializer.data)

    def put(self, request):
        pk = self.get_pk(request)
        product = self.get_object(pk)
        if product:
            serializer = ProductoSerializer(product, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        pk = self.get_pk(request)
        product = self.get_object(pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
            raise NotFound(detail='Category not found', code=status.HTTP_404_NOT_FOUND)

    def get_pk(self, request):
        pk = request.query_params.get('pk')
        if pk is None:
            raise Response({'error': 'without "pk" in request params'}, status=status.HTTP_400_BAD_REQUEST)
        return pk

    def get(self, request):
        pk = self.get_pk(request)
        category = self.get_object(pk)
        if category is None:
            return Response({'error': 'category not found'}, status=status.HTTP_404_NOT_FOUND)
        category_name = category.nombre
        return Response({'nombre': category_name})

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
            return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

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


class RudDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Detalle.objects.get(pk=pk)
        except Detalle.DoesNotExist:
            raise NotFound(detail='Detail not found', code=status.HTTP_404_NOT_FOUND)

    def get_pk(self, request):
        pk = request.query_params.get('pk')
        if pk is None:
            raise Response({'error': 'without "pk" in request params'}, status=status.HTTP_400_BAD_REQUEST)
        return pk

    def get(self, request):
        pk = self.get_pk(request)
        detail = self.get_object(pk)
        if detail is None:
            return Response({'error': 'detail not found'}, status=status.HTTP_404_NOT_FOUND)
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
            return Response({'error': 'Detail not found'}, status=status.HTTP_404_NOT_FOUND)


def delete(self, request):
    pk = self.get_pk(request)
    detail = self.get_object(pk)
    detail.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)