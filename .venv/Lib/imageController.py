from flask import Flask, request, jsonify
import detect_circles

app = Flask(__name__)

# @app.route('/process-image', methods=['POST'])
# def process_image():
#     # try:
#         # Request'ten imagePath al
#         image_path = request.json.get('imagePath')
#         print(image_path)
#         # Python kodunu çalıştır
#         result = subprocess.run(
#             ['python', detect_circles, image_path], capture_output=True,
#     text=True,
#     timeout=60 
#         )
#         print(result)
#         # Python'dan dönen veriyi al
#         if result.returncode == 0:
#             output = result.stdout
#             # JSON formatında dönen veriyi parse et
#             circles = json.loads(output)
#             print(circles)
#             return jsonify(circles)
#         else:
#             error_message = result.stderr  # Hata mesajını al
#             return jsonify({"error": f"Error processing image: {error_message}"}), 500
#     # except Exception as e:
#     #     print(e)
#     #     return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(host='localhost', port=5001,debug=True)

@app.route('/process-image', methods=['POST'])
def process_image():
    # imagePath parametresini JSON'dan al
    image_path = request.json.get('imagePath')
    print(image_path)

    # detect_circles modülündeki fonksiyonu çağır
    try:
        circles = detect_circles.process_image(image_path)
        
        if "error" in circles:
            return jsonify(circles), 400

        return jsonify(circles)
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='localhost', port=5001, debug=True)
    