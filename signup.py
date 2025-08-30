class SignUpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        email = data.get('email')
        password = data.get('password')

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            return Response({"error": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Validate the password
            validate_password(password)

            # Create user (email also used as username)
            user = User.objects.create_user(username=email, email=email, password=password, is_active=False)

            # ✅ Don't forget to return success here!
            return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)

        except Exception as e:
            print("Signup error:", str(e))  # Debug log
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

