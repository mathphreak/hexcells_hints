from PIL import Image, ImageFilter, ImageOps, ImageStat
from .cell import Cell
from .util import SloppyDict
from collections import defaultdict
import pytesseract
import platform


if platform.system() == 'Windows':
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'
    tessdata_dir_config = r'--tessdata-dir "C:\Program Files (x86)\Tesseract-OCR\tessdata"'
else:
    tessdata_dir_config = ''


def hex_box(x, y, edge_len, buffer=5):
    return (round(x - edge_len / 2 - buffer / 2),
            round(y - buffer / 2),
            round(x + (3 / 2 * edge_len) + buffer / 2),
            round(y + (edge_len * (3 ** 0.5)) + buffer / 2))


def get_hex_edge(edges, threshold=60):
    for sum in range(260, edges.height + edges.width - 10):
        for y in range(5, sum - 5):
            x = sum - y
            if x > edges.width - 5 or y > edges.height - 5:
                continue
            if edges.getpixel((x, y)) > threshold:
                print('EDGE:', (x, y))
                start_x = x
                end_x = x + 1
                while end_x < edges.width and edges.getpixel((end_x, y)) > threshold:
                    end_x += 1
                if end_x - start_x > 10:
                    return round((end_x - start_x) / 8) * 8


k = 0


def get_hex_label(hex):
    # hex = hex.resize((3 * hex.width, 3 * hex.height), Image.BICUBIC)
    global k
    # hex.save('hex_' + str(k) + '.png')
    k += 1
    result = pytesseract.image_to_string(hex, lang='eng', config='--psm 8 ' + tessdata_dir_config)
    result = result.upper().replace('O', '0').replace('T', '1').replace('S', '5')
    result = result.strip(" ,'\u2018\u2019")
    # I still don't understand where this came from.
    result = result.lstrip('Y')
    if result[0] == '{':
        result = result[:2] + '}'
    elif result[-1] == '}':
        result = '{' + result[-2:]
    elif result[0] == '-':
        result = result[:2] + '-'
    elif result[-1] == '-':
        result = '-' + result[-2:]
    return result


def parse_hex(hex):
    bbox = hex.getbbox()
    bbox = (bbox[0] + 24, bbox[1] + 20, bbox[2] - 30, bbox[3] - 25)
    hex_body = hex.crop(bbox)
    median = ImageStat.Stat(hex_body).median
    if median[0] > 200 and 150 < median[1] < 200 and median[2] < 100:
        return Cell(False, None, None)
    if median[0] < 50 and 150 < median[1] < 200 and median[2] > 200:
        return Cell(True, True, '')
    if median[0] < 100 and median[1] < 100 and median[2] < 100:
        return Cell(True, False, get_hex_label(hex_body))
    if median[0] > 200 and median[1] > 200 and median[2] > 200:
        return None
    print('Unknown color:', median)
    Image.new('RGB', (100, 100), tuple(median)).show()
    hex.show()
    return median


def nuke_scoreboard(im):
    nothing = Image.new('L', (250, 220), 0)
    im.paste(nothing, (im.width - nothing.width, 0))


def load_image(path):
    im = Image.open(path)
    orig = im.copy()
    im = im.rotate(45, expand=True)
    bbox = im.getbbox()
    bbox = (bbox[0] + 256, bbox[1], bbox[2], bbox[3])
    im = im.crop(bbox)
    im = im.rotate(-45)
    im = im.crop(im.getbbox())
    edges = im.filter(ImageFilter.FIND_EDGES)
    nuke_scoreboard(edges)
    edges = ImageOps.grayscale(edges).filter(ImageFilter.MedianFilter()).filter(ImageFilter.EDGE_ENHANCE)
    # edges.show()
    hex_edge_len = get_hex_edge(edges)
    buffer = 14
    print("Edge length:", hex_edge_len)
    cells_rows = SloppyDict(10, defaultdict(lambda: SloppyDict(10, {})))
    cells_cols = SloppyDict(10, defaultdict(lambda: SloppyDict(10, {})))
    # start at 5 to avoid top edge artifacts
    for sum in range(260, im.height + im.width - 10):
        for y in range(5, sum - 5):
            x = sum - y
            if x > im.width - 5 or y > im.height - 5:
                continue
            if edges.getpixel((x, y)) > 60:
                print(x, y)
                box = hex_box(x, y, hex_edge_len, buffer)
                hex = im.crop(box)
                # edges.show()
                hex_ghost = Image.new('L', (box[2] - box[0], box[3] - box[1]), 10)
                edges.paste(hex_ghost, box=box)
                # edges.show()
                cell = parse_hex(hex)
                if cell is not None:
                    cells_rows[y][x] = cell
                    cells_cols[x][y] = cell
    print('Rows:', len(cells_rows), sorted(cells_rows.keys()))
    print('Cols:', len(cells_cols), sorted(cells_cols.keys()))
    cells = [[None for k in cells_cols] for i in cells_rows]
    col_indices = SloppyDict(10, dict((k, i) for i, k in enumerate(sorted(cells_cols.keys()))))
    for i, y in enumerate(sorted(cells_rows.keys())):
        row = cells_rows[y]
        for x, cell in row.items():
            cells[i][col_indices[x]] = cell
    return orig, cells
