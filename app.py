from flask import Flask, render_template, request, send_file
from PIL import Image, ImageDraw, ImageFont
import os
import barcode
from barcode.writer import ImageWriter

app = Flask(__name__)

# Garantir que a pasta static exista
os.makedirs("static", exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gerar', methods=['POST'])
def gerar():
    nome = request.form['nome']
    nascimento = request.form['nascimento']
    sexo = request.form['sexo']
    cns = request.form['cns']

    # Geração da imagem
    img = Image.new('RGB', (800, 500), color='white')
    draw = ImageDraw.Draw(img)

    # Fonte Arial (certifique-se que a fonte esteja presente)
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    if not os.path.exists(font_path):
        font_path = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
    fonte = ImageFont.truetype(font_path, 30)

    draw.text((50, 50), f'Nome: {nome}', font=fonte, fill='black')
    draw.text((50, 100), f'Data de Nascimento: {nascimento}', font=fonte, fill='black')
    draw.text((50, 150), f'Sexo: {sexo}', font=fonte, fill='black')
    draw.text((50, 200), f'CNS: {cns}', font=fonte, fill='black')

    # Geração do código de barras
    ean = barcode.get('code128', cns, writer=ImageWriter())
    barcode_path = 'static/barcode.png'
    ean.save(barcode_path)

    barcode_img = Image.open(barcode_path)
    img.paste(barcode_img.resize((400, 100)), (50, 250))

    # Salvar imagem final
    caminho = 'static/cartao.png'
    img.save(caminho)

    return send_file(caminho, mimetype='image/png')

if __name__ == '__main__':
    app.run()
