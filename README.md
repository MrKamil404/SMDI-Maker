# SMDI Maker (PyQt)

A simple tool for creating SMDI textures for DayZ/Arma (and other games using the SMDI format).

## Features
- Load Metalic/Specular and Roughness/Glossiness textures
- Adjust brightness, contrast, and saturation for both channels
- Invert roughness channel with one click
- Set Specular Level and Power (as per Bohemia Interactive wiki)
- Live preview of Metalic, Roughness, and final SMDI in separate windows
- Save the final SMDI as PNG or PAA (using ImageToPAA.exe from DayZ Tools)
- Set custom path to ImageToPAA.exe

## How to use
1. **Load textures**: Click 'Load...' next to 'Metalic/Specular texture' and 'Roughness/Glossiness texture' to load your source images.
2. **Adjust parameters**: Use the sliders to change brightness, contrast, and saturation for each channel. You can also invert the roughness channel.
3. **Specular settings**: Set Specular Level and Power for the green channel (see BI wiki for details).
4. **Preview**: See the effect in real time in the preview windows.
5. **Set ImageToPAA path**: Click 'Set path to ImageToPAA.exe' and select the executable from DayZ Tools (required for PAA export).
6. **Save**: Use 'Save final SMDI as PAA' to export the result as a .paa file, or use the standard save to export as PNG or PAA.

## Options
- **Brightness, Contrast, Saturation**: Adjust for both Metalic and Roughness channels independently.
- **Invert Roughness Colors**: Inverts the roughness channel (useful for some workflows).
- **Specular Level/Power**: Sets the green channel bits as per SMDI format (see https://community.bistudio.com/wiki/Arma_3:_Super_Material_Map for details).
- **Set path to ImageToPAA.exe**: Allows you to use a custom location for the DayZ Tools converter.

## Building and Running
1. Install Python 3.8+.
2. Install dependencies:
   ```sh
   pip install PyQt5 Pillow numpy matplotlib
   ```
3. (Optional, for PAA export) Download and install DayZ Tools, and locate ImageToPAA.exe.
4. Run the app:
   ```sh
   python smdi_maker.py
   ```

## Notes
- For PAA export, ImageToPAA.exe must be available and set in the app.
- The tool does not require compilation, just run with Python.
- All previews are live and non-destructive.

---

**Author:** YourName
