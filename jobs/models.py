from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import datetime

class Job(models.Model):

    JOB_TYPE_CHOICES = (
        ('PCO', 'PCO'),
        ('MOT', 'MOT'),
        ('SERVICE', 'Service'),
    )

    STATUS_CHOICES = (
        ('NEW', 'New'),
        ('IN_PROCESS', 'In Process'),
        ('COMPLETED', 'Completed'),
        ('HOLD', 'Hold'),
    )

    appointment = models.CharField(max_length=100,blank=True,null=True,help_text="Car registration / appointment reference")

    scheduled_datetime = models.DateTimeField()
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)

    admin_comment = models.TextField(blank=True)
    mechanic_remark = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='NEW'
    )

    mechanic = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='assigned_jobs',
        limit_choices_to={'userprofile__role': 'MECHANIC'}
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_jobs'
    )

    created_at = models.DateTimeField(auto_now_add=True)


class JobInspection(models.Model):

    job = models.OneToOneField(
        Job,
        on_delete=models.CASCADE,
        related_name="inspection"
    )

    # SERVICE CHECKLIST
    engine_oil_change = models.BooleanField(default=False)
    oil_filter_change = models.BooleanField(default=False)
    cabin_filter = models.BooleanField(default=False)
    air_filter = models.BooleanField(default=False)
    spark_plugs = models.BooleanField(default=False)
    engine_coolant = models.BooleanField(default=False)
    wipers = models.BooleanField(default=False)
    battery = models.BooleanField(default=False)

    hybrid_filter = models.BooleanField(default=False)
    antifreeze = models.BooleanField(default=False)
    transmission_oil = models.BooleanField(default=False)
    washer_fluid = models.BooleanField(default=False)
    key_bettery = models.BooleanField(default=False)



    # BRAKES
    brake_pads_front = models.BooleanField(default=False)
    brake_pads_rear = models.BooleanField(default=False)

    # TYRES
    tyre_front_right = models.CharField(max_length=10, blank=True, null=True)
    tyre_front_left = models.CharField(max_length=10, blank=True, null=True)
    tyre_rear_right = models.CharField(max_length=10, blank=True, null=True)
    tyre_rear_left = models.CharField(max_length=10, blank=True, null=True)

    # Light Bulbs
    side_bulbs = models.BooleanField(default=False)
    h11_bulbs_left = models.BooleanField(default=False)
    h11_bulbs_right = models.BooleanField(default=False)
    hid_bulb_left = models.BooleanField(default=False)
    hid_bulb_right = models.BooleanField(default=False)

    # Others
    break_disc_fr = models.BooleanField(default=False)
    break_disc_re = models.BooleanField(default=False)
    shock_absorber_fr = models.BooleanField(default=False)
    shock_absorber_re = models.BooleanField(default=False)
    linkage = models.BooleanField(default=False)
    ball_joint = models.BooleanField(default=False)
    seat_cover = models.BooleanField(default=False)
    navigation = models.BooleanField(default=False)
    accident_camera = models.BooleanField(default=False)
    tracking_system = models.BooleanField(default=False)
    reverse_camera = models.BooleanField(default=False)
    labour = models.CharField(max_length=10, blank=True, null=True)
    

    # COMMENTS
    comments = models.TextField(blank=True)

    checked_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )

    checked_at = models.DateTimeField(auto_now=True)


    

def clean(self):
    # scheduled_datetime may not be set yet (admin form builds it later)
    if not self.scheduled_datetime:
        return

    start_time = datetime.time(8, 0)
    end_time = datetime.time(20, 0)

    job_time = self.scheduled_datetime.time()

    if not (start_time <= job_time <= end_time):
        raise ValidationError(
            "Job time must be between 08:00 AM and 08:00 PM"
        )

    if job_time.minute not in (0, 30):
        raise ValidationError(
            "Job time must be in 30-minute steps (e.g. 08:00, 08:30)"
        )

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    job = models.ForeignKey(
        'job',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    message = models.CharField(max_length=255)

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message


def __str__(self):
    return f"{self.job_type} | {self.scheduled_datetime} | {self.mechanic.username}"
