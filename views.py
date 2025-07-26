class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSignupSerializer

    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.get(email=request.data['email'])
        except User.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=400)

        if user.check_password(request.data['password']):
            has_teacher_application = TeacherApplication.objects.filter(user=user).exists()

            # Fetch user profile
            try:
                user_profile = user.profile  # Related name from OneToOneField
                serialized_profile = UserProfileSerializer(user_profile).data
            except UserProfile.DoesNotExist:
                serialized_profile = None  # Or return default empty profile if preferred

            refresh = RefreshToken.for_user(user)
            return Response({
                'profile': serialized_profile,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'email': user.email,
                'id': user.id,
                'has_teacher_application': has_teacher_application,
                # 'profile': serialized_profile,
               
            })
        else:
            return Response({"error": "Invalid credentials"}, status=400)
