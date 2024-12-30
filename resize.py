from PIL import Image

# Padrão: 360 / 580
def resize(path: str, size=(270, 405)) -> str:
    with Image.open(path) as image:
        resized = image.resize(size)
        resized.save(path)
        return path
