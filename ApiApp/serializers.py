from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

# Serailizer for Registeration

class RegisterationSerializer(serializers.ModelSerializer):
    role_choice = (
        ('super-admin', 'super-admin'),
        ('teacher', 'teacher'),
        ('student', 'student')
    )
    role = serializers.ChoiceField(choices=role_choice)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True) 

    class Meta:
        model = User
        fields = ['email', 'username', 'password','password2', 'role', 'groups']
        extra_kwargs = {'password': {'write_only': True}}

    # For Password Verification
    def save(self):   
        user_acc = User(email=self.validated_data['email'],username=self.validated_data['username'],)
        role = self.validated_data['role']
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Password didn\'t match '})
        user_acc.set_password(password)
        user_acc.save()
        group = Group.objects.get(name=role)
        user_acc.groups.add(group)
        return user_acc


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'groups']
   

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
   

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']
   


class TeacherAddSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    def save(self):   # For Password Verification
        user_acc = User(email=self.validated_data['email'],username=self.validated_data['username'],)
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Password didn\'t match '})
        user_acc.set_password(password)
        user_acc.save()
        # So that Teacher can only add students list
        group = Group.objects.get(name='student')
        user_acc.groups.add(group)
        return user_acc
