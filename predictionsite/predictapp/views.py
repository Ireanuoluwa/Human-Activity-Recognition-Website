# Import necessary modules and classes
from django.shortcuts import render, redirect
from django.conf import settings
from .forms import ImageUploadForm
import os
import torch
from PIL import Image
from torchvision.transforms import ToTensor
from .predict import get_predictions
from .models import UploadedImage
from django.views.generic import ListView

# Define a view function for handling image predictions
def predict(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Extract the uploaded image from the form
            image = form.cleaned_data['image']
            
            # Print the name and path of the uploaded image for debugging
            print(image.name)
            image_path = os.path.join(settings.MEDIA_ROOT, 'uploads', image.name)
            print(image_path)

            # Save the uploaded image
            with open(image_path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
            
            # Preprocess the image and get predictions
            predictions = get_predictions(image_path)

            # Save the uploaded image and predictions to the database
            uploaded_image = UploadedImage(image=image_path, predicted_class=predictions)
            uploaded_image.save()

            # Redirect to the results page
            return redirect('results')
    else:
        form = ImageUploadForm()

    # Render the index page with the upload form
    return render(request, 'predictapp/index.html', {'form': form})

# Define a view function for the index page
def index(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Call the predict function to handle prediction and redirection
            return predict(request)
    else:
        form = ImageUploadForm()

    # Render the index page with the upload form
    return render(request, 'predictapp/index.html', {'form': form})

# Define a class-based view for displaying the most recently uploaded image and its predictions
class RecentUploadedImageView(ListView):
    model = UploadedImage
    template_name = 'predictapp/result.html'
    context_object_name = 'uploaded_images'
    queryset = UploadedImage.objects.order_by('-id')[:1]  # Retrieve the most recent image

    def get_context_data(self, **kwargs):
        # Get the original context from the parent class
        context = super().get_context_data(**kwargs)

        # Mapping of predicted class labels to human-readable forms
        class_label_mapping = {
            'listening_to_music': 'Listening to music',
            'using_laptop': 'Using laptop',
            
        }

        # Iterate through each uploaded image in the context
        for uploaded_image in context['uploaded_images']:
            # Get the predicted class label for the current uploaded image
            predicted_class = uploaded_image.predicted_class
            
            # Map the predicted class label to its human-readable form using the mapping
            # If the label is not in the mapping, use the original label as is
            mapped_class = class_label_mapping.get(predicted_class, predicted_class)
            
            # Update the predicted class of the current uploaded image to the mapped value
            uploaded_image.predicted_class = mapped_class

        # Return the updated context with mapped predicted class labels
        return context

    
# Define a class-based view for listing all uploaded images
class UploadedImageListView(ListView):
    model = UploadedImage
    template_name = 'predictapp/image_list.html'
    context_object_name = 'uploaded_images'
