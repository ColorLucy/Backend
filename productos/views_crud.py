from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *
from django.db import transaction
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication

class ProductCreateAPIView(APIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    def post(self, request):
        product_data = request.data.get("producto", {})
        details_data = request.data.pop("detalles", [])
        images_data = request.data.pop("imagenes", [])
        print(product_data)
        print(details_data)
        print(images_data)

        if product_data['descripcion'] == "":
            product_data['descripcion'] = None
        product_serializer = ProductoSerializer(data=product_data)
        if not product_serializer.is_valid():
            print("producto-------")
            return Response(
                product_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        product_instance = product_serializer.save()

        for detail in details_data:
            detail['producto'] = product_instance.pk
            if detail['color'] == "":
                detail['color'] = "NA"
            detail_serializer = DetalleSerializer(data=detail)
            if not detail_serializer.is_valid():
                print("detalle-------")
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
                    print("img-----------")
                    return Response(
                        img_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )
        return Response(product_serializer.data, status=status.HTTP_201_CREATED)

class ProductGetAllAPIView(APIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
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

        product_serializer = ProductoDetalleImagenSerializer(product_instance)
        return Response(product_serializer.data, status=status.HTTP_200_OK)

class ProductUpdateAPIView(APIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
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

        product_data = request.data
        product_data['categoria'] = product_data['categoria'].get('id_categoria')
        if product_data.get('descripcion', "") == "":
            product_data['descripcion'] = None

        details_data = product_data.pop('detalles', None)

        product_serializer = ProductoSerializer(instance=product_instance, data=product_data)
        if not product_serializer.is_valid():
            return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            updated_product = product_serializer.save()
            
            existing_detail_ids = list(Detalle.objects.filter(producto=product_instance).values_list('id_detalle', flat=True))
            existing_image_ids = list(Imagen.objects.filter(detalle__producto=product_instance).values_list('pk', flat=True))
            updated_detail_ids = []
            updated_image_ids = []

            for detail in details_data:
                detail_id = detail.get('id_detalle')
                detail_images = detail.pop('imagenes', [])
                if detail['color'] == "":
                    detail['color'] = "NA"
                detail['producto'] = updated_product.pk

                if detail_id:
                    try:
                        detail_instance = Detalle.objects.get(pk=detail_id)
                    except Detalle.DoesNotExist:
                        return Response({"error": f"Detail with id {detail_id} does not exist"},
                                        status=status.HTTP_400_BAD_REQUEST)
                    detail_serializer = DetalleSerializer(instance=detail_instance, data=detail)
                    updated_detail_ids.append(detail_id)
                else:
                    detail_serializer = DetalleSerializer(data=detail)

                if not detail_serializer.is_valid():
                    return Response(detail_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                new_or_updated_detail = detail_serializer.save()

                for image in detail_images:
                    image['detalle'] = new_or_updated_detail.pk
                    image_id = image.get('id_imagen')
                    if image_id:
                        try:
                            image_instance = Imagen.objects.get(pk=image_id)
                        except Imagen.DoesNotExist:
                            return Response({"error": f"Image with id {image_id} does not exist"},
                                            status=status.HTTP_400_BAD_REQUEST)
                        image_serializer = ImagenSerializer(instance=image_instance, data=image)
                        updated_image_ids.append(image_id)
                    else:
                        image_serializer = ImagenSerializer(data=image)

                    if not image_serializer.is_valid():
                        return Response(image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                    image_serializer.save()

            images_to_delete = set(existing_image_ids) - set(updated_image_ids)
            Imagen.objects.filter(pk__in=images_to_delete).delete()
            details_to_delete = set(existing_detail_ids) - set(updated_detail_ids)
            Detalle.objects.filter(pk__in=details_to_delete).delete()
        return Response({"message": "Product updated successfully"}, status=status.HTTP_200_OK)


class ProductDeleteAPIView(APIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
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
