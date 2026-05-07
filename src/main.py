import sys

from copystatic import setup_public_dir
from gencontent import generate_pages_recursive

def main():
    basepath = "/"
    output_dir = "./docs" #./docs for github, ./public for statndard deployment
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    setup_public_dir("./static", output_dir)
    generate_pages_recursive("./content", "./template.html", output_dir, basepath)
    
main()