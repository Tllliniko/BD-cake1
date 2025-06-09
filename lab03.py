import webbrowser
import os
import configparser
def open_browser(gallery_data):
    gallery_data_js = f'var galleryData = {gallery_data};'
    html_content = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>Галерея</title>
        <style> body {{background-color: #FFB6C1;font-family: Arial, sans-serif;display: flex;flex-direction: column;align-items: center;justify-content: center;height: 100vh;margin: 0;padding: 0 20px;}}
            h1 {{color: #8B0000;font-size: 48px;margin: 20px 0;text-align: center;}}
            h2 {{color: #8B008B;font-size: 36px;text-align: center;}}
            .start-link {{color: blue;font-size: 24px;cursor: pointer;text-decoration: underline;margin-top: 30px;text-align: center;}}
            .start-link:hover {{color: #FF4500;}}
            .cake-container {{text-align: center;max-width: 800px;margin: auto;}}
            #cake-image {{max-width: 100%;height: auto;margin-bottom: 20px;border: 5px solid #FFFACD;border-radius: 10px;max-height: 300px;width: 95%;height: 400px;}}
            #cake-description {{text-align: justify;background-color: #E0FFFF;padding: 20px;border-radius: 10px;margin: auto;max-width: 600px;width: 90%;height: 240px;overflow-y: auto;}}
            button {{background-color: #FFB6C1;border: none;padding: 10px 20px;font-size: 16px;cursor: pointer;margin: 10px;border-radius: 5px;transition: background-color 0.3s;}}
            button:hover {{background-color: #FF69B4;}}
        </style>
        <script>{gallery_data_js}
            var currentIndex = 0; function showCake(index) {{currentIndex = index; document.getElementById('cake-title').innerText = galleryData[index].name; document.getElementById('cake-image').src = galleryData[index].image;
                document.getElementById('cake-description').innerText = galleryData[index].description;
                document.getElementById('gallery-start').style.display = 'none';
                document.getElementById('cake-container').style.display = 'block';}}
            function nextCake() {{currentIndex = (currentIndex + 1) % galleryData.length;
                showCake(currentIndex);}}
            function prevCake() {{currentIndex = (currentIndex - 1 + galleryData.length) % galleryData.length;
                showCake(currentIndex);}}
        </script>
    </head>
    <body> 
        <div id="gallery-start" style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh;">
            <h1>ГАЛЕРЕЯ</h1>
            <h2>ТОРТЫ</h2>
            <p class="start-link" onclick="showCake(0)">НАЧАТЬ ПРОСМОТР БД ТОРТОВ</p>
        </div>
        <div id="cake-container" class="cake-container" style="display: none;">
            <h1 id="cake-title"></h1>
            <img id="cake-image" src="" alt="Торт">
            <p id="cake-description"></p>
            <button onclick="prevCake()">Назад</button>
            <button onclick="nextCake()">Вперёд</button></div>
    </body>
    </html>"""
    with open('gallery.html', 'w', encoding='utf-8') as file: # Сохранение HTML содержимого файла
        file.write(html_content)
    webbrowser.open('file://' + os.path.realpath('gallery.html'))    # Открываем HTML-файл в веб-браузере по умолчанию
def create_gallery_data(folder_path):
    config = configparser.ConfigParser()
    ini_path = os.path.join(folder_path, 'index.ini')
    if not os.path.exists(ini_path):
        return []
    with open(ini_path, 'r', encoding='utf-8') as f:
        config.read_file(f)
    gallery_data = []
    for section in config.sections():
        cake_name = section
        image_path = os.path.join(folder_path, config[section]['image'])
        info_path = os.path.join(folder_path, config[section]['info'])
        try:
            with open(info_path, 'r', encoding='utf-8') as f:
                description = f.read()
            gallery_data.append({'name': cake_name, 'image': image_path, 'description': description})
        except Exception as e:
            print(f"Ошибка при загрузке данных торта '{cake_name}': {e}")
    return gallery_data


