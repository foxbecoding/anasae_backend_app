from django.contrib.auth.hashers import make_password, check_password
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSignUpSerializer(serializers.ModelSerializer):
    
    # Create hidden password field for password confirmation
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'password',
            'confirm_password',
            'date_of_birth',
            'agreed_to_toa'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        agreed_to_toa = attrs.get('agreed_to_toa')
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')


        # Check if passwords matches
        if password != confirm_password:
            msg = 'Passwords must match.'
            raise serializers.ValidationError({"error": msg}, code='authorization')
        
        #Check if user agreed to terms of agreement
        if not agreed_to_toa:
            msg = 'Please agree to our Terms.'
            raise serializers.ValidationError({"error": msg}, code='authorization')

        # Save User in database
        user = User(
            first_name = attrs.get('first_name'),
            last_name = attrs.get('last_name'),
            email = attrs.get('email').lower(),
            password = make_password(attrs.get('password')),
            agreed_to_toa = attrs.get('agreed_to_toa'), 
            date_of_birth = attrs.get('date_of_birth') 
        )

        user.save()

        attrs['user'] = user
        return attrs  

class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email',
            'password',
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'write_only': True},
        }

    email = serializers.CharField(
        label="Email",
        write_only=True
    )
    
    password = serializers.CharField(
        label="Password",
        # This will be used when the DRF browsable API is enabled
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        # Set username and password from attrs
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:

            # Find user with username/email and password combination
            user = self.authenticate(email, password)
    
            if not user:
                # If we don't have a regular user, raise a ValidationError
                msg = 'Access denied: Invalid authentication credentials.'
                raise serializers.ValidationError({'access_denied': msg}, code='authorization')
        else:
            msg = 'Both "email" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')

   
        # We have a valid user, put it in the serializer's validated_data.
        # It will be used in the view.
        attrs['user'] = user
        return attrs
    
    def authenticate(self, email, password):
        # Check if username or email exist in database
        # and check if password matches with user input
        if User.objects.filter(email=email.lower()):
            user = User.objects.get(email=email.lower())
            if user.is_producer: return None
            if user.is_staff: return None
            
            if check_password(password, user.password):
                return user
            else :
                return None
        else :
            return None
        
