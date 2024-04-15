from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *


# create product
class ProductCreateAPIView(APIView):
    def post(self, request):
        product_data = request.data.get('producto', {})
        details_data = request.data.pop('detalles', [])
        images_data = request.data.pop('imagenes', [])

        product_serializer = ProductoSerializer(data=product_data)

        if product_serializer.is_valid():
            product_instance = product_serializer.save()
            detail_instance = None

            print(product_instance)
            for detail in details_data:
                detail['producto'] = product_instance.pk
                detail_serializer = DetalleSerializer(data=detail)
                if detail_serializer.is_valid():
                    detail_instance = detail_serializer.save(producto=product_instance)
                    print(detail_instance)
                else:
                    errors = {
                        **detail_serializer.errors,
                    }
                    return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        
            for img in images_data:
                img['detalle'] = detail_instance.pk
                img_serializer = ImagenSerializer(data=img)
                if img_serializer.is_valid():
                    img_instance = img_serializer.save(detalle=detail_instance)
                    print(img_instance)
                else:
                    errors = {
                        **img_serializer.errors,
                    }
                    return Response(errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(product_serializer.data, status=status.HTTP_201_CREATED)
        errors = {
            **product_serializer.errors,
        }
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)


# view all products
class ProductListAPIView(APIView):
    def get(self, request):
        products = Producto.objects.all()
        serializer = ProductoSerializer(products, many=True)
        return Response(serializer.data)

# product: get, update, delete
class ProductDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Producto.objects.get(pk=pk)
        except Producto.DoesNotExist:
            return None
   
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
        serializer = ProductoSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        pk = self.get_pk(request)
        product = self.get_object(pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

# CATEGORIES

# create category
class CategoryCreateAPIView(APIView):
    def post(self, request):
        print(request.data)
        serializer = CategoriaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# view all categories
class CategoryListAPIView(APIView):
    def get(self, request):
        categories = Categoria.objects.all()
        serializer = CategoriaSerializer(categories, many=True)
        return Response(serializer.data)
    
# category: get, update, delete
class CategoryDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Categoria.objects.get(pk=pk)
        except Categoria.DoesNotExist:
            return None
   
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
        serializer = CategoriaSerializer(category)
        return Response(serializer.data)

    def put(self, request):
        pk = self.get_pk(request)
        category = self.get_object(pk)
        serializer = CategoriaSerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        pk = self.get_pk(request)
        category = self.get_object(pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

# DETAILS
# create detail
class DetailCreateAPIView(APIView):
    def post(self, request):
        serializer = DetalleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# view all details
class DetailListAPIView(APIView):
    def get(self, request):
        details = Detalle.objects.all()
        serializer = DetalleSerializer(details, many=True)
        return Response(serializer.data)
    
# detail: get, update, delete
class RudDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Detalle.objects.get(pk=pk)
        except Detalle.DoesNotExist:
            return None
   
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
        serializer = CategoriaSerializer(detail)
        return Response(serializer.data)

    def put(self, request):
        pk = self.get_pk(request)
        detail = self.get_object(pk)
        serializer = CategoriaSerializer(detail, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else: return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        pk = self.get_pk(request)
        detail = self.get_object(pk)
        detail.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)