from django.shortcuts import render,redirect
from .forms import UserRegistrationForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import AttendanceForm
from .models import Attendance, UserProfile
import face_recognition
from django.core.files.uploadedfile import SimpleUploadedFile
import base64
from io import BytesIO
from django.shortcuts import redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
import csv
from django.http import HttpResponse
# Create your views here.

def index(request):
    return render(request,'index.html')


def student_list(request):
    users = User.objects.all()

    return render(request,'student_list.html',{'users':users})

def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('student_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def attendance_records(request):
    # Get filter parameters from GET request
    status = request.GET.get('status', '')
    date = request.GET.get('date', '')
    username = request.GET.get('username', '')

    # Initialize the queryset for Attendance model
    attendance_records = Attendance.objects.all()

    # Apply filters if provided
    if status:
        attendance_records = attendance_records.filter(status=status)
    
    if date:
        attendance_records = attendance_records.filter(date=date)
    
    if username:
        attendance_records = attendance_records.filter(user__username__icontains=username)

    # Pass the filtered records to the template
    return render(request, 'attendance_records.html', {
        'records': attendance_records,
        'status': status,
        'date': date,
        'username': username,
    })



def export_attendance(request):
    # Create the HttpResponse object with the appropriate CSV header
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="attendance_records.csv"'

    # Write data to CSV
    writer = csv.writer(response)
    writer.writerow(['User', 'Date', 'Status'])  # Add headers
    attendance_records = Attendance.objects.all()

    for record in attendance_records:
        writer.writerow([record.user.username, record.date, record.status])

    return response



@staff_member_required
def mark_attendance_admin(request, record_id):
    if request.method == "POST":
        attendance_record = get_object_or_404(Attendance, id=record_id)
        new_status = request.POST.get('status')
        if new_status in ['Present', 'Absent']:
            attendance_record.status = new_status
            attendance_record.save()
    return redirect('attendance_records')

@login_required
def mark_attendance(request):
    if request.method == "POST":
        photo_data = request.POST.get('photo')
        if photo_data:
            # Decode the Base64 string
            format, imgstr = photo_data.split(';base64,')
            ext = format.split('/')[-1]
            image_data = base64.b64decode(imgstr)

            # Convert to an in-memory file
            image_file = BytesIO(image_data)
            uploaded_photo = SimpleUploadedFile("photo." + ext, image_file.read(), content_type="image/" + ext)

            try:
                # Face recognition process
                uploaded_image = face_recognition.load_image_file(uploaded_photo)
                uploaded_encoding = face_recognition.face_encodings(uploaded_image)[0]

                user_profile = UserProfile.objects.get(user=request.user)
                registered_image = face_recognition.load_image_file(user_profile.photo.path)
                registered_encoding = face_recognition.face_encodings(registered_image)[0]

                results = face_recognition.compare_faces([registered_encoding], uploaded_encoding)
                if results[0]:
                    Attendance.objects.create(user=request.user, status='Present')
                    return redirect('attendance_success')
                else:
                    Attendance.objects.create(user=request.user, status='Absent')
                    return redirect('attendance_failure')
            except Exception as e:
                print("Error in face recognition:", e)
                return redirect('attendance_failure')
        else:
            print("No photo received")
            return redirect('attendance_failure')
    else:
        return render(request, 'mark_attendance.html')