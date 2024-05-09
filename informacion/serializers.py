from rest_framework.serializers import ModelSerializer, ReadOnlyField
from .models import (
    InfoBar,
    HomeText,
    HomeStartImage,
    HomeCombinationsImage,
    HomeProductsImage,
    HomeAlliesImage,
)


class HomeTextSerializer(ModelSerializer):
    class Meta:
        model = HomeText
        fields = (
            "start_title",
            "start_text_one",
            "start_text_two",
            "combinations_title",
            "combinations_text",
            "products_text",
            "allies_text",
        )


class HomeStartImageSerializer(ModelSerializer):
    url = ReadOnlyField()

    class Meta:
        model = HomeStartImage
        fields = (
            "url",
            "start_image",
        )


class HomeCombinationsImageSerializer(ModelSerializer):
    url = ReadOnlyField()

    class Meta:
        model = HomeCombinationsImage
        fields = (
            "url",
            "combinations_image",
        )


class HomeProductsImageSerializer(ModelSerializer):
    url = ReadOnlyField()

    class Meta:
        model = HomeProductsImage
        fields = (
            "url",
            "products_image",
        )


class HomeAlliesImageSerializer(ModelSerializer):
    url = ReadOnlyField()

    class Meta:
        model = HomeAlliesImage
        fields = (
            "url",
            "allies_image",
        )


class InfoBarSerializer(ModelSerializer):
    class Meta:
        model = InfoBar
        fields = ("title", "phone_one", "phone_two", "address")
