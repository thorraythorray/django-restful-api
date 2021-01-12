"""alphax URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import include, url
from image_ana import views as iamge_ana_views

urlpatterns = [
    # url('admin/', admin.site.urls),
    # url('depth_camera/', include('depth_camera.urls')),
    url('image_ana/', include('image_ana.urls')),
    url('test/', iamge_ana_views.ana_test),
    url('alipay/callback/', iamge_ana_views.alipay_callback),
    url('wxmall/', include('wxmall.urls'))
]

