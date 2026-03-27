import adif_io as aio
import pprint
from PIL import Image, ImageDraw, ImageFont
import os

def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    import unicodedata
    import re
    # 使用原始字符串 r'' 避免转义警告
    value = str(re.sub(r'[^\w\s-]', '', value).strip().lower())
    value = str(re.sub(r'[-\s]+', '-', value))
    return value

def drawCenteredText(text, textarea, font_in, font_color='rgb(0,0,0)', y_offset_correction=0):
    """
    在指定区域绘制居中文字（水平+垂直居中）
    
    参数：
    - text: 要绘制的文字
    - textarea: 字典，包含 'offset' 和 'size'，可选 'y_offset_correction'
    - font_in: PIL 字体对象
    - font_color: 文字颜色
    - y_offset_correction: 纵向微调，可正可负
    """
    # 获取字体基线信息
    ascent, descent = font_in.getmetrics()
    
    # 文字实际边界
    bbox = draw.textbbox((0, 0), text, font=font_in)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]

    # 水平居中
    x = ((textarea['size'][0] - w) / 2) + textarea['offset'][0]
    
    # 垂直居中，使用 ascent/descent 进行调整
    y = ((textarea['size'][1] - h) / 2) + textarea['offset'][1] - descent / 2

    # 如果 textarea 字典里有 y_offset_correction，则叠加
    y += textarea.get('y_offset_correction', 0)
    y += y_offset_correction

    draw.text((x, y), text, font=font_in, fill=font_color)


fontfile = 'Roboto/Roboto-Regular.ttf'
font = ImageFont.truetype(fontfile, size=63)

boldfontfile = 'Roboto/Roboto-Black.ttf'
bold_font = ImageFont.truetype(boldfontfile, size=63)

freq_font = ImageFont.truetype(fontfile, size=52)

sigfontfile = 'Autography/Autography.otf'
sig_font = ImageFont.truetype(sigfontfile, size=63)

imageinfo = [
    {
        'filename': 'DigitalQSL.jpg',
        'fields': {
            'to_radio': {'offset': (70, 714), 'size': (350, 108)},
            'date_d': {'offset': (426, 714), 'size': (116, 108)},
            'date_m': {'offset': (548, 714), 'size': (104, 108)},
            'date_y': {'offset': (659, 714), 'size': (126, 108)},
            'time_on': {'offset': (793, 714), 'size': (218, 108)},
            'freq': {'offset': (1016, 714), 'size': (260, 108)},
            'mode': {'offset': (1284, 714), 'size': (214, 108)},
            'rst': {'offset': (1508, 714), 'size': (185, 108)},
            'confirm_qso': {'offset': (1111, 455), 'size': (52, 52)},
            'pse_qsl': {'offset': (52, 458), 'size': (52, 52)},
            '73': {'offset': (1166, 855), 'size': (518, 107)}
        }
    },
    {
        'filename': 'GenericQSL.jpg',
        'fields': {
            'to_radio': {'offset': (64, 714), 'size': (350, 108)},
            'date_d': {'offset': (403, 714), 'size': (116, 108)},
            'date_m': {'offset': (512, 714), 'size': (104, 108)},
            'date_y': {'offset': (615, 714), 'size': (126, 108)},
            'time_on': {'offset': (733, 714), 'size': (218, 108)},
            'freq': {'offset': (936, 714), 'size': (260, 108)},
            'mode': {'offset': (1185, 714), 'size': (214, 108)},
            'rst': {'offset': (1395, 714), 'size': (185, 108)},
            'confirm_qso': {'offset': (1025, 480), 'size': (52, 52)},
            'pse_qsl': {'offset': (65, 480), 'size': (52, 52)},
            '73': {'offset': (1130, 847), 'size': (518, 160)}
        }
    }
]

CARDNO = 1
fields = imageinfo[CARDNO]['fields']

adif_file = "wsjtx_log_ORIG.adi"
adif = aio.read_from_file(adif_file)

#sig_img = Image.open("Scott_Trans.png")
#ratio =  sig_img.height / fields['73']['size'][1]
#(im_w, im_h) = (int(sig_img.width // ratio), int(sig_img.height // ratio))
#sig_img_r = sig_img.resize((im_w, im_h))

white = 'rgb(255,255,255)'
black = 'rgb(0,0,0)'
red = 'rgb(255,0,0)'
blue= 'rgb(0,0,255)'

for qso in adif[0]:
    print(f"Working on {qso['CALL']}")
    image = Image.open(imageinfo[CARDNO]['filename'])

    draw = ImageDraw.Draw(image)

    #Call
    drawCenteredText(qso['CALL'], fields['to_radio'], bold_font, black)

    #QSO date
    day = qso['QSO_DATE'][-2:]
    month = qso['QSO_DATE'][4:6]
    year = qso['QSO_DATE'][2:4]

    drawCenteredText(day, fields['date_d'], bold_font, black)
    drawCenteredText(month, fields['date_m'], bold_font, black)
    drawCenteredText(year, fields['date_y'], bold_font, black)

    #QSO time_on
    time_on = qso['TIME_ON'][:2] + ":" + qso['TIME_ON'][2:4]
    drawCenteredText(time_on, fields['time_on'], bold_font, black)

    #QSO Frequency
    freq = qso['FREQ'][:8]
    drawCenteredText(freq, fields['freq'], freq_font, red)

    #QSO mode
    qso_mode = qso['MODE']
    drawCenteredText(qso_mode, fields['mode'], bold_font, black)

    #RST
    rst = qso['RST_SENT']
    drawCenteredText(rst, fields['rst'], bold_font, black)

    #confirm QSO
    drawCenteredText('x', fields['confirm_qso'], bold_font, black, 0)

    #pse QSL
    drawCenteredText('x', fields['pse_qsl'], bold_font, black, 0)

    #73
    drawCenteredText('de BG7XTQ', fields['73'], sig_font, blue)

    filecall = slugify(qso['CALL'])
    filedatetime = str(qso['QSO_DATE'][:4]) + str(month) + str(day) + '_' + str(qso['TIME_ON'])
    if not os.path.exists('out'):
        os.makedirs('out')
    image.save(f"out/{filecall}_{filedatetime}.jpg")
