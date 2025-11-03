import flet as ft
import io, base64
from PIL import Image

# Import your backend modules
from modules.cleanscan import remove_sensitive_content
from modules.safeshare import generate_safe_preview
from modules.noiseguard import add_privacy_noise


def main(page: ft.Page):
    page.title = "🛡️ ImageShield Mobile"
    page.bgcolor = "#0d1117"
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"

    # App Header
    header = ft.Row(
        [
            ft.Image(src="assets/logo.png", width=50, height=50),
            ft.Text("ImageShield", size=26, weight=ft.FontWeight.BOLD),
        ],
        alignment="center",
    )

    # Tabs for modules
    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=400,
        indicator_color="#00C4FF",
        tabs=[
            ft.Tab(text="CleanScan", icon=ft.Icons.SEARCH),
            ft.Tab(text="SafeShare", icon=ft.Icons.LOCK),
            ft.Tab(text="NoiseGuard", icon=ft.Icons.GRID_VIEW),
        ],
        expand=1,
    )

    # Shared widgets
    file_picker = ft.FilePicker()
    page.overlay.append(file_picker)
    uploaded_img = ft.Image(width=300, height=250, fit=ft.ImageFit.CONTAIN)
    output_img = ft.Image(width=300, height=250, fit=ft.ImageFit.CONTAIN)
    run_btn = ft.ElevatedButton("▶ Run Module", color="white", bgcolor="#00C4FF", width=250)
    status_text = ft.Text("", size=16)

    # Upload handler
    def on_file_picked(e):
        if e.files:
            uploaded_img.src = e.files[0].path
            status_text.value = f"📷 Loaded: {e.files[0].name}"
            page.update()

    file_picker.on_result = on_file_picked
    upload_btn = ft.ElevatedButton("📤 Upload Image", on_click=lambda e: file_picker.pick_files(allow_multiple=False))

    # 🧠 Module runner
    def process(e):
        if not file_picker.result or not file_picker.result.files:
            page.snack_bar = ft.SnackBar(ft.Text("⚠️ Please upload an image first!"))
            page.snack_bar.open = True
            page.update()
            return

        file_path = file_picker.result.files[0].path
        img = Image.open(file_path)

        # Process based on selected tab
        if tabs.selected_index == 0:  # CleanScan
            out = remove_sensitive_content(img)
            status_text.value = "✅ CleanScan complete! Faces blurred."
        elif tabs.selected_index == 1:  # SafeShare
            out = generate_safe_preview(img)
            status_text.value = "✅ SafeShare done! Metadata stripped & watermark added."
        else:  # NoiseGuard
            out = add_privacy_noise(img)
            status_text.value = "✅ NoiseGuard applied! Privacy filter added."

        # Show processed image
        buf = io.BytesIO()
        out.save(buf, format="PNG")
        output_img.src_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")
        page.update()

    run_btn.on_click = process

    # Tab content layout
    def build_tab(title):
        return ft.Container(
            ft.Column(
                [
                    ft.Text(title, size=18),
                    upload_btn,
                    uploaded_img,
                    run_btn,
                    output_img,
                    status_text,
                ],
                alignment="center",
                horizontal_alignment="center",
                spacing=10,
            ),
            padding=20,
        )

    clean_tab = build_tab("🔍 CleanScan: Face Blur")
    safeshare_tab = build_tab("🔐 SafeShare: Watermark")
    noise_tab = build_tab("🧊 NoiseGuard: Filters")

    tab_views = ft.Container(
        ft.Tabs(
            selected_index=0,
            tabs=[
                ft.Tab(text="CleanScan", content=clean_tab),
                ft.Tab(text="SafeShare", content=safeshare_tab),
                ft.Tab(text="NoiseGuard", content=noise_tab),
            ],
            expand=1,
            animation_duration=500,
            indicator_color="#00C4FF",
        ),
        expand=True,
    )

    # Main layout
    layout = ft.Column(
        [header, ft.Divider(color="#222"), tab_views],
        alignment="center",
        horizontal_alignment="center",
        spacing=10,
    )

    page.add(layout)


ft.app(target=main)
