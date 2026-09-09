from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def cesfam_view(request):
    return render(
        request,
        "cesfam/cesfam.html"
    )