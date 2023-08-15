# URL configuration for predictionsite project.

# Import necessary modules
from django.contrib import admin
from django.urls import path
from predictapp import views  # Import views from the predictapp app
from django.conf.urls.static import static
from django.conf import settings

# Define the urlpatterns list to route URLs to views
urlpatterns = [
    path("admin/", admin.site.urls),  # Admin panel URL
    path("", views.index, name="index"),  # Default route to index view
    path('result/', views.RecentUploadedImageView.as_view(), name="results"),  # Route to result view
    path('image_list/', views.UploadedImageListView.as_view(), name='image_list'),  # Route to image list view
    # path('result/', views.checkout, name='result'),  # An example commented out route
]

# Append more URL patterns if needed
urlpatterns += [
    # ... additional URL patterns can be added here ...
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Serving static images from MEDIA_URL

# The above line appends the serving of static media files in development using Django's server.
# In production, you should use a proper web server to serve static files for better performance.
