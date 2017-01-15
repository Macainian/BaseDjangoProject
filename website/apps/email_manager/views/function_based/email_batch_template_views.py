import json

from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from website.apps.email_manager.models import EmailBatchTemplate
from website.apps.email_manager.utils.get_clean_ckeditor_html_code import get_clean_ckeditor_html_code


@csrf_exempt
def get_email_preview_view(request):
    unparsed_injected_html_code = request.POST.get("html_code", None)

    if unparsed_injected_html_code is None:
        return HttpResponse("<h1>Email failed to render: Missing html_code</h1>")

    if unparsed_injected_html_code == "":
        return HttpResponse("<h1>Email failed to render: Empty html_code</h1>")

    reset_url = settings.NON_PREFIXED_SITE_URL + reverse(
        "account_manager.password_reset_confirm", kwargs={"uuid": "234ABCDEF234234"}
    )

    context = {"request": request, "account": request.user.account, "reset_url": reset_url}
    final_html_code = get_clean_ckeditor_html_code(unparsed_injected_html_code, context)
    print(final_html_code)

    return HttpResponse(final_html_code)


@csrf_exempt
def get_email_batch_template_view(request, email_batch_template_id):
    if EmailBatchTemplate.objects.filter(id=email_batch_template_id).exists():
        email_batch_template = EmailBatchTemplate.objects.get(id=email_batch_template_id)

        out_data = {}
        out_data["email_batch_template_name"] = email_batch_template.name
        out_data["from_code"] = email_batch_template.from_code
        out_data["subject_code"] = email_batch_template.subject_code
        out_data["basic_message"] = email_batch_template.basic_message
        out_data["html_code"] = email_batch_template.html_code

        return HttpResponse(content=json.dumps(out_data))
    else:
        return HttpResponse(content="No EmailTemplate with id \"" + str(email_batch_template_id) + "\"", status=500)


@csrf_exempt
def save_email_batch_template_view(request, email_batch_template_id):
    email_batch_template_name = request.POST.get("email_batch_template_name", None)
    from_code = request.POST.get("from_code", None)
    subject_code = request.POST.get("subject_code", None)
    basic_message = request.POST.get("basic_message", None)
    html_code = request.POST.get("html_code", None)

    if not email_batch_template_name:
        return HttpResponse(content="email_batch_template_name is required", status=500)

    if not from_code:
        return HttpResponse(content="from_code is required", status=500)

    if not subject_code:
        return HttpResponse(content="subject_code is required", status=500)

    if not basic_message:
        return HttpResponse(content="basic_message is required", status=500)

    if not html_code:
        return HttpResponse(content="html_code is required", status=500)

    if email_batch_template_id == "new":
        EmailBatchTemplate.objects.create(
            name=email_batch_template_name, from_code=from_code, subject_code=subject_code,
            basic_message=basic_message, html_code=html_code, created_by=request.user.staff_member,
            updated_by=request.user.staff_member
        )
    else:
        if EmailBatchTemplate.objects.filter(id=email_batch_template_id).exists():
            email_batch_template = EmailBatchTemplate.objects.get(id=email_batch_template_id)
            email_batch_template.name = email_batch_template_name
            email_batch_template.from_code = from_code
            email_batch_template.subject_code = subject_code
            email_batch_template.basic_message = basic_message
            email_batch_template.html_code = html_code
            email_batch_template.updated_by = request.user.staff_member
            email_batch_template.save()
        else:
            return HttpResponse(content="No EmailTemplate with id \"" + str(email_batch_template_id) + "\"", status=500)

    return HttpResponse()


@csrf_exempt
def copy_email_batch_template_view(request, email_batch_template_id):
    new_email_batch_template_name = request.POST.get("new_email_batch_template_name", None)

    if not new_email_batch_template_name:
        return HttpResponse(content="new_email_batch_template_name is required", status=500)

    if EmailBatchTemplate.objects.filter(id=email_batch_template_id).exists():
        original_email_batch_template = EmailBatchTemplate.objects.get(id=email_batch_template_id)
        EmailBatchTemplate.objects.create(
            name=new_email_batch_template_name, from_code=original_email_batch_template.from_code,
            subject_code=original_email_batch_template.subject_code,
            basic_message=original_email_batch_template.basic_message,
            html_code=original_email_batch_template.html_code, created_by=request.user.staff_member,
            updated_by=request.user.staff_member
        )
    else:
        return HttpResponse(content="No EmailTemplate with id \"" + str(email_batch_template_id) + "\"", status=500)

    return HttpResponse()
