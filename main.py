from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)

class Boez:
    def __init__(self, name, coordinates):
        #self.name = 'images/' + name + '.png'
        self.name = name
        self.coordinates = coordinates

boizi_proverka = {}

boizi = {}

@app.route('/', methods=['GET', 'POST'])
def arena():
    if request.method == 'POST':
        b = Boez(request.form.get('name'), request.form.get('coordinates'))
        boizi_proverka[b.name] = b.coordinates
        boizi.clear()
        for k, v in boizi_proverka.items():
            boizi[v] = k
        return redirect(url_for('arena', boizi=boizi))
    return render_template('arena.html', boizi=boizi)

if __name__ == '__main__':
    app.run(debug=True)