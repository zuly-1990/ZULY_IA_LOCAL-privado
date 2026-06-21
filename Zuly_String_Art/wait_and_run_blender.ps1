while (!(Test-Path "C:\Users\Admin\Desktop\ZULY_IA_LOCAL\Zuly_String_Art\string_art_result.png")) {
    Start-Sleep -Seconds 5
}
Write-Output "Image generated. Running Blender script..."
& "C:\Program Files\Blender Foundation\Blender 3.6\blender.exe" --background --python "C:\Users\Admin\Desktop\ZULY_IA_LOCAL\Zuly_String_Art\string_art_blender.py"
Write-Output "Blender generation complete."
