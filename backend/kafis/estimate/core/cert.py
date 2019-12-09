from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw


def cert(face, name, class_tag):
    face = face.resize((300, 300))
    fontsize = 36
    font = ImageFont.truetype("/home/ubuntu/project/kafis/backend/kafis/estimate/core/arial.ttf", fontsize, encoding="unic")
    text_position_1 = (300, 350)
    face_position = (250, 425)
    text_position_2 = (250, 750)
    text_position_3 = (250, 850)
    text_color = (0, 0, 0)
    img = Image.open('/home/ubuntu/project/kafis/backend/kafis/estimate/core/certificate.jpg')
    img.paste(face, face_position)
    # img.show()
    draw = ImageDraw.Draw(img)
    text_1 = "О том, что"
    text_2 = name
    text_3 = "{0} человек".format(class_tag)
    draw.text(text_position_1, text_1, text_color, font)
    draw.text(text_position_2, text_2, text_color, font)
    draw.text(text_position_3, text_3, text_color, font)
    img_path = 'media/photos/certificate_{0}.jpg'.format(name)
    img.save(img_path)
    return 'http://185.228.234.181:8000/' + img_path

# cert(0, 'Антон Смирнов', 'красивый')
