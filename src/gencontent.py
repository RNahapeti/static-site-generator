import os

from pathlib import Path
from block_markdown import markdown_to_html_node

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No H1 header found in markdown")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        md_content = f.read()
    with open(template_path, "r") as f:
        t_content = f.read()

    html = markdown_to_html_node(md_content).to_html()
    title = extract_title(md_content)
    inter_html = t_content.replace("{{ Title }}", title).replace("{{ Content }}", html)
    final_html = inter_html.replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')

    # Make the necessary directories for our final file if necessary
    dest_directory = os.path.dirname(dest_path)
    if dest_directory:
        os.makedirs(dest_directory, exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(final_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for file in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, file)
        dest_path = os.path.join(dest_dir_path, file)
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page(from_path, template_path, dest_path, basepath)
        else:
            generate_pages_recursive(from_path, template_path, dest_path, basepath)