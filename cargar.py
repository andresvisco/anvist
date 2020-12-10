from PIL import Image
import face_recognition
import pickle
import cv2
import numpy as np

class Cargar:
    def __init__(self, _filePath) -> None:
        self._filePath = _filePath
        self._imagen = None
        self._rotarCounter = 0
        self._imagenTemp = None
        
    def cargarImagen(self):
        if self._filePath is not None:
            self._imagen = Image.open(self._filePath) #cv2.imread(filePath.name)
            imagenShape = [self._imagen.width, self._imagen.height]
            if imagenShape[0] > 400:
                imagenShape[0] = int(imagenShape[0] * 0.75)
                imagenShape[1] = int(imagenShape[1] * 0.75)
            self._imagen = self._imagen.resize(imagenShape)
            self._imagenTemp = self._imagen
            return self._imagen
    
    def _predecir(self, imagen):
        self._imagen = imagen #.resize(width=400)
        encodingsPath = 'encodings.pickle'
        detection_method = "hog"
        data = pickle.loads(open(encodingsPath, "rb").read())
        # image = cv2.imread(self._imagen)
        rgb = cv2.cvtColor(np.array(self._imagen), cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(rgb, model=detection_method)
        encodings = face_recognition.face_encodings(rgb, boxes)
        names = []
        for encoding in encodings:
            matches = face_recognition.compare_faces(data["encodings"],encoding)
            name = "Unknown"
            if True in matches:
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}
                
                for i in matchedIdxs:
                    name = data["names"][i]
                    counts[name] = counts.get(name, 0) + 1
                name = max(counts, key=counts.get)
            names.append(name)
        
        for ((top, right, bottom, left), name) in zip(boxes, names):
            # print("A: " + str(type(self._imagen)))
            self._imagen = cv2.rectangle(np.array(self._imagen), (left, top), (right, bottom), (0, 255, 200), 1)
            # print("B: " + str(type(self._imagen)))
            y = top - 15 if top - 15 > 15 else top + 15
            self._imagen = cv2.putText(self._imagen, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        

        return self._imagen, names

    def _rotar(self):
        self._imagen = cv2.rotate(np.array(self._imagen), rotateCode=cv2.ROTATE_90_CLOCKWISE)
        self._rotarCounter += 90
        # return self._imagen, self._rotarCounter