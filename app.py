from flask import Flask, request, jsonify, send_file
from PIL import Image, ImageDraw, ImageFont
import io

app = Flask(__name__)

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    title = data.get("title", "Titolo sconosciuto")
    artist = data.get("artist", "Artista sconosciuto")
    price = data.get("price", "-- €")
    discount = data.get("discount", "-20")

    # colori e font
    bg = (255, 230, 128)
    badge_color = (255, 58, 58)
    text_color = (27, 27, 58)
    white = (255, 255, 255)

    font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 56)
    font_artist = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
    font_price = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
    font_badge = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
    font_logo = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)

    img = Image.new("RGB", (1080,1080), color=bg)
    draw = ImageDraw.Draw(img)

    # vinile centrale
    x, y, r = 540, 380, 260
    draw.ellipse([x-r, y-r, x+r, y+r], fill=(10,10,10))
    draw.ellipse([x-r*0.35, y-r*0.35, x+r*0.35, y+r*0.35], fill=(80,80,80))

    # pannello bianco sotto
    draw.rectangle([50, 820, 1030, 1050], fill=white)

    # titolo + artista
    draw.text((90, 840), title[:40], font=font_title, fill=text_color)
    draw.text((90, 910), artist, font=font_artist, fill=text_color)

    # prezzo
    draw.text((880, 840), f"{price}", font=font_price, fill=badge_color)

    # badge sconto
    draw.ellipse([90, 90, 200, 200], fill=badge_color)
    txt = discount if str(discount).startswith("-") else f"-{discount}%"
    tw, th = draw.textsize(txt, font=font_badge)
    draw.text((145 - tw/2, 145 - th/2), txt, font=font_badge, fill=white)

    # logo
    lw, lh = draw.textsize("VINIL DOC", font=font_logo)
    draw.text((540 - lw/2, 30), "VINIL DOC", font=font_logo, fill=text_color)

    # output in memoria
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    return send_file(buffer, mimetype="image/png")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)