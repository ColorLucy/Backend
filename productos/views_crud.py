from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
from django.db import transaction


class ProductCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
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
                    img_serializer.save(detalle=detail_instance)
                else:
                    return Response(
                        img_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )
        return Response(product_serializer.data, status=status.HTTP_201_CREATED)

class ProductGetAllAPIView(APIView):
    permission_classes = [IsAuthenticated]
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
    permission_classes = [IsAuthenticated]
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
            updated_product = product_serializer.save()
            existing_detail_ids = list(Detalle.objects.filter(producto=product_instance).values_list('id_detalle', flat=True))
            updated_detail_ids = []

            for detail in details_data:
                detail_id = detail.get('id_detalle')
                if detail_id:
                    updated_detail_ids.append(detail_id)
                    try:
                        detail_instance = Detalle.objects.get(pk=detail_id)
                        detail_serializer = DetalleSerializer(instance=detail_instance, data=detail)
                    except Detalle.DoesNotExist:
                        return Response({"error": f"Detail with ID {detail_id} does not exist"}, status=status.HTTP_404_NOT_FOUND)
                else:
                    detail_serializer = DetalleSerializer(data=detail)

                if detail_serializer.is_valid():
                    new_detail = detail_serializer.save(producto=updated_product)
                else:
                    return Response(detail_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            details_to_delete = set(existing_detail_ids) - set(updated_detail_ids)
            Detalle.objects.filter(pk__in=details_to_delete).delete()

            with transaction.atomic():
                existing_image_ids = list(Imagen.objects.filter(detalle__producto=product_instance).values_list('pk', flat=True))
                updated_image_ids = []

                for img_data in images_data:
                    image_id = img_data.get('id_imagen')
                    is_detail_valid = img_data.get('detalle')
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

                    elif is_detail_valid != None:
                        img_data['detalle'] = img_data.get('detalle')
                        new_image_serializer = ImagenSerializer(data=img_data)
                        if new_image_serializer.is_valid():
                            new_image_serializer.save()

                    else:
                        img_data['detalle'] = new_detail.pk
                        new_image_serializer = ImagenSerializer(data=img_data)
                        if new_image_serializer.is_valid():
                            new_image_serializer.save()

                images_to_delete = set(existing_image_ids) - set(updated_image_ids)
                Imagen.objects.filter(pk__in=images_to_delete).delete()         
            return Response({"message": "Product updated successfully"}, status=status.HTTP_200_OK)
        else:
            return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]
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