from PIL import Image, ImageFilter, ImageOps, ImageStat
from .cell import Cell
from .util import SloppyDict
from collections import defaultdict


def hex_box(x, y, edge_len, buffer=5):
    return (round(x - edge_len / 2 - buffer / 2),
            round(y - buffer / 2),
            round(x + (3 / 2 * edge_len) + buffer / 2),
            round(y + (edge_len * (3 ** 0.5)) + buffer / 2))


def get_hex_edge(edges, threshold=60):
    # start at 5 to dodge artifacts
    for y in range(5, edges.height - 5):
        for x in range(max(5, 256 - y), edges.width - 5):
            if edges.getpixel((x, y)) > threshold:
                print('EDGE:', (x, y))
                start_x = x
                end_x = x + 1
                while end_x < edges.width and edges.getpixel((end_x, y)) > threshold:
                    end_x += 1
                if end_x - start_x > 10:
                    return end_x - start_x


k = 0


def get_hex_label(hex):
    bbox = hex.getbbox()
    bbox = (bbox[0] + 32, bbox[1] + 10, bbox[2] - 30, bbox[3] - 20)
    hex = hex.crop(bbox)
    # hex = hex.resize((5 * hex.width, 5 * hex.height), Image.BICUBIC)
    global k
    import pytesseract
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'
    tessdata_dir_config = r'--tessdata-dir "C:\Program Files (x86)\Tesseract-OCR\tessdata"'
    hex.save('hex_' + str(k) + '.png')
    k += 1
    result = pytesseract.image_to_string(hex, config='--psm 8 ' + tessdata_dir_config)
    return result.upper().replace('O', '0').replace('T', '1').strip(' ,')


def parse_hex(hex):
    median = ImageStat.Stat(hex).median
    if median[0] > 200 and 100 < median[1] < 200 and median[2] < 100:
        return Cell(False, None, None)
    if median[0] < 100 and 100 < median[1] < 200 and median[2] > 200:
        return Cell(True, True, '')
    if median[0] < 100 and median[1] < 100 and median[2] < 100:
        return Cell(True, False, get_hex_label(hex))
    if median[0] > 200 and median[1] > 200 and median[2] > 200:
        return None
    print('Unknown color:', median)
    Image.new('RGB', (100, 100), tuple(median)).show()
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
                # hex.show()
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
