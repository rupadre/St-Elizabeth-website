from django.shortcuts import render


def make_view(template, build_context):
    def view(request):
        return render(request, template, build_context())
    return view
