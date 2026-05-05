from copystatic import setup_public_dir
from gencontent import generate_page

def main():
    setup_public_dir("./static", "./public")
    generate_page("./content/index.md", "./template.html", "public/index.html")
main()