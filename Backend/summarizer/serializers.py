from rest_framework import serializers
from .models import PDFDocument


class PDFDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PDFDocument
        fields = ["id", "file", "extracted_text", "summary", "created_at"]
        read_only_fields = ["id", "created_at", "summary", "extracted_text"]
