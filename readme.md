
## Setup

1. Create and activate the virtual environment:

    ```bash
    python -m venv venv          # Create a virtual environment
    ```

    On Windows:

    ```bash
    .\venv\Scripts\activate     # Activate the virtual environment
    ```

    On Unix or MacOS:

    ```bash
    source venv/bin/activate    # Activate the virtual environment
    ```

2. Install project dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Place your images in the `images/` folder.
2. Run the text detection script:

    ```bash
    python src/main.py
    ```

3. View the detected text in the terminal output.

## Notes

- Adjust Tesseract configurations and preprocessing steps in `main.py` based on your image characteristics.
- Explore additional libraries or methods for more advanced text detection scenarios.

## Contributors

- [Your Name]
- [Contributor 2]
- ...

## License

This project is licensed under the [MIT License](LICENSE).
