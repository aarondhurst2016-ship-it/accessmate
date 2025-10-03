# Live camera and OCR for Kivy (mobile/desktop)
from kivy.uix.boxlayout import BoxLayout # pyright: ignore[reportMissingImports]
from kivy.uix.button import Button # pyright: ignore[reportMissingImports]
from kivy.uix.label import Label # pyright: ignore[reportMissingImports]
from kivy.uix.camera import Camera # pyright: ignore[reportMissingImports]
import pytesseract
from PIL import Image
import io

class CameraScreen(BoxLayout):
    def recognize_faces_cloud(self, instance):
        try:
            import boto3
            from speech import speak
            import base64
            import os
            texture = self.camera.texture
            if not texture:
                self.result_label.text = "No camera image available."
                return
            img_data = texture.pixels
            size = texture.size
            pil_img = Image.frombytes(mode='RGBA', size=size, data=img_data)
            pil_img = pil_img.convert('RGB')
            # Convert image to bytes
            buf = io.BytesIO()
            pil_img.save(buf, format='JPEG')
            image_bytes = buf.getvalue()
            # AWS credentials (set your own)
            aws_access_key = os.environ.get('AWS_ACCESS_KEY_ID', 'YOUR_ACCESS_KEY')
            aws_secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY', 'YOUR_SECRET_KEY')
            region = os.environ.get('AWS_REGION', 'us-east-1')
            client = boto3.client('rekognition', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=region)
            response = client.detect_faces(Image={'Bytes': image_bytes}, Attributes=['ALL'])
            # For identification, use search_faces_by_image with a Rekognition collection
            # Example: response = client.search_faces_by_image(CollectionId='your_collection', Image={'Bytes': image_bytes})
            names = []
            for face_detail in response.get('FaceDetails', []):
                # If using search_faces_by_image, get name from face match
                names.append('Person')
            if names:
                self.result_label.text = f"AWS Rekognition: {', '.join(names)}"
                speak(f"I see: {', '.join(names)}")
            else:
                self.result_label.text = "No faces recognized by AWS Rekognition."
                speak("No faces recognized.")
        except Exception as e:
            self.result_label.text = f"AWS Rekognition error: {str(e)}"
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.camera = Camera(play=True)
        self.add_widget(self.camera)
        self.ocr_btn = Button(text="Read Text from Camera")
        self.ocr_btn.bind(on_press=self.read_text)
        self.add_widget(self.ocr_btn)
        self.face_btn = Button(text="Recognize Faces (Local)")
        self.face_btn.bind(on_press=self.recognize_faces)
        self.add_widget(self.face_btn)
        self.cloud_face_btn = Button(text="Recognize Faces (Cloud)")
        self.cloud_face_btn.bind(on_press=self.recognize_faces_cloud)
        self.add_widget(self.cloud_face_btn)
        self.result_label = Label(text="OCR/Face result will appear here.")
        self.add_widget(self.result_label)
    def read_text(self, instance):
        # Capture image from camera
        texture = self.camera.texture
        if texture:
            img_data = texture.pixels
            size = texture.size
            pil_img = Image.frombytes(mode='RGBA', size=size, data=img_data)
            pil_img = pil_img.convert('L')
            text = pytesseract.image_to_string(pil_img)
            self.result_label.text = f"Detected text: {text}"

    def recognize_faces(self, instance):
        try:
            import face_recognition  # pyright: ignore[reportMissingImports]
            from speech import speak
            texture = self.camera.texture
            if not texture:
                self.result_label.text = "No camera image available."
                return
            img_data = texture.pixels
            size = texture.size
            pil_img = Image.frombytes(mode='RGBA', size=size, data=img_data)
            pil_img = pil_img.convert('RGB')
            img_array = face_recognition.load_image_file(io.BytesIO(pil_img.tobytes()))
            # Load known faces (simple demo: load from 'known_faces/' folder)
            import os
            known_face_encodings = []
            known_face_names = []
            faces_dir = os.path.join(os.getcwd(), 'known_faces')
            if os.path.exists(faces_dir):
                for fname in os.listdir(faces_dir):
                    if fname.lower().endswith(('.jpg', '.png')):
                        img_path = os.path.join(faces_dir, fname)
                        img = face_recognition.load_image_file(img_path)
                        encodings = face_recognition.face_encodings(img)
                        if encodings:
                            known_face_encodings.append(encodings[0])
                            known_face_names.append(os.path.splitext(fname)[0])
            # Detect faces in camera image
            face_locations = face_recognition.face_locations(img_array)
            face_encodings = face_recognition.face_encodings(img_array, face_locations)
            names = []
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]
                names.append(name)
            if names:
                self.result_label.text = f"Recognized: {', '.join(names)}"
                speak(f"I see: {', '.join(names)}")
            else:
                self.result_label.text = "No faces recognized."
                speak("No faces recognized.")
        except Exception as e:
            self.result_label.text = f"Face recognition error: {str(e)}"