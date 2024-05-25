import os
import sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
import xml.etree.ElementTree as ET
from cairosvg import svg2png
from PIL import Image

def generate_svgs(font_path, output_dir):
    font = TTFont(font_path)
    glyph_set = font.getGlyphSet()
    
    for glyph_name in font.getGlyphOrder():
        if glyph_name not in ['.notdef', '.null', 'nonmarkingreturn'] and glyph_name.isalpha() and glyph_name.isupper():
            glyph = glyph_set[glyph_name]
            pen = SVGPathPen(glyph_set)
            glyph.draw(pen)
            svg_path = os.path.join(output_dir, f"{glyph_name}.svg")
            
            # Create the SVG XML structure
            svg = ET.Element("svg", {
                "xmlns": "http://www.w3.org/2000/svg",
                "viewBox": "0 0 1000 1000",  # Temporary viewBox, will be updated later
                "xml:space": "preserve"
            })
            path = ET.SubElement(svg, "path", {
                "d": pen.getCommands(),
                "fill": "black"
            })

            # Save the SVG file
            tree = ET.ElementTree(svg)
            tree.write(svg_path)

    font.close()

def adjust_svg(input_path, output_path):
    # Parse the SVG file
    tree = ET.parse(input_path)
    root = tree.getroot()
    ns = {'svg': 'http://www.w3.org/2000/svg'}

    # Render the SVG to PNG using CairoSVG
    png_file = input_path.replace('.svg', '.png')
    svg2png(url=input_path, write_to=png_file)

    # Open the rendered PNG and get its bounding box
    with Image.open(png_file) as img:
        bbox = img.getbbox()
        if bbox:
            xmin, ymin, xmax, ymax = bbox
            width = xmax - xmin
            height = ymax - ymin

            # Update the viewBox and dimensions
            root.attrib['viewBox'] = f"{xmin} {ymin} {width} {height}"
            root.attrib['width'] = str(width)
            root.attrib['height'] = str(height)

            # Correct the orientation if necessary (invert Y axis)
            for path_element in root.findall('.//svg:path', ns):
                transform = f"translate(0, {height}) scale(1, -1)"
                if 'transform' in path_element.attrib:
                    path_element.attrib['transform'] += " " + transform
                else:
                    path_element.attrib['transform'] = transform

            # Save the updated SVG to the output directory
            tree.write(output_path)
            print(f"Processed {input_path} to {output_path}")
        else:
            print(f"No bounding box found for {input_path}")

    # Clean up the temporary PNG file
    os.remove(png_file)

def process_svgs_in_folder(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(".svg"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            adjust_svg(input_path, output_path)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python generate_svgs.py /path/to/font/file.otf")
        sys.exit(1)

    font_path = sys.argv[1]
    if not os.path.isfile(font_path):
        print(f"Font file not found: {font_path}")
        sys.exit(1)

    output_dir = "svgs"
    adjusted_output_dir = "output_svgs"
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    if not os.path.exists(adjusted_output_dir):
        os.makedirs(adjusted_output_dir)

    print(f"Generating SVGs from font: {font_path}")
    generate_svgs(font_path, output_dir)
    print("Adjusting SVG bounding boxes...")
    process_svgs_in_folder(output_dir, adjusted_output_dir)
    print("SVG generation and adjustment complete.")
