from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import PDFDocument
from .serializers import PDFDocumentSerializer
from .utils.utils import extract_text_from_pdf
from .utils.ai_engine import summarize_text

# Create your views here.


class PDFDocumentViewSet(viewsets.ModelViewSet):
    serializer_class = PDFDocumentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PDFDocument.objects.filter(user=self.request.user).order_by(
            "-created_at"
        )

    def perform_create(self, serializer):
        file = self.request.FILES.get("file")
        if not file:
            raise serializers.ValidationError({"file": "PDF file is required"})

        extracted_text = extract_text_from_pdf(file)
        if not extracted_text:
            raise serializers.ValidationError(
                {"file": "Could not extract text from PDF"}
            )

        summary = summarize_text(extracted_text)
        if not summary:
            raise serializers.ValidationError({"summary": "Could not generate summary"})

        serializer.save(
            user=self.request.user, extracted_text=extracted_text, summary=summary
        )

    @action(detail=True, methods=["post"])
    def summarize(self, request, pk=None):
        """
        Custom action to re-generate summary for an existing PDF.
        """
        pdf_document = self.get_object()

        # Generate new summary
        if pdf_document.extracted_text:
            summary = summarize_text(
                pdf_document.extracted_text,
            )

            if summary:
                pdf_document.summary = summary
                pdf_document.save()

                serializer = self.get_serializer(pdf_document)
                return Response(serializer.data)
            else:
                return Response(
                    {"error": "Failed to generate summary"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        else:
            return Response(
                {"error": "No extracted text available"},
                status=status.HTTP_400_BAD_REQUEST,
            )
