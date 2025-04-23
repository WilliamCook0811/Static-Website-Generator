
#This project is a Static Website Generator with a GUI built using Tkinter. 
#It allows users to create custom HTML and CSS files with themes, additional content, and preview functionality.

import os
import tkinter as tk
from tkinter import messagebox, filedialog
import tempfile
import webbrowser




# Function to create the HTML and CSS files
def create_html_file(filename, title, heading, paragraph, css_filename, preview=False):
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Ask for save location if the option is checked
    if save_location_var.get():
        save_dir = filedialog.askdirectory(title="Select Save Location")
        if not save_dir: # If no directory is selected, use the script directory
            return
        script_dir = save_dir

    # Create full paths for the HTML and CSS files
    html_path = os.path.join(script_dir, filename)
    css_path = os.path.join(script_dir, css_filename)

    # Collect content from all additional content boxes
    additional_content_html = ""
    for i, (content_type, content_data) in enumerate(additional_content_boxes):
        if content_type == "paragraph":
            text = content_data.get("1.0", "end-1c").strip()
            text = text.replace('\n', '<br>')  # Convert newlines to line breaks
            if text:
                additional_content_html += f'<div class="additional-content" id="additional-{i}">\n<p>{text}</p>\n</div>\n'
        
        elif content_type == "image":
            alt = content_data["alt"].get().strip()
            src_path = content_data["path_var"].get().strip()

            if src_path and os.path.exists(src_path):
                image_filename = os.path.basename(src_path)
                dest_image_path = os.path.join(script_dir, image_filename)
                
                try:
                    if src_path != dest_image_path:
                        with open(src_path, "rb") as src_file:
                            with open(dest_image_path, "wb") as dest_file:
                                dest_file.write(src_file.read())
                except Exception as e:
                    print(f"Error copying image: {e}")
                    continue

                additional_content_html += f'<div class="additional-content" id="additional-{i}">\n<div class="image-container"><img src="{image_filename}" alt="{alt}"></div>\n</div>\n'

        
        elif content_type == "video":
            video_url = content_data["url"].get().strip()
            if video_url:
                #YouTube video ID
                video_id = None
                if "youtube.com/watch?v=" in video_url:
                    video_id = video_url.split("youtube.com/watch?v=")[1].split("&")[0]
                elif "youtu.be/" in video_url:
                    video_id = video_url.split("youtu.be/")[1].split("?")[0]
                
                if video_id:
                    embed_code = f'<div class="video-container"><iframe width="560" height="315" src="https://www.youtube.com/embed/{video_id}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe></div>'
                    additional_content_html += f'<div class="additional-content" id="additional-{i}">\n{embed_code}\n</div>\n'
    # -------------------------------------------------------------------------

    # HTML content
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="{css_filename}">  
</head>
<body>
    <div class="container">
        {f'<div class="banner-container"><img src="{banner_url_entry.get()}" class="banner-image" alt="Banner image"><h1 class="banner-title">{banner_title_entry.get()}</h1></div>' if banner_url_entry.get() else ''}
        
        <header>
            {'' if banner_url_entry.get() else f'<h1>{heading}</h1>'}
            {f'<p class="subheading">{subheading_entry.get()}</p>' if subheading_entry.get() else ''}
        </header>
        
        <main>
            <p class="main-paragraph">{paragraph}</p>
            
            {f'<div class="image-container"><img src="{image_url_entry.get()}" alt="{image_alt_entry.get()}"></div>' if image_url_entry.get() else ''}
            
            {f'<p class="secondary-paragraph">{secondary_paragraph_text.get("1.0", "end-1c").strip().replace("\n", "<br>")}</p>' if secondary_paragraph_text.get("1.0", "end-1c").strip() else ''}
            
            <!-- Additional Content Stuff -->
            {additional_content_html}
        </main>
        
        {f'<footer><p>{footer_entry.get()}</p></footer>' if footer_entry.get() else ''}
    </div>
</body>
</html>
"""
    #----------------------------------- themes --------------------------------
    presets = {
        "Light Minimalist": {
            "background_color": "#ffffff", 
            "text_color": "#333333", 
            "heading_color": "#000000", 
            "font_family": "Helvetica",
            "container_bg": "#f9f9f9",
            "container_padding": "20px",
            "container_margin": "20px auto",
            "container_max_width": "800px",
            "border_radius": "8px",
            "box_shadow": "0 2px 4px rgba(0,0,0,0.1)",
            "video_bg": "#f0f0f0",
            "video_padding": "10px",
            "video_border_radius": "4px"
        },
        "Dark Mode": {
            "background_color": "#121212", 
            "text_color": "#e0e0e0", 
            "heading_color": "#ffffff", 
            "font_family": "Segoe UI",
            "container_bg": "#1e1e1e",
            "container_padding": "25px",
            "container_margin": "20px auto",
            "container_max_width": "800px",
            "border_radius": "0",
            "box_shadow": "0 4px 8px rgba(0,0,0,0.3)",
            "video_bg": "#f0f0f0",
            "video_padding": "10px",
            "video_border_radius": "4px"
        },
        "Ocean Breeze": {
            "background_color": "#e0f7fa", 
            "text_color": "#006064", 
            "heading_color": "#004d40", 
            "font_family": "Verdana",
            "container_bg": "#b2ebf2",
            "container_padding": "30px",
            "container_margin": "30px auto",
            "container_max_width": "750px",
            "border_radius": "12px",
            "box_shadow": "0 4px 8px rgba(0,105,92,0.2)",
            "video_bg": "#f0f0f0",
            "video_padding": "10px",
            "video_border_radius": "4px"
        },
        "Sunset Glow": {
            "background_color": "#fff3e0", 
            "text_color": "#4e342e", 
            "heading_color": "#e65100", 
            "font_family": "Georgia",
            "container_bg": "#ffe0b2",
            "container_padding": "25px",
            "container_margin": "25px auto",
            "container_max_width": "700px",
            "border_radius": "10px",
            "box_shadow": "0 4px 6px rgba(230,81,0,0.2)",
            "video_bg": "#f0f0f0",
            "video_padding": "10px",
            "video_border_radius": "4px"
        },
        "Forest": {
            "background_color": "#e8f5e9", 
            "text_color": "#2e7d32", 
            "heading_color": "#1b5e20", 
            "font_family": "Tahoma",
            "container_bg": "#c8e6c9",
            "container_padding": "20px",
            "container_margin": "20px auto",
            "container_max_width": "850px",
            "border_radius": "15px",
            "box_shadow": "0 3px 5px rgba(27,94,32,0.2)",
            "video_bg": "#f0f0f0",
            "video_padding": "10px",
            "video_border_radius": "4px"
        },
        "Cyberpunk Neon": {
            "background_color": "#0f0f0f", 
            "text_color": "#39ff14", 
            "heading_color": "#ff0055", 
            "font_family": "Courier New",
            "container_bg": "#1a1a1a",
            "container_padding": "20px",
            "container_margin": "20px auto",
            "container_max_width": "900px",
            "border_radius": "0",
            "box_shadow": "0 0 15px #ff0055, 0 0 30px #39ff14",
            "video_bg": "#f0f0f0",
            "video_padding": "10px",
            "video_border_radius": "4px"
        },
        "Midnight": {
            "background_color": "#0d1117",
            "text_color": "#c9d1d9",
            "heading_color": "#58a6ff",
            "font_family": "Consolas",
            "container_bg": "#161b22",
            "container_padding": "25px",
            "container_margin": "25px auto",
            "container_max_width": "850px",
            "border_radius": "6px",
            "box_shadow": "0 4px 8px rgba(0,0,0,0.5)",
            "video_bg": "#1f2937",
            "video_padding": "12px",
            "video_border_radius": "6px"
        },
        "Vintage": {
            "background_color": "#faf3e0",
            "text_color": "#5b4636",
            "heading_color": "#7a4e2d",
            "font_family": "Garamond",
            "container_bg": "#fffaf0",
            "container_padding": "30px",
            "container_margin": "30px auto",
            "container_max_width": "700px",
            "border_radius": "10px",
            "box_shadow": "0 3px 5px rgba(139,69,19,0.2)",
            "video_bg": "#f5f0e1",
            "video_padding": "12px",
            "video_border_radius": "8px"
        },
        "Candy": {
            "background_color": "#fff0f5",
            "text_color": "#6a1b9a",
            "heading_color": "#d81b60",
            "font_family": "Comic Sans MS",
            "container_bg": "#ffe4ec",
            "container_padding": "20px",
            "container_margin": "20px auto",
            "container_max_width": "800px",
            "border_radius": "20px",
            "box_shadow": "0 6px 12px rgba(216,27,96,0.3)",
            "video_bg": "#f8bbd0",
            "video_padding": "12px",
            "video_border_radius": "12px"
        }


    }

    # get theme 
    theme_choice = theme_var.get()
    style = presets[theme_choice]

    # CSS content
    css_content = f"""/* Global Styles */
body {{
    font-family: {style["font_family"]}, sans-serif;
    margin: 0;
    padding: 0;
    background-color: {style["background_color"]};
    color: {style["text_color"]};
    line-height: 1.6;
}}

/* Container */
.container {{
    background-color: {style["container_bg"]};
    padding: {style["container_padding"]};
    margin: {style["container_margin"]};
    max-width: {style["container_max_width"]};
    border-radius: {style["border_radius"]};
    box-shadow: {style["box_shadow"]};
}}

/* Typography */
h1 {{
    color: {style["heading_color"]};
    font-size: 2.2em;
    margin-bottom: 0.5em;
}}

.subheading {{
    font-size: 1.2em;
    color: {style["text_color"]};
    opacity: 0.8;
    margin-top: 0;
}}

p {{
    font-size: 1em;
    word-wrap: break-word;
}}

.main-paragraph {{
    margin-bottom: 1.5em;
}}

.secondary-paragraph {{
    font-size: 0.9em;
    opacity: 0.9;
}}

/* Additional Content Styles */
.additional-content {{
    margin: 1.5em 0;
    padding: 1em;
    background-color: rgba(0,0,0,0.05);
    border-radius: 4px;
}}

/* Links */
a {{
    color: #0645ad;
    text-decoration: none;
}}

a:hover {{
    color: #0b0080;
    text-decoration: underline;
}}

/* Image */
.image-container {{
    margin: 1.5em 0;
    text-align: center;
}}

.image-container img {{
    max-width: 100%;
    height: auto;
    border-radius: 4px;
}}

/* Video Embed Styles */
.video-container {{
    position: relative;
    padding-bottom: 56.25%; /* 16:9 aspect ratio */
    height: 0;
    overflow: hidden;
    margin: 1.5em 0;
    background-color: #000;
    border-radius: 8px;
}}

.video-container iframe {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    border: none;
}}

@media (max-width: 600px) {{
    .video-container iframe {{
        height: auto;
        min-height: 200px;
    }}
}}

/* Banner Styles */
.banner-container {{
    position: relative;
    width: 100%;
    margin-bottom: 2em;
}}

.banner-image {{
    width: 100%;
    max-height: 300px;
    object-fit: cover;
    border-radius: {style["border_radius"]};
    opacity: 0.8; 
}}

.banner-title {{
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    color: {style["heading_color"]}; 
    font-size: 3em;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3); 
    margin: 0;
    padding: 0;
}}

@media (max-width: 600px) {{
    .banner-title {{
        font-size: 2em;
    }}
}}

/* Footer */
footer {{
    margin-top: 2em;
    padding-top: 1em;
    border-top: 1px solid rgba(0,0,0,0.1);
    font-size: 0.8em;
    text-align: center;
    opacity: 0.7;
}}

/* respond to device */
@media (max-width: 600px) {{
    .container {{
        margin: 10px;
        padding: 15px;
    }}
    
    h1 {{
        font-size: 1.8em;
    }}
}}"""

    # Write to the HTML file
    with open(html_path, "w") as html_file:
        html_file.write(html_content)
    
    # Write to the CSS file
    with open(css_path, "w") as css_file:
        css_file.write(css_content)

    # Open the folder and the website (only if not in preview mode)
    if not preview:
        # Confirmation message
        messagebox.showinfo("Success", f"Website created:\n- HTML: {html_path}\n- CSS: {css_path}")
        os.startfile(html_path)
        os.startfile(script_dir) 
    else:
        os.startfile(html_path)



# Function to create a new additional content
def add_additional_content(content_type="paragraph"):
    # Create a frame for this additional content
    frame = tk.Frame(additional_content_container, bg="#f4f4f4", bd=1, relief="groove", padx=5, pady=5)
    frame.pack(fill="x", padx=5, pady=5)
    
    # Add a label to identify this content
    label = tk.Label(frame, text=f"Additional Content #{len(additional_content_boxes)+1}", font=("Helvetica", 10, "bold"), bg="#f4f4f4")
    label.grid(row=0, column=0, columnspan=2, sticky="w")
    
    if content_type == "paragraph":
        # Create a text widget for paragraph content
        text = tk.Text(frame, height=3, width=60, font=("Helvetica", 10))
        text.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        additional_content_boxes.append(("paragraph", text))

    elif content_type == "image":
        # Create entry fields for alt text and a button to select image
        tk.Label(frame, text="Image Alt Text:", font=("Helvetica", 10), bg="#f4f4f4").grid(row=1, column=0, padx=5, pady=2, sticky="e")
        alt_entry = tk.Entry(frame, width=30, font=("Helvetica", 10))
        alt_entry.grid(row=1, column=1, padx=5, pady=2, sticky="w")

        image_path_var = tk.StringVar()
        tk.Label(frame, text="Selected File:", font=("Helvetica", 8), bg="#f4f4f4").grid(row=2, column=0, padx=5, sticky="e")
        tk.Label(frame, textvariable=image_path_var, font=("Helvetica", 8), bg="#f4f4f4", fg="gray").grid(row=2, column=1, sticky="w")

        def select_image_file():
            file_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image files", "*.jpg *.png *.gif *.jpeg")])
            if file_path:
                image_path_var.set(file_path)

        browse_btn = tk.Button(frame, text="Browse Image", font=("Helvetica", 9), command=select_image_file)
        browse_btn.grid(row=3, column=1, padx=5, pady=2, sticky="w")

        additional_content_boxes.append(("image", {
            "alt": alt_entry,
            "path_var": image_path_var
        }))


    elif content_type == "video":
        # Create entry fields for YouTube URL
        tk.Label(frame, text="YouTube Video URL:", font=("Helvetica", 10), bg="#f4f4f4").grid(row=1, column=0, padx=5, pady=2, sticky="e")
        url_entry = tk.Entry(frame, width=40, font=("Helvetica", 10))
        url_entry.grid(row=1, column=1, padx=5, pady=2, sticky="w")
        
        # Add example text
        url_entry.insert(0, "https://www.youtube.com/watch?v=M6Nx0R83y3Y")
        
        additional_content_boxes.append(("video", {"url": url_entry}))
    
    # Add a delete button for the additional stuff
    delete_btn = tk.Button(frame, text="Remove", font=("Helvetica", 8), 
                          command=lambda f=frame, i=len(additional_content_boxes)-1: remove_content(f, i))
    delete_btn.grid(row=0, column=1, sticky="e")
    
    # Scroll
    canvas.configure(scrollregion=canvas.bbox("all"))

# Function to remove content 
def remove_content(frame, index):
    frame.destroy()
    if index < len(additional_content_boxes):
        additional_content_boxes.pop(index)
    # Update labels
    for i, child in enumerate(additional_content_container.winfo_children()):
        if isinstance(child, tk.Frame):
            child.winfo_children()[0].config(text=f"Additional Content #{i+1}")

# Function for the submit button
def on_submit():
    filename = html_filename_entry.get().strip()
    if not filename.endswith(".html"):
        filename += ".html"
    
    css_filename = css_filename_entry.get().strip()
    if not css_filename.endswith(".css"):
        css_filename += ".css"
    
    title = title_entry.get().strip()
    heading = heading_entry.get().strip()
    paragraph = paragraph_text.get("1.0", "end-1c").strip()
    paragraph = paragraph.replace('\n', '<br>')  # Convert newlines to HTML line breaks

    # Required field check
    if not filename or not css_filename or not title or not heading or not paragraph:
        messagebox.showerror("Input Error", "Please fill in all required fields.")
        return

    # Create the HTML file
    create_html_file(filename, title, heading, paragraph, css_filename)

def preview_html():
    filename = "preview.html"
    css_filename = "preview.css"
    title = title_entry.get().strip()
    heading = heading_entry.get().strip()
    paragraph = paragraph_text.get("1.0", "end-1c").strip().replace("\n", "<br>")

    if not title or not heading or not paragraph:
        messagebox.showerror("Missing Info", "Please fill in the required fields to preview.")
        return

    # Create temp directory for preview
    temp_dir = tempfile.mkdtemp()

    html_path = os.path.join(temp_dir, filename)
    css_path = os.path.join(temp_dir, css_filename)

    # Simulate required fields
    create_html_file(filename, title, heading, paragraph, css_filename, preview=True)
    #point to temp files

# Setting up the Tkinter window
root = tk.Tk()
root.title("Website Builder")

# Padding and font styling
root.geometry("800x700")
root.configure(bg="#f4f4f4")

# Create a canvas and scrollbar
canvas = tk.Canvas(root, bg="#f4f4f4")
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg="#f4f4f4")

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.grid(row=0, column=0, sticky="nsew")
scrollbar.grid(row=0, column=1, sticky="ns")

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Configure scrollable frame
scrollable_frame.grid_rowconfigure(0, weight=1)
scrollable_frame.grid_columnconfigure(0, weight=1)

# Mouse wheel scrolling function
def _on_mousewheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

# Bind mouse wheel to scroll
canvas.bind_all("<MouseWheel>", _on_mousewheel)
# ------------------------------------------ Required Fields -------------------------------------------------
required_frame = tk.LabelFrame(scrollable_frame, text="Required Fields", font=("Helvetica", 12, "bold"), bg="#f4f4f4")
required_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

# HTML Filename
tk.Label(required_frame, text="HTML Filename:", font=("Helvetica", 10), bg="#f4f4f4").grid(row=0, column=0, padx=10, pady=5, sticky="e")
html_filename_entry = tk.Entry(required_frame, width=40, font=("Helvetica", 10))
html_filename_entry.grid(row=0, column=1, padx=10, pady=5)
# Add descriptive text to the right
tk.Label(required_frame, text="(e.g., index.html)", font=("Helvetica", 8), bg="#f4f4f4", fg="gray").grid(row=0, column=2, padx=5, sticky="w")

# CSS Filename
tk.Label(required_frame, text="CSS Filename:", font=("Helvetica", 10), bg="#f4f4f4").grid(row=1, column=0, padx=10, pady=5, sticky="e")
css_filename_entry = tk.Entry(required_frame, width=40, font=("Helvetica", 10))
css_filename_entry.grid(row=1, column=1, padx=10, pady=5)
tk.Label(required_frame, text="(e.g., styles.css)", font=("Helvetica", 8), bg="#f4f4f4", fg="gray").grid(row=1, column=2, padx=5, sticky="w")

# Title
tk.Label(required_frame, text="Title of the Webpage:", font=("Helvetica", 10), bg="#f4f4f4").grid(row=2, column=0, padx=10, pady=5, sticky="e")
title_entry = tk.Entry(required_frame, width=40, font=("Helvetica", 10))
title_entry.grid(row=2, column=1, padx=10, pady=5)
tk.Label(required_frame, text="(Appears in browser tab)", font=("Helvetica", 8), bg="#f4f4f4", fg="gray").grid(row=2, column=2, padx=5, sticky="w")

# Heading (H1)
tk.Label(required_frame, text="Main Heading (H1):", font=("Helvetica", 10), bg="#f4f4f4").grid(row=3, column=0, padx=10, pady=5, sticky="e")
heading_entry = tk.Entry(required_frame, width=40, font=("Helvetica", 10))
heading_entry.grid(row=3, column=1, padx=10, pady=5)
tk.Label(required_frame, text="(Main page heading)", font=("Helvetica", 8), bg="#f4f4f4", fg="gray").grid(row=3, column=2, padx=5, sticky="w")

# Paragraph content
tk.Label(required_frame, text="Main Paragraph Content:", font=("Helvetica", 10), bg="#f4f4f4").grid(row=4, column=0, padx=10, pady=5, sticky="e")
paragraph_text = tk.Text(required_frame, height=5, width=40, font=("Helvetica", 10))
paragraph_text.grid(row=4, column=1, padx=10, pady=5)

# Theme selection
tk.Label(required_frame, text="Select a Theme:", font=("Helvetica", 10), bg="#f4f4f4").grid(row=5, column=0, padx=10, pady=5, sticky="e")
theme_var = tk.StringVar()
theme_choices = ["Light Minimalist", "Dark Mode", "Ocean Breeze", "Sunset Glow", "Forest", "Cyberpunk Neon", "Midnight", "Vintage", "Candy"]
theme_dropdown = tk.OptionMenu(required_frame, theme_var, *theme_choices)
theme_dropdown.grid(row=5, column=1, padx=10, pady=5, sticky="w")
theme_var.set("Light Minimalist")  # Set default theme

# --------------------------------------- Additional Content Section -------------------------------------------
content_frame = tk.LabelFrame(scrollable_frame, text="Additional Content", font=("Helvetica", 12, "bold"), bg="#f4f4f4")
content_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

# Subheading
tk.Label(content_frame, text="Subheading (optional):", font=("Helvetica", 10), bg="#f4f4f4").grid(row=0, column=0, padx=10, pady=5, sticky="e")
subheading_entry = tk.Entry(content_frame, width=40, font=("Helvetica", 10))
subheading_entry.grid(row=0, column=1, padx=10, pady=5)
tk.Label(content_frame, text="(Smaller text under heading)", font=("Helvetica", 8), bg="#f4f4f4", fg="gray").grid(row=0, column=2, padx=5, sticky="w")

# Secondary Paragraph
tk.Label(content_frame, text="Secondary Paragraph (optional):", font=("Helvetica", 10), bg="#f4f4f4").grid(row=1, column=0, padx=10, pady=5, sticky="e")
secondary_paragraph_text = tk.Text(content_frame, height=3, width=40, font=("Helvetica", 10))
secondary_paragraph_text.grid(row=1, column=1, padx=10, pady=5)

# Image URL
tk.Label(content_frame, text="Image URL (optional):", font=("Helvetica", 10), bg="#f4f4f4").grid(row=2, column=0, padx=10, pady=5, sticky="e")
image_url_entry = tk.Entry(content_frame, width=40, font=("Helvetica", 10))
image_url_entry.grid(row=2, column=1, padx=10, pady=5)
tk.Label(content_frame, text="(Full URL to your image)", font=("Helvetica", 8), bg="#f4f4f4", fg="gray").grid(row=2, column=2, padx=5, sticky="w")

# Image Alt Text
tk.Label(content_frame, text="Image Alt Text (optional):", font=("Helvetica", 10), bg="#f4f4f4").grid(row=3, column=0, padx=10, pady=5, sticky="e")
image_alt_entry = tk.Entry(content_frame, width=40, font=("Helvetica", 10))
image_alt_entry.grid(row=3, column=1, padx=10, pady=5)

# Footer
tk.Label(content_frame, text="Footer Text (optional):", font=("Helvetica", 10), bg="#f4f4f4").grid(row=4, column=0, padx=10, pady=5, sticky="e")
footer_entry = tk.Entry(content_frame, width=40, font=("Helvetica", 10))
footer_entry.grid(row=4, column=1, padx=10, pady=5)

# Banner Image
tk.Label(content_frame, text="Banner Image URL (optional):", font=("Helvetica", 10), bg="#f4f4f4").grid(row=6, column=0, padx=10, pady=5, sticky="e")
banner_url_entry = tk.Entry(content_frame, width=40, font=("Helvetica", 10))
banner_url_entry.grid(row=6, column=1, padx=10, pady=5)
tk.Label(content_frame, text="(Large header image)", font=("Helvetica", 8), bg="#f4f4f4", fg="gray").grid(row=6, column=2, padx=5, sticky="w")

# Banner Title Overlay
tk.Label(content_frame, text="Banner Title (optional):", font=("Helvetica", 10), bg="#f4f4f4").grid(row=7, column=0, padx=10, pady=5, sticky="e")
banner_title_entry = tk.Entry(content_frame, width=40, font=("Helvetica", 10))
banner_title_entry.grid(row=7, column=1, padx=10, pady=5)

# Save Location Option (KEEP AT THE END)
save_location_var = tk.BooleanVar()
save_location_check = tk.Checkbutton(content_frame, text="Choose custom save location", variable=save_location_var, font=("Helvetica", 10), bg="#f4f4f4")
save_location_check.grid(row=8, column=0, columnspan=1, pady=10)
tk.Label(content_frame, text="(It is recommended that you create a folder to save the website to)", font=("Helvetica", 8), bg="#f4f4f4", fg="gray").grid(row=8, column=1, padx=5, sticky="w")

# Container for dynamic additional content
additional_content_container = tk.Frame(scrollable_frame, bg="#f4f4f4")
additional_content_container.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

# List to track additional content boxes
additional_content_boxes = []

# ------------------------------------ Buttons to add new content -----------------------------------
add_content_frame = tk.Frame(scrollable_frame, bg="#f4f4f4")
add_content_frame.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

tk.Button(add_content_frame, text="Add Paragraph", command=lambda: add_additional_content("paragraph"), 
          font=("Helvetica", 10), bg="#2196F3", fg="white").pack(side="left", padx=5)
tk.Button(add_content_frame, text="Add Image", command=lambda: add_additional_content("image"), 
          font=("Helvetica", 10), bg="#4CAF50", fg="white").pack(side="left", padx=5)
tk.Button(add_content_frame, text="Add Video", command=lambda: add_additional_content("video"), 
          font=("Helvetica", 10), bg="#FF5722", fg="white").pack(side="left", padx=5)


# Preview button
preview_button = tk.Button(scrollable_frame, text="Preview Website", font=("Helvetica", 12), command=preview_html, bg="#2196F3", fg="white")
preview_button.grid(row=4, column=0, pady=(0, 20), sticky="ew")

#  Submit
submit_button = tk.Button(scrollable_frame, text="Generate Website", font=("Helvetica", 12), command=on_submit, bg="#4CAF50", fg="white")
submit_button.grid(row=5, column=0, pady=10, sticky="ew")

# add some white space at the bottom for quality
spacer = tk.Label(scrollable_frame, text="", bg="#f4f4f4")
spacer.grid(row=6, column=0, pady=30)


# Run 
root.mainloop()