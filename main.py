import datetime
import os

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.lang import Builder

# Import your image processing modules
from modules.safeshare import add_watermark
from modules.cleanscan import blur_faces
from modules.noiseguard import apply_noiseguard

Builder.load_file("imageshield.kv")


class MainScreen(BoxLayout):
    selected_image = StringProperty('')  # Holds the current image path

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        os.makedirs("assets", exist_ok=True)
        self.audit_log = []   # ✅ audit log initialized here

    def on_file_selected(self, filechooser, selection):
        """Triggered when an image is selected from FileChooser."""
        if selection:
            self.selected_image = selection[0]
            self.ids.preview.source = self.selected_image
            self.ids.preview.reload()
            self.ids.summary.text = f"📷 Selected: {os.path.basename(self.selected_image)}"

    def run_selected_module(self):
        """Applies the selected ImageShield module."""
        module = self.ids.module_selector.text
        input_path = self.selected_image

        if not input_path:
            self.ids.summary.text = "⚠️ Please select an image first."
            return

        output_path = os.path.join("assets", "processed.jpg")
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # === CleanScan ===
        if module == "CleanScan":
            result_path, face_count = blur_faces(input_path, output_path)
            self.ids.preview.source = result_path
            self.ids.summary.text = f"✅ CleanScan: {face_count} face(s) blurred."
            entry = f"[{timestamp}] {module} → faces blurred: {face_count}"
            self.audit_log.append(entry)

        # === SafeShare ===
        elif module == "SafeShare":
            text = self.ids.watermark_text.text or "SAFE SHARE"
            opacity = int(self.ids.watermark_opacity.value)
            angle = int(self.ids.watermark_angle.value)
            position = self.ids.watermark_position.text

            result_path = add_watermark(
                input_path,
                output_path,
                text=text,
                opacity=opacity,
                angle=angle,
                position=position
            )
            self.ids.preview.source = result_path
            self.ids.summary.text = (
                f"✅ SafeShare: Watermark '{text}' added, opacity={opacity}, "
                f"angle={angle}, position={position}. Metadata removed."
            )
            entry = f"[{timestamp}] {module} → text='{text}', opacity={opacity}, angle={angle}, position={position}"
            self.audit_log.append(entry)

        # === NoiseGuard ===
        elif module == "NoiseGuard":
            mode = self.ids.noise_mode.text
            intensity = int(self.ids.noise_intensity.value)

            result_path, mode = apply_noiseguard(
                input_path,
                output_path,
                mode=mode,
                intensity=intensity
            )
            self.ids.preview.source = result_path
            self.ids.summary.text = f"✅ NoiseGuard: Applied {mode} filter with intensity {intensity}."
            entry = f"[{timestamp}] {module} → mode={mode}, intensity={intensity}"
            self.audit_log.append(entry)

        else:
            self.ids.summary.text = "⚠️ Please select a valid module."

        # Refresh preview image
        self.ids.preview.reload()

    def clear_history(self):
        """Clears image and summary panel."""
        self.selected_image = ''
        self.ids.preview.source = ''
        self.ids.summary.text = "Summary will appear here..."
        self.ids.module_selector.text = "Choose Module"

    def download_image(self):
        """Indicates saved image status."""
        if os.path.exists("assets/processed.jpg"):
            self.ids.summary.text += "\n📥 Saved to assets/processed.jpg"
        else:
            self.ids.summary.text += "\n⚠️ No processed image found."

    def on_module_selected(self, spinner, text):
        """Show/hide dynamic controls based on module."""
        # Hide all controls
        for cid in [
            "watermark_text", "watermark_opacity", "watermark_angle",
            "watermark_position", "noise_mode", "noise_intensity"
        ]:
            self.ids[cid].opacity = 0

        if text == "SafeShare":
            for cid in ["watermark_text", "watermark_opacity", "watermark_angle", "watermark_position"]:
                self.ids[cid].opacity = 1

        elif text == "NoiseGuard":
            for cid in ["noise_mode", "noise_intensity"]:
                self.ids[cid].opacity = 1

    def show_audit_log(self):
        """Displays last 5 log entries in summary panel."""
        if not self.audit_log:
            self.ids.summary.text = "📜 No actions logged yet."
        else:
            self.ids.summary.text = "\n".join(self.audit_log[-5:])

    def export_audit_log(self):
        """Exports full audit log to file."""
        with open("assets/audit_log.txt", "w") as f:
            f.write("\n".join(self.audit_log))
        self.ids.summary.text += "\n📂 Audit log saved to assets/audit_log.txt"


class ImageShieldApp(App):
    def build(self):
        self.title = "🛡️ ImageShield"
        return MainScreen()


if __name__ == "__main__":
    ImageShieldApp().run()