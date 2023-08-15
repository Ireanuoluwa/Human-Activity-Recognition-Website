from django import forms

class ImageUploadForm(forms.Form):
    # Define a field for uploading images
    image = forms.ImageField()  # This creates an image upload field

