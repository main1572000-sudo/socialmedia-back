from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # جلب توكن access and refresh 
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # تجديد التوكن في حالة انتهائه تم ضبط ال اكسيس توكن على يوم واحد
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # طلب انشاء حساب الحقول المطلوبة اسم المستخدم والايميل والباسورد
    path('register/',views.RegisterView.as_view(),name='signup'),
    # لعرض ملف المستخدم بحيث يستطيع تعديل اسمه وايميله وباسورده 
    path('profile/me/',views.UserProfileView.as_view(),name='userprofile'),
    # وضع التوكن في البلاكليست لتسجيل الخروج 
    path('api/logout/', views.LogoutView.as_view(), name='auth_logout'),
    # الصفحة الرئيسية لعرض جميع المنشورات للجميع
    path('', views.PostGetView.as_view(), name='all_posts'),
    # انشاء بوست جديد بشرط ان يكون المستخدم مسجل الدخةل
    path('CreatePost/', views.PostCreateView.as_view(), name='create_post'),
    # تعديل او حذف بوست المستخدم بحيث لا يستطيع تعديل او حذف الا البوست الخاص به 
    path('editpost/<uuid:pk>/', views.PostDetailView.as_view(), name='edit_post'),
    # ارسال {"value":"LIKE"} or {"value":"DISLIKE"} على حسب ضغط المستخدم
    path('posts/<uuid:pk>/like/', views.ToggleLikeView.as_view(), name='toggle-like'),
    # عرض المنشورات التي قام المستخدم بانشائها 
    path('myposts/', views.MyPostsView.as_view(), name='my_posts'),
    # لعرض وإنشاء تعليق على منشور معين
    path('posts/<uuid:pk>/comments/', views.CommentListCreateView.as_view(), name='post-comments'),
    # لتعديل أو حذف تعليق معين بواسطة الـ ID الخاص بالتعليق
    path('comments/<int:pk>/', views.CommentDetailView.as_view(), name='comment-detail'),
]