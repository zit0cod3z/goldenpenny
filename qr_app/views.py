from django.shortcuts import render, redirect
from .models import Attendee, Child
# from .serializers import UserSerializer
from django.db.models import Q
# from django.contrib.auth.hashers import make_password
from django.db import IntegrityError

# View to render the HTML template
def user_check_view(request):
	result = None
	attendee = None
	result_class = ""
	if request.method == "POST":
		name = request.POST.get('name')
		email = request.POST.get('email')
		phone_number = request.POST.get('phone_number')
		ticket_type = request.POST.get('ticket_type')  # This can also be from a dropdown in your template

		if ticket_type == 'family':
			child_names = request.POST.getlist('child_names')  # Assuming you pass a list of names

			for child_name in child_names:
				if child_name:  # Ensure the child name is not empty
					Child.objects.get_or_create(attendee=attendee, name=child_name)

		try:
			attendee = Attendee.objects.get( Q(name=name) | Q(email=email) | Q(phone_number=phone_number))
			result = "Attendee found!"
			result_class = "found"
		except Attendee.DoesNotExist:
			result = "Attendee not found. No records."
			result_class = "not-found"
	return render(request, 'qr_app/index.html', {'result': result, 'attendee': attendee, 'result_class': result_class})


def register_view(request):
	registration_success = False
	error_message = "" 
	if request.method == "POST":
		name = request.POST.get('name').strip()
		email = request.POST.get('email')
		phone_number = request.POST.get('phone_number')
		instagram_handle = request.POST.get('instagram_handle').strip()
		ticket_type = request.POST.get('ticket_type')
		additional_info = request.POST.get('additional_info', '').strip()
		number_of_children = int(request.POST.get('number_of_children', 0))

		if Attendee.objects.filter(name=name).exists():
			error_message = "This User is already registered."
		if Attendee.objects.filter(email=email).exists():
			error_message = "This Email is already registered."
		if Attendee.objects.filter(phone_number=phone_number).exists():
			error_message = "This phone number is already registered."
		else:
			attendee = Attendee(
	            name=name,
	            email=email,
	            phone_number=phone_number,
	            instagram_handle=instagram_handle,
                ticket_type=ticket_type,
	        )
			try:
				attendee.save()

				for i in range(number_of_children):
					child_name = request.POST.get(f'child_name_{i + 1}').strip()
					if child_name:  # Ensure the name is not empty
						Child.objects.create(attendee=attendee, name=child_name)

				request.session['registration_success'] = True
				return redirect('register_page')  # Redirect to the same page
			except IntegrityError:
				error_message = "An error occurred while registering. Please try again."

         # Clear the session variable if it exists
	if 'registration_success' in request.session:
		registration_success = request.session['registration_success']
		del request.session['registration_success']  # Clear the session variable
	else:
		registration_success = False

	return render(request, 'qr_app/register.html', {'registration_success': registration_success, 'error_message': error_message })