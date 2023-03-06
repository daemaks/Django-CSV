from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt

from . import services
from .forms import ColumnFormSet, DataSchemaForm, ModelColumnFormSet
from .models import Column, DataSchema


class CustomLoginView(LoginView):
    template_name = "users/login.html"
    redirect_authenticated_user = True
    success_url = "/"

    def get_success_url(self) -> str:
        return self.success_url

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["username"].widget.attrs.update(
            {"class": "form-control mb-3", "placeholder": "Username"}
        )
        form.fields["password"].widget.attrs.update(
            {"class": "form-control mb-3", "placeholder": "Password"}
        )
        return form


def root(request):
    return render(request, "base.html")


@login_required
def get_data_schemas(request):
    data_schemas = DataSchema.objects.filter(user=request.user)
    return render(
        request, "schemas/schemas_list.html", {"data_schemas": data_schemas}
    )


@login_required
def get_data_schema(request, pk):
    data_schema = DataSchema.objects.get(pk=pk)
    return render(
        request, "schemas/generate.html", {"data_schema": data_schema}
    )


@login_required
def create_schema(request):
    if request.method == "POST":
        schema_form = DataSchemaForm(request.POST)
        column_formset = ColumnFormSet(request.POST)
        if services.handle_create_schema_form_submission(
            request.user, schema_form, column_formset
        ):
            return redirect("schema_list")
    else:
        schema_form = DataSchemaForm()
        column_formset = ColumnFormSet()

    context = {
        "schema_form": schema_form,
        "column_formset": column_formset,
    }

    return render(request, "schemas/create.html", context)


@login_required
def update_schema(request, pk):
    schema = get_object_or_404(DataSchema, id=pk)
    queryset = Column.objects.filter(schema=schema)
    schema_form = DataSchemaForm(request.POST or None, instance=schema)
    column_formset = ModelColumnFormSet(
        request.POST or None, queryset=queryset
    )

    if request.method == "POST":
        if services.handle_update_schema_form_submission(
            schema_form, column_formset
        ):
            return redirect("schema_list")

    return render(
        request,
        "schemas/update.html",
        {
            "schema_form": schema_form,
            "column_formset": column_formset,
        },
    )


@login_required
def delete_schema(request, pk):
    schema = get_object_or_404(DataSchema, pk=pk)
    if request.method == "POST":
        schema.delete()
        return redirect("schema_list")
    return render(request, "schemas/delete.html", {"schema": schema})


@login_required
@csrf_exempt
def generate_data(request, pk):
    if request.method == "POST":
        # Get the number of records to generate
        num_records = int(request.POST.get("num_records"))

        # Get the data schema from the database
        schema = get_object_or_404(DataSchema, id=pk)
        columns = Column.objects.filter(schema=schema)

        # Generate the fake data
        rows = services.generate_fake_data(num_records, columns)

        # Create a CSV response with the generated data
        filename = schema.name.replace(" ", "-") + ".csv"
        response = services.create_csv_response(columns, rows, filename)

        # Save the CSV file to media root and get its URL
        url = services.save_csv_to_media(response, filename)

        return JsonResponse({"url": url, "filename": filename})
