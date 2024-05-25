# fontsvg

## Overview

`fontsvg` is a Python script that converts font glyphs to SVG files. This script uses the `fonttools` and `svgwrite` libraries to extract glyphs from a font file and save them as individual SVG files.

## Requirements

- Python 3.12 or later
- `fonttools` library
- `svgwrite` library

## Installation

1. **Clone the Repository**:
    ```sh
    git clone https://github.com/eboy79/fontsvg.git
    cd fontsvg
    ```

2. **Create a Virtual Environment**:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install Dependencies**:
    ```sh
    pip install svgwrite fonttools
    ```

## Usage

1. **Place your Font File**:
    - Place the font file you want to convert in the `fontsvg` directory. Update the script with the correct font file name if necessary.

2. **Run the Script**:
    - Run the `generate_svgs.py` script to generate SVG files for each glyph in the font:
    ```sh
    python generate_svgs.py
    ```

3. **Output**:
    - The script will generate SVG files for each glyph in the same directory.

## Script Details

The `generate_svgs.py` script extracts glyphs from the specified font file and saves them as individual SVG files. Below is a brief overview of the main functions:

- `get_svg_path_for_char(font, char)`: This function retrieves the SVG path for a specific character from the font.
- `create_svg_for_char(char, path)`: This function creates an SVG file for the given character and path.
- The script iterates through a predefined set of characters (A-Z, a-z) and generates SVG files for each.

## Example

To convert a font named `example_font.ttf`:

1. Place `example_font.ttf` in the `fontsvg` directory.
2. Update the font file path in `generate_svgs.py` if necessary:
    ```python
    font = TTFont('example_font.ttf')
    ```
3. Run the script:
    ```sh
    python generate_svgs.py
    ```
4. SVG files will be created for each character in the directory.

## Troubleshooting

- Ensure the font file is in the correct format and accessible.
- Make sure all dependencies are installed in the virtual environment.
- If you encounter any errors, verify the glyph extraction logic in the script and adjust as necessary for the specific font type.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributions

Contributions are welcome! Please submit a pull request or open an issue to discuss any changes or improvements.

## Contact

For any questions or feedback, please contact [eboy79](https://github.com/eboy79).

