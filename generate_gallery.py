import os
from urllib.parse import quote

# --- CONFIGURATION ---
WALLPAPER_DIR = '.' 
IGNORE_FILES = {'README.md', 'generate_gallery.py', '.gitignore', '.git', 'LICENSE'}
EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
COLUMNS = 3
WIDTH = "300" 

def get_images(directory):
    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            if filename in IGNORE_FILES:
                continue
            ext = os.path.splitext(filename)[1].lower()
            if ext in EXTENSIONS:
                path = os.path.relpath(os.path.join(root, filename), directory)
                files.append(path)
    # Sort them so they don't jump around every time you run the script
    return sorted(files)

def generate_readme(images):
    readme_path = 'README.md'
    # ---------------------------------------------------------
    # 🔥 FIX: This must match the tag in your README.md
    # ---------------------------------------------------------
    marker = ""
    
    # 1. Read existing content safely
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
    else:
        content = f"# Wallpaper Collection\n\n{marker}\n"

    # 2. Check for the marker
    if marker not in content:
        print(f"⚠️  Marker '{marker}' not found! Appending it to the end.")
        content += f"\n\n{marker}\n"

    # 3. Split the file: Keep the header (index 0)
    try:
        header_content = content.split(marker)[0]
    except ValueError:
        print("❌ Error: Marker was empty. Hard-coding fallback.")
        header_content = content

    # 4. Build the new grid
    print(f"🔍 Found {len(images)} images. Building grid...")
    
    # We reconstruct the file starting with the header + the marker
    new_content = header_content + marker + "\n\n<table>\n"
    
    for i, img_path in enumerate(images):
        # Start row
        if i % COLUMNS == 0:
            new_content += "  <tr>\n"
        
        # HTML Encode paths (fix spaces/symbols)
        encoded_path = quote(img_path)
        name = os.path.basename(img_path)

        # Build Cell
        new_content += f'    <td align="center" valign="top">\n'
        new_content += f'      <a href="{encoded_path}">\n'
        new_content += f'        <img src="{encoded_path}" width="{WIDTH}" alt="{name}" style="border-radius:10px;" />\n'
        new_content += f'      </a>\n'
        new_content += f'      <br />\n'
        new_content += f'      <sub>{name}</sub>\n'
        new_content += f'    </td>\n'

        # End row
        if (i + 1) % COLUMNS == 0:
            new_content += "  </tr>\n"
    
    # Close final row if not complete
    if len(images) % COLUMNS != 0:
        new_content += "  </tr>\n"
        
    new_content += "</table>\n"

    # 5. Write it back
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print("✅ README.md successfully updated.")

if __name__ == "__main__":
    imgs = get_images(WALLPAPER_DIR)
    if imgs:
        generate_readme(imgs)
    else:
        print("❌ No images found in this directory.")
