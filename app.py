import torch
print(torch.cuda.is_available())  # Should return True if CUDA is set up properly
print(torch.cuda.current_device())  # Get the current device ID
print(torch.cuda.get_device_name(torch.cuda.current_device()))  # Get the name of your GPU
