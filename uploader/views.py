import pandas as pd
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .forms import UploadFileForm
from .models import UploadedFile

def handle_uploaded_file(f):
    file_path = 'uploads/' + f.name
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return file_path

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file_path = handle_uploaded_file(request.FILES['file'])
            summary = generate_summary(file_path)
            send_summary_email(summary)
            return render(request, 'success.html', {'summary': summary})
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

def generate_summary(file_path):
    data = pd.read_csv(file_path)
    summary = data.describe().to_string()
    return summary

def send_summary_email(summary):
    send_mail(
        'Python Assignment - Your Name',
        summary,
        'from@example.com',
        ['tech@themedius.ai'],
        fail_silently=False,
    )
