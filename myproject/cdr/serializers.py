from rest_framework import serializers
from .models import CallDetailRecord


class CallDetailRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallDetailRecord
        fields = (
            'call_id', 'caller_number', 'callee_number', 'start_time', 'end_time', 'duration', 'call_type',
            'call_status')
