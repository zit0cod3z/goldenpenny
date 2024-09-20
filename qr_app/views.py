from django.shortcuts import render
from .models import User
# from .serializers import UserSerializer
from django.db.models import Q

# View to render the HTML template
def user_check_view(request):
	result = None
	user = None
	result_class = ""
	if request.method == "POST":
		name = request.POST.get('name')
		email = request.POST.get('email')
		phone_number = request.POST.get('phone_number')

		try:
			user = User.objects.get( Q(name=name) | Q(email=email) | Q(phone_number=phone_number)
				)
			result = "User found!"
			result_class = "found"
		except User.DoesNotExist:
			result = "User not found. No records."
			result_class = "not-found"
	return render(request, 'qr_app/index.html', {'result': result, 'user': user, 'result_class': result_class})

# class UserCheckView(APIView):
#     def get(self, request):
#         name = request.query_params.get('name')
#         email = request.query_params.get('email')
#         phone_number = request.query_params.get('phone_number')

#         try:
#             user = User.objects.get(
#                 Q(name=name) | Q(email=email) | Q(phone_number=phone_number)
#             )
#             serializer = UserSerializer(user)
#             return Response({"message": "User found!", "user": serializer.data}, status=status.HTTP_200_OK)
#         except User.DoesNotExist:
#             return Response({"message": "User not found. No records."}, status=status.HTTP_404_NOT_FOUND)