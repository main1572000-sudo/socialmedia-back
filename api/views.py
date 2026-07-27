from rest_framework import generics ,permissions,status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .serializers import User,UserSerializer,PostSerializer,Post
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from .models import Post, PostLike

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    # إعادة المستخدم المسجل حالياً فقط
    def get_object(self):
        return self.request.user
    
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            # استخراج الـ refresh token من جسم الطلب
            refresh_token = request.data.get("refresh")
            
            if not refresh_token:
                return Response({"error": "الـ refresh token مطلوب."}, status=status.HTTP_400_BAD_REQUEST)

            # إدخال التوكن في القائمة السوداء (Blacklist)
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "تم تسجيل الخروج بنجاح."}, status=status.HTTP_205_RESET_CONTENT)

        except Exception as e:
            return Response({"error": "التوكن غير صالح أو منتهي الصلاحية بالفعل."}, status=status.HTTP_400_BAD_REQUEST)
#........................................................
# كل المنشورات 
class PostGetView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]

# انشاء منشور
class PostCreateView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # هنا يتم التعيين التلقائي!
        serializer.save(author=self.request.user)
# تعديل بوست معين
class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # تصفية المنشورات لتُرجع فقط المنشورات التي يملكها المستخدم المسجل حالياً
        return Post.objects.filter(author=self.request.user)
# بوستاتي : 
class MyPostsView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # تصفية المنشورات لتُرجع فقط المنشورات التي يملكها المستخدم المسجل حالياً
        return Post.objects.filter(author=self.request.user)
    


class ToggleLikeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        user = request.user
        
        # استلام القيمة من body، القيمة الافتراضية تكون LIKE
        like_type = request.data.get('value', 'LIKE').upper()

        # التأكد من أن القيمة المرسلة إما LIKE أو DISLIKE فقط
        if like_type not in ['LIKE', 'DISLIKE']:
            return Response(
                {'error': 'Invalid value. Allowed values are LIKE or DISLIKE.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # البحث عن تفاعل سابق لنفس المستخدم على هذا البوست
        like_obj = PostLike.objects.filter(user=user, post=post).first()

        if like_obj:
            if like_obj.value == like_type:
                # 1. إذا ضغط على نفس الزر مرة أخرى -> نلغي التفاعل (حذف)
                like_obj.delete()
                return Response({'message': 'Interaction removed'}, status=status.HTTP_200_OK)
            else:
                # 2. إذا غير رأيه (مثلاً من LIKE إلى DISLIKE) -> نحدث القيمة
                like_obj.value = like_type
                like_obj.save()
                return Response({'message': f'Changed to {like_type}'}, status=status.HTTP_200_OK)
        else:
            # 3. أول تفاعل للمستخدم على هذا البوست -> إنشاء جديد
            PostLike.objects.create(user=user, post=post, value=like_type)
            return Response({'message': f'Added {like_type}'}, status=status.HTTP_201_CREATED)