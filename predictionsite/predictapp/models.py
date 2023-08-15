from django.db import models

# Create your models here.

class PredImage(models.Model):
    def __str__(self):
        return self.title  # Returns the title of the image (not defined in the model)

    image = models.ImageField(upload_to="C:/Users/moyin/OneDrive/Desktop/DEEP LEARNING/Human-Activity-Recognition-Project/predictionsite/predictionsite/pictures/uploads")
    # Field to store the uploaded image, with the specified upload path

class UploadedImage(models.Model):
    image = models.ImageField(upload_to='C:/Users/moyin/OneDrive/Desktop/DEEP LEARNING/Human-Activity-Recognition-Project/predictionsite/pictures/uploads', max_length=1000)
    # Field to store the uploaded image, with a specified upload path and maximum length

    predicted_class = models.CharField(max_length=500)
    # Field to store the predicted class for the uploaded image, with a maximum length of 500 characters
