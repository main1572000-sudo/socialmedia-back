from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    # نستخدم write_only=True حتى نطلب كلمة المرور عند التسجيل ولا نرجعها عند القراءة
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        # نستخدم set_password لتشفير كلمة المرور بشكل آمن قبل الحفظ
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user

class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    likes_count = serializers.SerializerMethodField()
    dislike_count = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ['id','author','title','category','content','created_at','likes_count','dislike_count']
        
    def get_likes_count(self, obj):
        return obj.likes.filter(value='LIKE').count()
    
    def get_dislike_count(self, obj):
        return obj.likes.filter(value='DISLIKE').count()