import os
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv()

# ✅ Manually configure Cloudinary (in case Django settings aren't loaded)
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
)

# ✅ Check if Cloudinary API key is loading
print("Testing Cloudinary Upload...")
print("Cloudinary API Key:", cloudinary.config().api_key)  # Should NOT be None

try:
    response = cloudinary.uploader.upload("IMG_9822.jpg")  # Replace with an actual image path
    print("✅ Upload Successful!")
    print(response)
except Exception as e:
    print("❌ Cloudinary upload error:", e)