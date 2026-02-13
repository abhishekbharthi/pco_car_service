from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from accounts.decorators import mechanic_required
from .models import Job, JobInspection
from django.utils import timezone

from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML

from django.contrib.auth.models import User
from .models import Notification


from django.http import JsonResponse




@login_required(login_url='/accounts/login/')
@mechanic_required
def mechanic_job_list(request):
    
    jobs = Job.objects.filter(mechanic=request.user)

    # ---- Filters ----
    status = request.GET.get('status')
    date = request.GET.get('date')

    # Default: NEW + HOLD
    if not status:
        jobs = jobs.filter(status__in=['NEW', 'HOLD'])
    else:
        jobs = jobs.filter(status=status)

    if date:
        jobs = jobs.filter(scheduled_datetime__date=date)
    else:
        today = timezone.localdate()
        jobs = jobs.filter(scheduled_datetime__date=today)

    jobs = jobs.order_by('scheduled_datetime')

    return render(request, 'jobs/mechanic_job_list.html', {
        'jobs': jobs,
        'selected_status': status,
        'selected_date': date,
    })

def mechanic_job_update(request, job_id):
    job = get_object_or_404(Job, id=job_id, mechanic=request.user)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        new_remark = request.POST.get('mechanic_remark', '').strip()

        if new_remark:
            timestamp = timezone.now().strftime("%d-%m-%Y %H:%M")
            entry = f"\n[{timestamp}] {request.user.username}: {new_remark}"

            job.mechanic_remark = (job.mechanic_remark or "") + entry

        job.status = new_status
        job.save()

        return redirect('mechanic_job_list')

    return render(request, 'jobs/mechanic_job_update.html', {'job': job})

@login_required(login_url='/accounts/login/')
@mechanic_required
def mechanic_checklist(request, job_id):

    job = get_object_or_404(Job, id=job_id, mechanic=request.user)

    inspection, created = JobInspection.objects.get_or_create(job=job)

    if request.method == "POST":

        # -------- SERVICE CHECKBOXES --------
        inspection.engine_oil_change = 'engine_oil_change' in request.POST
        inspection.oil_filter_change = 'oil_filter_change' in request.POST
        inspection.cabin_filter = 'cabin_filter' in request.POST
        inspection.air_filter = 'air_filter' in request.POST
        inspection.spark_plugs = 'spark_plugs' in request.POST
        inspection.engine_coolant = 'engine_coolant' in request.POST
        inspection.wipers = 'wipers' in request.POST
        inspection.battery = 'battery' in request.POST

        inspection.hybrid_filter = 'hybrid_filter' in request.POST
        inspection.antifreeze = 'antifreeze' in request.POST
        inspection.transmission_oil = 'transmission_oil' in request.POST
        inspection.washer_fluid = 'washer_fluid' in request.POST
        inspection.key_bettery = 'key_bettery' in request.POST



        # -------- BRAKES --------
        inspection.brake_pads_front = 'brake_pads_front' in request.POST
        inspection.brake_pads_rear = 'brake_pads_rear' in request.POST

        # -------- TYRES --------
        inspection.tyre_front_right = request.POST.get("tyre_front_right")
        inspection.tyre_front_left = request.POST.get("tyre_front_left")
        inspection.tyre_rear_right = request.POST.get("tyre_rear_right")
        inspection.tyre_rear_left = request.POST.get("tyre_rear_left")

        # -------- Light Bulbs ----------
        inspection.side_bulbs = 'side_bulbs' in request.POST
        inspection.h11_bulbs_left = 'h11_bulbs_left' in request.POST
        inspection.h11_bulbs_right = 'h11_bulbs_right' in request.POST
        inspection.hid_bulb_left = 'hid_bulb_left' in request.POST
        inspection.hid_bulb_right =  'hid_bulb_right' in request.POST


        #------- Others ----------
        inspection.break_disc_fr = 'break_disc_fr' in request.POST
        inspection.break_disc_re = 'break_disk_re' in request.POST
        inspection.shock_absorber_fr = 'shock_absorber_fr' in request.POST
        inspection.shock_absorber_re = 'shock_absorber_re' in request.POST
        inspection.linkage = 'linkage' in request.POST
        inspection.ball_joint = 'ball_joint' in request.POST
        inspection.seat_cover = 'seat_cover' in request.POST
        inspection.navigation = 'navigation' in request.POST
        inspection.accident_camera = 'accident_camera' in request.POST
        inspection.tracking_system = 'tracking_system' in request.POST
        inspection.reverse_camera = 'reverse_camera' in request.POST
        inspection.labour = request.POST.get("labour")

        # -------- COMMENTS --------
        inspection.comments = request.POST.get("comments")

        inspection.checked_by = request.user
        inspection.save()

        # ===============================
        # ✅ SMART ACTION HANDLING HERE
        # ===============================

        action = request.POST.get("action")


        # check if any checklist field has value
        checklist_filled = any([
            inspection.engine_oil_change,
            inspection.oil_filter_change,
            inspection.cabin_filter,
            inspection.air_filter,
            inspection.spark_plugs,
            inspection.engine_coolant,
            inspection.wipers,
            inspection.battery,
            inspection.hybrid_filter,
            inspection.antifreeze,
            inspection.transmission_oil,
            inspection.washer_fluid,
            inspection.key_bettery,

            inspection.brake_pads_front,
            inspection.brake_pads_rear,

            inspection.tyre_front_right,
            inspection.tyre_front_left,
            inspection.tyre_rear_right,
            inspection.tyre_rear_left,

            inspection.side_bulbs,
            inspection.h11_bulbs_left,
            inspection.h11_bulbs_right,
            inspection.hid_bulb_left,
            inspection.hid_bulb_right,

            inspection.break_disc_fr,
            inspection.break_disc_re,
            inspection.shock_absorber_fr,
            inspection.shock_absorber_re,
            inspection.linkage,
            inspection.ball_joint,
            inspection.seat_cover,
            inspection.navigation,
            inspection.accident_camera,
            inspection.tracking_system,
            inspection.reverse_camera,
        ])

        # update status automatically
        if checklist_filled and job.status == "NEW":
            job.status = "IN_PROCESS"

        if action == "complete":
            job.status = "COMPLETED"
            
        job.save()


        # get all admin users
        admins = User.objects.filter(
            userprofile__role__in=["ADMIN", "SUPER_ADMIN"]
        )

        for admin in admins:

            Notification.objects.create(
                user=admin,
                job=job,
                message=f"{job.appointment} updated by {request.user.get_full_name() or request.user.username}"
            )


        return redirect("mechanic_dashboard")

    return render(request, "jobs/mechanic_checklist.html", {
        "job": job,
        "inspection": inspection
    })

@login_required
def job_card_pdf(request, job_id):

    # STEP 1 — GET JOB FIRST
    job = get_object_or_404(Job, id=job_id)

    # STEP 2 — RENDER HTML TEMPLATE
    html_string = render_to_string(
        "jobs/job_card_pdf.html",
        {"job": job}
    )

    # STEP 3 — CONVERT TO PDF
    html = HTML(string=html_string)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f"inline; filename=job_{job.id}.pdf"

    html.write_pdf(response)

    return response 

@login_required
@login_required
def get_notifications(request):

    print("Logged user:", request.user)

    notifications = Notification.objects.filter(
        is_read=False
    ).order_by("-created_at")

    print("Found:", notifications)

    data = []

    for n in notifications:
        data.append({
            "id": n.id,
            "message": n.message
        })

    return JsonResponse({"notifications": data})


@login_required
def mark_notification_read(request, notification_id):

    Notification.objects.filter(
        id=notification_id,
        user=request.user
    ).update(is_read=True)

    return JsonResponse({"status": "ok"})
