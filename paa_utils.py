import os
import subprocess
import tempfile
from PyQt5.QtWidgets import QFileDialog, QMessageBox

def save_paa(final_image, imagetopaa_path, parent=None):
    path, _ = QFileDialog.getSaveFileName(parent, 'Save image as PAA', '', 'PAA (*.paa)')
    if path:
        tmp_png = tempfile.mktemp(suffix='.png')
        final_image.save(tmp_png)
        exe = imagetopaa_path or 'ImageToPAA.exe'
        result = subprocess.run([exe, tmp_png, path], capture_output=True)
        if os.path.exists(tmp_png):
            os.remove(tmp_png)
        if result.returncode == 0:
            QMessageBox.information(parent, 'Saved', f'Image saved to {path} (PAA)')
        else:
            QMessageBox.warning(parent, 'Error', f'PAA save error: {result.stderr.decode("utf-8") or "PAA conversion error"}')
