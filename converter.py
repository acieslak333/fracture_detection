from genericpath import exists
import pydicom
import numpy as np
import os
import cv2
from tqdm import tqdm

DATA_FOLDER_NAME = 'train_data'
CONVERTED_FOLDER_NAME = 'converted_images'

class DicomFile():
    def __init__(self, path):
        self.load_path = path
        self.save_path, self.name = self.set_save_path()
        self.image = self.read_dicom_image_data()
    
    def __str__(self):
        return f"Image size: {self.image.shape}\nLoad path: {self.load_path} \nSave path: {os.path.join(self.save_path, self.name)}"

    def set_save_path(self):
        save_folder_name = CONVERTED_FOLDER_NAME
        truncated_path = self.load_path.split('\\')
        if len(truncated_path) == 1:
            truncated_path = self.load_path.split('/')
        name = truncated_path[-1]
        save_path = ''.join(truncated_path[1:-1])
        return os.path.join(save_folder_name, save_path), name

    def read_dicom_image_data(self):
        image = pydicom.dcmread(self.load_path)
        image = image.pixel_array
        return image
    
    def save_image(self):
        os.makedirs(self.save_path, exist_ok=True)
        file_name = self.name.replace('.dcm','.png')
        file_path = os.path.join(self.save_path, file_name)
        cv2.imwrite(file_path, self.image)


def list_all_dicom_files(path):
    dicom_folders_lists = [os.path.join(path, folder) for folder in os.listdir(path)]
    dicom_list = []
    print('Getting DICOM paths')
    for folder_list in tqdm(dicom_folders_lists):
        dicom_list.extend([os.path.join(folder_list, file) for file in os.listdir(folder_list)])
    
    print('Paths loaded')
    return dicom_list

def convert_images(images_paths):
    print('Converting DICOMS')
    for path in tqdm(images_paths):
        temp_dicom = DicomFile(path)
        temp_dicom.save_image()
    print('All converted!')

if __name__ == "__main__":
    dicom_files = list_all_dicom_files(DATA_FOLDER_NAME)
    convert_images(dicom_files)