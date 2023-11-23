from django.db import models


class CallDetailRecord(models.Model):
    CALL_TYPES = (
        ('outgoing', 'Outgoing'),
        ('incoming', 'Incoming'),
        ('missed', 'Missed'),
    )
    CALL_STATUS = (
        ('successful', 'Successful'),
        ('unanswered', 'Unanswered'),
        ('rejected', 'Rejected'),
    )

    call_id = models.UUIDField(primary_key=True)
    caller_number = models.CharField(max_length=20)
    callee_number = models.CharField(max_length=20)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration = models.DurationField()
    call_type = models.CharField(max_length=10, choices=CALL_TYPES)
    call_status = models.CharField(max_length=15, choices=CALL_STATUS)
