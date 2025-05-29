import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSlider, QFileDialog,
    QMessageBox, QGroupBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage
from image_utils import apply_enhancements, invert_image
from widgets import ImageView
from paa_utils import save_paa
from PIL import Image
import numpy as np

class SMDIMakerQt(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('SMDI Maker (PyQt)')
        self.resize(1100, 700)
        self.metallic_img = None
        self.roughness_img = None
        self.final_image = None
        self.imagetopaa_path = ''
        self.init_ui()

    def make_slider(self, minv, maxv, val, label, layout):
        hbox = QHBoxLayout()
        lbl = QLabel(label)
        hbox.addWidget(lbl)
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(minv)
        slider.setMaximum(maxv)
        slider.setValue(val)
        hbox.addWidget(slider)
        value_label = QLabel(str(val))
        hbox.addWidget(value_label)
        layout.addLayout(hbox)
        # Aktualizuj wartość na bieżąco
        def update_value_label():
            value_label.setText(str(slider.value()))
        slider.valueChanged.connect(update_value_label)
        return slider

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        control_layout = QVBoxLayout()
        main_layout.addLayout(control_layout, 0)

        # --- File loading section ---
        file_groupbox = QGroupBox('File loading')
        file_group = QVBoxLayout()
        file_group.addWidget(QLabel('Metalic/Specular texture'))
        btn_metallic = QPushButton('Load...')
        btn_metallic.clicked.connect(self.load_metallic)
        file_group.addWidget(btn_metallic)
        file_group.addWidget(QLabel('Roughness/Glossiness texture'))
        btn_roughness = QPushButton('Load...')
        btn_roughness.clicked.connect(self.load_roughness)
        file_group.addWidget(btn_roughness)
        file_groupbox.setLayout(file_group)
        control_layout.addWidget(file_groupbox)

        # --- Metalic/Specular section ---
        metalic_groupbox = QGroupBox('Metalic/Specular options')
        metalic_group = QVBoxLayout()
        self.metallic_brightness = self.make_slider(20, 200, 100, 'Brightness', metalic_group)
        self.metallic_saturation = self.make_slider(0, 200, 100, 'Saturation', metalic_group)
        self.metallic_contrast = self.make_slider(20, 200, 100, 'Contrast', metalic_group)
        metalic_groupbox.setLayout(metalic_group)
        control_layout.addWidget(metalic_groupbox)

        # --- Roughness/Glossiness section ---
        roughness_groupbox = QGroupBox('Roughness/Glossiness options')
        roughness_group = QVBoxLayout()
        self.roughness_brightness = self.make_slider(20, 200, 100, 'Brightness', roughness_group)
        self.roughness_saturation = self.make_slider(0, 200, 100, 'Saturation', roughness_group)
        self.roughness_contrast = self.make_slider(20, 200, 100, 'Contrast', roughness_group)
        btn_invert_rough = QPushButton('Invert Roughness Colors')
        btn_invert_rough.clicked.connect(self.invert_roughness)
        roughness_group.addWidget(btn_invert_rough)
        roughness_groupbox.setLayout(roughness_group)
        control_layout.addWidget(roughness_groupbox)

        # --- Specular section ---
        specular_groupbox = QGroupBox('Specular')
        specular_group = QVBoxLayout()
        self.specular_level = self.make_slider(0, 15, 8, 'Specular Level', specular_group)
        self.specular_power = self.make_slider(0, 15, 8, 'Specular Power', specular_group)
        self.specular_level.sliderReleased.connect(self.update_preview)
        self.specular_power.sliderReleased.connect(self.update_preview)
        specular_groupbox.setLayout(specular_group)
        control_layout.addWidget(specular_groupbox)

        # --- Tools section ---
        tools_groupbox = QGroupBox('Tools')
        tools_group = QVBoxLayout()
        btn_set_imagetopaa = QPushButton('Set path to ImageToPAA.exe')
        btn_set_imagetopaa.clicked.connect(self.set_imagetopaa_path)
        tools_group.addWidget(btn_set_imagetopaa)
        btn_save_paa = QPushButton('Save final SMDI as PAA')
        btn_save_paa.clicked.connect(self.save_final_paa)
        tools_group.addWidget(btn_save_paa)
        tools_groupbox.setLayout(tools_group)
        control_layout.addWidget(tools_groupbox)

        # --- Previews ---
        preview_layout = QHBoxLayout()
        vbox_met = QVBoxLayout()
        vbox_met.addWidget(QLabel('Metalic/Specular'))
        self.metallic_view = ImageView()
        vbox_met.addWidget(self.metallic_view)
        preview_layout.addLayout(vbox_met)
        vbox_rough = QVBoxLayout()
        vbox_rough.addWidget(QLabel('Roughness/Glossiness'))
        self.roughness_view = ImageView()
        vbox_rough.addWidget(self.roughness_view)
        preview_layout.addLayout(vbox_rough)
        vbox_final = QVBoxLayout()
        vbox_final.addWidget(QLabel('SMDI'))
        self.final_view = ImageView()
        vbox_final.addWidget(self.final_view)
        preview_layout.addLayout(vbox_final)
        main_layout.addLayout(preview_layout, 1)

        # Sliders update preview only on release
        for slider in [self.metallic_brightness, self.metallic_saturation, self.metallic_contrast,
                       self.roughness_brightness, self.roughness_saturation, self.roughness_contrast]:
            slider.sliderReleased.connect(self.update_preview)

    def load_metallic(self):
        path, _ = QFileDialog.getOpenFileName(self, 'Load Metalic/Specular', '', 'Images (*.png *.jpg *.jpeg *.bmp)')
        if path:
            self.metallic_img = Image.open(path).convert('L')
            self.update_preview()

    def load_roughness(self):
        path, _ = QFileDialog.getOpenFileName(self, 'Load Roughness/Glossiness', '', 'Images (*.png *.jpg *.jpeg *.bmp)')
        if path:
            self.roughness_img = Image.open(path).convert('L')
            self.update_preview()

    def invert_roughness(self):
        if self.roughness_img is not None:
            self.roughness_img = invert_image(self.roughness_img)
            self.update_preview()

    def set_imagetopaa_path(self):
        path, _ = QFileDialog.getOpenFileName(self, 'Select ImageToPAA.exe', '', 'ImageToPAA.exe (ImageToPAA.exe)')
        if path:
            self.imagetopaa_path = path
            QMessageBox.information(self, 'Set', f'Path to ImageToPAA.exe set to:\n{path}')

    def update_preview(self):
        if self.metallic_img is None or self.roughness_img is None:
            self.metallic_view.set_image(QImage(256, 256, QImage.Format_RGB32))
            self.roughness_view.set_image(QImage(256, 256, QImage.Format_RGB32))
            self.final_view.set_image(QImage(256, 256, QImage.Format_RGB32))
            return
        size = self.metallic_img.size
        if self.roughness_img.size != size:
            rough = self.roughness_img.resize(size, Image.BILINEAR)
        else:
            rough = self.roughness_img
        if self.metallic_img.size != size:
            metallic = self.metallic_img.resize(size, Image.BILINEAR)
        else:
            metallic = self.metallic_img
        # Metalic/Specular processing
        met = apply_enhancements(
            metallic,
            self.metallic_brightness.value()/100.0,
            self.metallic_saturation.value()/100.0,
            self.metallic_contrast.value()/100.0
        )
        met_arr = np.array(met, dtype=np.uint8)
        level = self.specular_level.value() & 0x0F
        power = self.specular_power.value() & 0x0F
        met_scaled = ((met_arr / 255.0) * 15 * (level / 15.0)).astype(np.uint8)
        g_arr = ((met_scaled.astype(np.uint8) << 4) | power).astype(np.uint8)
        g = Image.fromarray(g_arr, mode='L')
        # Roughness/Glossiness processing
        rough = apply_enhancements(
            rough,
            self.roughness_brightness.value()/100.0,
            self.roughness_saturation.value()/100.0,
            self.roughness_contrast.value()/100.0
        )
        r = Image.new('L', size, 255)
        b = Image.fromarray(255 - np.array(rough))
        final = Image.merge('RGB', (r, g, b))
        self.final_image = final
        # Previews
        met_rgb = met.convert('RGB')
        arr = np.array(met_rgb)
        h, w, ch = arr.shape
        bytes_per_line = ch * w
        qimg = QImage(arr.data, w, h, bytes_per_line, QImage.Format_RGB888)
        self.metallic_view.set_image(qimg.copy())
        rough_rgb = rough.convert('RGB')
        arr2 = np.array(rough_rgb)
        h2, w2, ch2 = arr2.shape
        bytes_per_line2 = ch2 * w2
        qimg2 = QImage(arr2.data, w2, h2, bytes_per_line2, QImage.Format_RGB888)
        self.roughness_view.set_image(qimg2.copy())
        arr3 = np.array(final)
        h3, w3, ch3 = arr3.shape
        bytes_per_line3 = ch3 * w3
        qimg3 = QImage(arr3.data, w3, h3, bytes_per_line3, QImage.Format_RGB888)
        self.final_view.set_image(qimg3.copy())

    def save_final(self):
        if self.final_image is not None:
            path, _ = QFileDialog.getSaveFileName(self, 'Save image', '', 'PNG (*.png);;PAA (*.paa)')
            if path:
                ext = os.path.splitext(path)[1].lower()
                if ext == '.paa':
                    try:
                        save_paa(self.final_image, self.imagetopaa_path, self)
                    except Exception as e:
                        QMessageBox.warning(self, 'Error', f'PAA save error: {e}')
                else:
                    self.final_image.save(path)
                    QMessageBox.information(self, 'Saved', f'Image saved to {path}')
        else:
            QMessageBox.warning(self, 'No image', 'First load and process textures!')

    def save_final_paa(self):
        if self.final_image is not None:
            save_paa(self.final_image, self.imagetopaa_path, self)
        else:
            QMessageBox.warning(self, 'No image', 'First load and process textures!')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = SMDIMakerQt()
    win.show()
    sys.exit(app.exec_())
