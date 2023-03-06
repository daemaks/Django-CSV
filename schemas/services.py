import csv
import os

from django.conf import settings
from django.http import HttpResponse
from faker import Faker


def handle_create_schema_form_submission(user, schema_form, column_formset):
    if schema_form.is_valid() and column_formset.is_valid():
        schema = schema_form.save(commit=False)
        schema.user = user
        schema.save()
        for column_form in column_formset:
            column = column_form.save(commit=False)
            column.schema = schema
            column.save()
        return True
    return False


def handle_update_schema_form_submission(schema_form, column_formset):
    if schema_form.is_valid() and column_formset.is_valid():
        schema = schema_form.save()
        columns = column_formset.save(commit=False)
        for column in columns:
            column.schema = schema
            column.save()
        column_formset.save_m2m()
        return True
    return False


def generate_fake_data(num_records, columns):
    fake = Faker()
    rows = []
    for _ in range(num_records):
        row = []
        for column in columns:
            if column.type == "full_name":
                row.append(fake.name())
            elif column.type == "job":
                row.append(fake.job())
            elif column.type == "email":
                row.append(fake.email())
            elif column.type == "domain_name":
                row.append(fake.domain_name())
            elif column.type == "phone_number":
                row.append(fake.phone_number())
            elif column.type == "company_name":
                row.append(fake.company())
            elif column.type == "text":
                num_sentences = column.sentences
                row.append(fake.paragraph(nb_sentences=num_sentences))
            elif column.type == "integer":
                min_val = column.range_start
                max_val = column.range_end
                row.append(fake.random_int(min=min_val, max=max_val))
            elif column.type == "address":
                row.append(fake.address())
            elif column.type == "date":
                row.append(fake.date())
        rows.append(row)
    return rows


def create_csv_response(columns, rows, filename):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    writer = csv.writer(response)
    writer.writerow([column.name for column in columns])
    for row in rows:
        writer.writerow(row)
    return response


def save_csv_to_media(response, filename):
    media_path = os.path.join(settings.MEDIA_ROOT, filename)
    with open(media_path, "w") as f:
        f.write(response.content.decode())
    url = f"{settings.MEDIA_URL}{filename}"
    return url
