from rest_framework import generics, status
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import CallDetailRecord
from .serializers import CallDetailRecordSerializer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


class CDRListCreateView(generics.ListCreateAPIView):
    queryset = CallDetailRecord.objects.all()
    serializer_class = CallDetailRecordSerializer
    parser_classes = [JSONParser, ]
    # permission_classes = [IsAuthenticated, ]

    def create(self, request, *args, **kwargs):
        cdr_data = request.data.get('cdr_data')
        if cdr_data:
            processed_cdrs = []
            for cdr_entry in cdr_data:
                try:
                    serializer = CallDetailRecordSerializer(data=cdr_entry)
                    if serializer.is_valid():
                        serializer.save()
                        processed_cdrs.append(serializer.data)
                    else:
                        processed_cdrs.append({"error": serializer.errors})
                except Exception as e:
                    return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"message": "CDR data processed successfully", "processed_cdrs": processed_cdrs},
                            status=status.HTTP_201_CREATED)

        return super().create(request, *args, **kwargs)


class CDRDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CallDetailRecord.objects.all()
    serializer_class = CallDetailRecordSerializer
    parser_classes = [JSONParser, ]
    permission_classes = [IsAuthenticated, ]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
