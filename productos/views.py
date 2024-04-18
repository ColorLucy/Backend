from django.http import HttpResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from django.db import transaction


# create product
class ProductCreateAPIView(APIView):
    def post(self, request):
        product_data = request.data.get("producto", {})
        details_data = request.data.pop("detalles", [])
        images_data = request.data.pop("imagenes", [])

        product_serializer = ProductoSerializer(data=product_data)

        if not product_serializer.is_valid():
            return Response(
                product_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        product_instance = product_serializer.save()

        for detail in details_data:
            detail["producto"] = product_instance.pk
            detail_serializer = DetalleSerializer(data=detail)
            if not detail_serializer.is_valid():
                return Response(
                    detail_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
            detail_instance = detail_serializer.save(producto=product_instance)
            for img in images_data:
                img["detalle"] = detail_instance.pk
                img_serializer = ImagenSerializer(data=img)
                if img_serializer.is_valid():
                    img_instance = img_serializer.save(detalle=detail_instance)
                else:
                    return Response(
                        img_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )

        return Response(product_serializer.data, status=status.HTTP_201_CREATED)

class ProductGetAllAPIView(APIView):
    def get_pk(self, request):
        pk = request.query_params.get('pk')
        if pk is None:
            raise Response({'error': 'without "pk" in request params'}, status=status.HTTP_400_BAD_REQUEST)
        return pk
    
    def get(self, request):
        pk = self.get_pk(request)
        try:
            product_instance = Producto.objects.get(pk=pk)
        except Producto.DoesNotExist:
            return Response({"error": "Product does not exist"}, status=status.HTTP_404_NOT_FOUND)

        product_serializer = ProductoSerializer(product_instance)
        details_queryset = Detalle.objects.filter(producto=product_instance)
        detail_serializer = DetalleSerializer(details_queryset, many=True)
        images_queryset = Imagen.objects.filter(detalle__in=details_queryset)
        image_serializer = ImagenSerializer(images_queryset, many=True)

        data = {
            "product": product_serializer.data,
            "details": detail_serializer.data,
            "images": image_serializer.data,
        }

        return Response(data, status=status.HTTP_200_OK)
    
class ProductUpdateAPIView(APIView):
    def get_pk(self, request):
        pk = request.query_params.get('pk')
        if pk is None:
            raise Response({'error': 'without "pk" in request params'}, status=status.HTTP_400_BAD_REQUEST)
        return pk
    
    def put(self, request):
        pk = self.get_pk(request)
        try:
            product_instance = Producto.objects.get(pk=pk)
        except Producto.DoesNotExist:
            return Response({"error": "Product does not exist"}, status=status.HTTP_404_NOT_FOUND)

        product_data = request.data.get('producto', {})
        details_data = request.data.pop('detalles', [])
        images_data = request.data.pop('imagenes', [])

        product_serializer = ProductoSerializer(instance=product_instance, data=product_data)
        if product_serializer.is_valid():
            # update product data
            updated_product = product_serializer.save()

            # update details data
            for detail in details_data:
                detail['producto'] = product_instance.pk
                detail_id = detail.get('id_detalle')
                if detail_id:
                    try:
                        detail_instance = Detalle.objects.get(pk=detail_id)
                        detail_serializer = DetalleSerializer(instance=detail_instance, data=detail)
                    except Detalle.DoesNotExist:
                        return Response({"error": f"Detail with ID {detail_id} does not exist"}, status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response({"error": "id_detalle is required"}, status=status.HTTP_400_BAD_REQUEST)

                if detail_serializer.is_valid():
                    updated_detail = detail_serializer.save(producto=updated_product)
                else:
                    return Response(detail_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # delete and add images
            with transaction.atomic():
                existing_image_ids = list(Imagen.objects.filter(detalle__producto=product_instance).values_list('pk', flat=True))
                updated_image_ids = []
                for img_data in images_data:
                    image_id = img_data.get('id_imagen')
                    if image_id:
                        updated_image_ids.append(image_id)
                        try:
                            image_instance = Imagen.objects.get(pk=image_id, detalle__producto=product_instance)
                            image_serializer = ImagenSerializer(instance=image_instance, data=img_data)
                        except Imagen.DoesNotExist:
                            return Response({"error": f"Image with ID {image_id} does not exist for this product"}, status=status.HTTP_404_NOT_FOUND)

                        if image_serializer.is_valid():
                            image_serializer.save(detalle=image_instance.detalle)
                        else:
                            return Response(image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        img_data['detalle'] = updated_detail.pk
                        new_image_serializer = ImagenSerializer(data=img_data)
                        if new_image_serializer.is_valid():
                            new_image_serializer.save()
                        else:
                            return Response(new_image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                images_to_delete = set(existing_image_ids) - set(updated_image_ids)
                Imagen.objects.filter(pk__in=images_to_delete).delete()
                    
            return Response({"message": "Product updated successfully"}, status=status.HTTP_200_OK)
        else:
            return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDeleteAPIView(APIView):
    def get_pk(self, request):
        pk = request.query_params.get('pk')
        if pk is None:
            raise Response({'error': 'without "pk" in request params'}, status=status.HTTP_400_BAD_REQUEST)
        return pk
    
    def get_object(self, pk, table):
        try:
            return table.objects.get(pk=pk)
        except Categoria.DoesNotExist:
            return None
        
    def delete(self, request):
        pk = self.get_pk(request)
        product = self.get_object(pk, Producto)

        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProductListAPIView(APIView):
    def get(self, request):
        products = Producto.objects.all()[:25]
        serializer = ProductoDetalleImagenSerializer(products, many=True)
        return Response(serializer.data)
    
class DetalleProductoApi(APIView):
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
