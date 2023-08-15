import torch
from torchvision.transforms import ToTensor, Resize
import torchvision.transforms as transforms
from torchvision import datasets
import torchvision
from PIL import Image
import os
import pickle

# Get the directory of the current script
current_directory = os.path.dirname(os.path.abspath(__file__))



model_path = os.path.join(current_directory, 'model.pkl')

hardetection_path = os.path.dirname(os.path.dirname(current_directory))
new_train_path = os.path.join(hardetection_path, 'hardetection/new_train') # new_train directory

# Load the pre-trained model
with open(model_path, 'rb') as f:
    model = pickle.load(f)

device = torch.device("cuda")


model.eval()




# Define transformations for preprocessing the input image
transform = transforms.Compose([
    transforms.Resize((512, 512)),  # Resize images to the input size of the model (224)
    transforms.ToTensor(),           # Convert images to tensors
])

# Load training data to obtain class names
train_data = datasets.ImageFolder(root= new_train_path,
                                  transform=transform,
                                  target_transform=None)
class_names = train_data.classes

def get_predictions(image_path):
    # Preprocess the image
    custom_image = torchvision.io.read_image(str(image_path)).type(torch.float32)
    custom_image = custom_image / 255.
    custom_image_transform = transforms.Compose([transforms.Resize((512, 512), antialias=True)])
    custom_image_transformed = custom_image_transform(custom_image)
    
    # Ensure the model is in evaluation mode
    model.eval()
    
    with torch.inference_mode():
        
        # Make a prediction on the image with an extra dimension
        custom_image_pred = model(custom_image_transformed.unsqueeze(dim=0).to(device))
        custom_image_pred_probs = torch.softmax(custom_image_pred, dim=1)
        custom_image_pred_label = torch.argmax(custom_image_pred_probs, dim=1)
        custom_image_pred_class = class_names[custom_image_pred_label.cpu()]
        predictions = custom_image_pred_class

    return predictions

