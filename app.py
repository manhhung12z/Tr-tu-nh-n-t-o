from flask import Flask, render_template, request, jsonify, url_for
from ultralytics import YOLO
import os
import cv2
from werkzeug.utils import secure_filename 
import uuid
UPLOAD_FOLDER ='static/uploads'
RESULT_FOLDER = "static/results"
#để nhận được request.files , nếu nhận từ form  thì request.form , nhận dữ liệu từ json thì request.json
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

app=Flask(__name__) #Khoi tao ung dung Flask biến name giúp flask biết nơi để tìm các tệp tin và tài nguyên khác nhau như template và static files.
model=YOLO("best.pt") 
#khai báo bệnh biện pháp và giải pháp
DISEASE_INFO = {

    "Apple Scab Leaf": {
        "severity": "Trung bình",
        "affected_parts": "Lá",
        "symptoms": "Lá xuất hiện đốm nâu đen và sần sùi.",
        "solutions": [
            {
                "title": "Thuốc trừ nấm",
                "description": "Phun Mancozeb 80WP hoặc Dithane M-45."
            }
        ]
    },

    "Apple rust leaf": {
        "severity": "Trung bình",
        "affected_parts": "Lá",
        "symptoms": "Lá có đốm vàng cam giống gỉ sắt.",
        "solutions": [
            {
                "title": "Thuốc trừ nấm",
                "description": "Phun Score 250EC hoặc Anvil 5SC."
            }
        ]
    },

    "Bell_pepper leaf spot": {
        "severity": "Trung bình",
        "affected_parts": "Lá",
        "symptoms": "Lá xuất hiện các đốm nâu hoặc đen.",
        "solutions": [
            {
                "title": "Thuốc phòng trị",
                "description": "Phun Coc 85WP hoặc Kasumin 2L."
            }
        ]
    },

    "Corn Gray leaf spot": {
        "severity": "Trung bình",
        "affected_parts": "Lá",
        "symptoms": "Lá có các vết dài màu xám.",
        "solutions": [
            {
                "title": "Thuốc trừ nấm",
                "description": "Phun Amistar Top 325SC hoặc Tilt Super 300EC."
            }
        ]
    },

    "Corn leaf blight": {
        "severity": "Nặng",
        "affected_parts": "Lá",
        "symptoms": "Lá xuất hiện các vết cháy dài màu nâu.",
        "solutions": [
            {
                "title": "Thuốc trừ nấm",
                "description": "Phun Nativo 750WG hoặc Tilt Super 300EC."
            }
        ]
    },

    "Corn rust leaf": {
        "severity": "Trung bình",
        "affected_parts": "Lá",
        "symptoms": "Lá có nhiều chấm nâu đỏ.",
        "solutions": [
            {
                "title": "Thuốc trừ nấm",
                "description": "Phun Anvil 5SC hoặc Amistar Top 325SC."
            }
        ]
    },

    "Potato leaf early blight": {
        "severity": "Trung bình",
        "affected_parts": "Lá",
        "symptoms": "Lá có đốm nâu dạng vòng đồng tâm.",
        "solutions": [
            {
                "title": "Thuốc trừ nấm",
                "description": "Phun Mancozeb 80WP hoặc Daconil 75WP."
            }
        ]
    },

    "Potato leaf late blight": {
        "severity": "Nặng",
        "affected_parts": "Lá",
        "symptoms": "Lá thâm đen và lan rất nhanh.",
        "solutions": [
            {
                "title": "Thuốc trừ nấm",
                "description": "Phun Ridomil Gold 68WG hoặc Aliette 800WG."
            }
        ]
    },

    "Squash Powdery mildew leaf": {
        "severity": "Trung bình",
        "affected_parts": "Lá",
        "symptoms": "Lá có lớp bột trắng.",
        "solutions": [
            {
                "title": "Thuốc trừ nấm",
                "description": "Phun Sulfur 80WG hoặc Score 250EC."
            }
        ]
    },

    "Tomato Early blight leaf": {
        "severity": "Trung bình",
        "affected_parts": "Lá",
        "symptoms": "Lá có đốm nâu dạng vòng đồng tâm.",
        "solutions": [
            {
                "title": "Thuốc trừ nấm",
                "description": "Phun Daconil 75WP hoặc Mancozeb 80WP."
            }
        ]
    },

    "Tomato Septoria leaf spot": {
        "severity": "Trung bình",
        "affected_parts": "Lá",
        "symptoms": "Lá có nhiều đốm nhỏ màu xám.",
        "solutions": [
            {
                "title": "Thuốc trừ nấm",
                "description": "Phun Daconil 75WP hoặc Score 250EC."
            }
        ]
    },

    "Tomato leaf bacterial spot": {
        "severity": "Trung bình",
        "affected_parts": "Lá",
        "symptoms": "Lá có đốm đen nhỏ và quầng vàng.",
        "solutions": [
            {
                "title": "Thuốc kháng khuẩn",
                "description": "Phun Coc 85WP hoặc Kasumin 2L."
            }
        ]
    },

    "Tomato leaf late blight": {
        "severity": "Nặng",
        "affected_parts": "Lá",
        "symptoms": "Lá thâm đen, ẩm ướt và lan nhanh.",
        "solutions": [
            {
                "title": "Loại bỏ cây bệnh",
                "description": "Nhổ bỏ cây nhiễm nặng."
            },
            {
                "title": "Thuốc trừ nấm",
                "description": "Phun Ridomil Gold 68WG hoặc Aliette 800WG."
            }
        ]
    },

    "Tomato leaf mosaic virus": {
        "severity": "Nặng",
        "affected_parts": "Lá",
        "symptoms": "Lá loang lổ xanh vàng và biến dạng.",
        "solutions": [
            {
                "title": "Xử lý",
                "description": "Nhổ bỏ cây bệnh và kiểm soát côn trùng truyền virus."
            }
        ]
    },

    "Tomato leaf yellow virus": {
        "severity": "Nặng",
        "affected_parts": "Lá",
        "symptoms": "Lá vàng, xoăn và cây còi cọc.",
        "solutions": [
            {
                "title": "Xử lý",
                "description": "Diệt bọ phấn trắng và loại bỏ cây bệnh."
            }
        ]
    },

    "Tomato mold leaf": {
        "severity": "Trung bình",
        "affected_parts": "Lá",
        "symptoms": "Mặt dưới lá có lớp mốc xám.",
        "solutions": [
            {
                "title": "Thuốc trừ nấm",
                "description": "Phun Antracol 70WP hoặc Nativo 750WG."
            }
        ]
    },

    "Tomato two spotted spider mites leaf": {
        "severity": "Trung bình",
        "affected_parts": "Lá",
        "symptoms": "Lá có chấm vàng và mạng nhện mỏng.",
        "solutions": [
            {
                "title": "Thuốc trừ nhện đỏ",
                "description": "Phun Ortus 5SC hoặc Danitol 10EC."
            }
        ]
    },

    "grape leaf black rot": {
        "severity": "Nặng",
        "affected_parts": "Lá",
        "symptoms": "Lá có đốm tròn màu nâu đen.",
        "solutions": [
            {
                "title": "Thuốc trừ nấm",
                "description": "Phun Mancozeb 80WP hoặc Nativo 750WG."
            }
        ]
    }
}
HEALTHY_INFO = {
    "severity": "Khỏe mạnh",
    "affected_parts": "Lá",
    "symptoms": "Lá cây phát triển bình thường, không phát hiện dấu hiệu bệnh.",
    "solutions": [
        {
            "title": "Khuyến nghị",
            "description": "Tiếp tục chăm sóc, tưới nước hợp lý và theo dõi định kỳ."
        }
    ]
}

HEALTHY_CLASSES = [
    "Apple leaf",
    "Bell_pepper leaf",
    "Blueberry leaf",
    "Cherry leaf",
    "Peach leaf",
    "Potato leaf",
    "Raspberry leaf",
    "Soyabean leaf",
    "Strawberry leaf",
    "Tomato leaf",
    "grape leaf"
]

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/predict', methods=['POST'])
def predict():
    if "file" not in request.files:
        return jsonify({"success": False, "message": "Không có tệp tin nào được tải lên."})
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"success": False, "message": "Tên tệp tin không hợp lệ."})
    ext = file.filename.rsplit(".", 1)[-1].lower()
    filename = secure_filename(file.filename) #Đảm bảo tên tệp tin an toàn bằng cách loại bỏ các ký tự không hợp lệ và ngăn chặn các cuộc tấn công tiêm nhiễm đường dẫn.
    upload_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(upload_path) #Lưu tệp tin đã tải lên vào thư mục uploads với tên tệp tin đã được làm sạch.
    if ext in ["jpg", "jpeg", "png"]:
        return predict_image(upload_path, filename)
    elif ext in ["mp4", "avi", "mov"]:
        return predict_video(upload_path)
    else:
        return jsonify({
            "success": False,
            "message": "Chỉ hỗ trợ ảnh jpg, jpeg, png và video mp4, avi, mov"
        })
def predict_image(upload_path, filename):
    results = model.predict(save=True, source=upload_path, project=os.path.abspath("static"), name="results", exist_ok=True) #Dự đoán bằng mô hình YOLO, lưu kết quả vào thư mục static/results với tên tệp tin đã được làm sạch.
    result_file = os.path.join(RESULT_FOLDER, filename)
    boxes = results[0].boxes
    detected_diseases = []
    if(len(boxes)>0):
        for box in boxes:
            class_id = int(box.cls[0])           # Lấy mã ID của khung hiện tại
            disease_name = model.names[class_id] # Đổi ID thành tên bệnh
            confidence = float(box.conf[0])      # Lấy độ tin cậy của khung hiện tại
            conf_percent = round(confidence * 100, 2)
            info = DISEASE_INFO.get(disease_name, HEALTHY_INFO) # Lấy thông tin bệnh từ DISEASE_INFO, nếu không có thì lấy thông tin khỏe mạnh
            detected_diseases.append({
                "name": disease_name,
                "confidence": conf_percent,
                "severity": info["severity"],
                "affected_parts": info["affected_parts"],
                "symptoms": info["symptoms"],
                "solutions": info["solutions"]
            })
    else:
        disease_name = "Không phát hiện bệnh"
        conf_percent = 0.0
        detected_diseases.append({
            "name": disease_name,
            "confidence": conf_percent
        })
    return jsonify({"success": True, "diseases": detected_diseases, "filename": url_for("static", filename=f"results/{filename}")})
def predict_video(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return jsonify({"success": False, "message": "Không thể mở video."})
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0:
        fps = 25
    result_name = f"{uuid.uuid4()}.mp4"
    result_path = os.path.join(RESULT_FOLDER, result_name)
    fourcc = cv2.VideoWriter_fourcc(*"avc1") #Định nghĩa codec nén video sử dụng để ghi video kết quả. Ở đây, "mp4v" được sử dụng cho định dạng MP4.
    out = cv2.VideoWriter(result_path, fourcc, fps, (width, height)) #Tạo đối tượng VideoWriter để ghi video kết quả với định dạng mp4, tốc độ khung hình và kích thước khung giống như video gốc.
    detections = []
    while True:
        success, frame = cap.read()
        if not success:
            break
        results = model.track(
            frame,
            persist=True,
            conf=0.5,
            verbose=False
        )
        annotated_frame = results[0].plot()
        out.write(annotated_frame)
        
        for box in results[0].boxes:
            class_id = int(box.cls[0])
            disease_name = model.names[class_id]
            confidence = float(box.conf[0])

            detections.append({
                "disease": disease_name,
                "confidence": round(confidence * 100, 2)
            })

    cap.release()
    out.release()
    summary = {}
    for item in detections:
        name = item["disease"]
        if name not in summary:
            summary[name] = {
                "count": 0,
                "total_confidence": 0.0
            }
        summary[name]["count"] += 1
        summary[name]["total_confidence"] += item["confidence"]
    summary_list = []
    for name,data in summary.items():
        if name in HEALTHY_CLASSES:
            info = HEALTHY_INFO
        else:
            info = DISEASE_INFO.get(name, HEALTHY_INFO)
        avg_confidence = round(data["total_confidence"] / data["count"],2)
        summary_list.append({
            "disease": name,
            "count": data["count"],
            "avg_confidence": round(avg_confidence, 2),
            "severity": info["severity"],
            "affected_parts": info["affected_parts"],
            "symptoms": info["symptoms"],
            "solutions": info["solutions"]
        })
    return jsonify({
        "success": True,
        "summary": summary_list,
        "filename": url_for("static", filename=f"results/{result_name}")
    })

if __name__ == "__main__":
    app.run(debug=True,use_reloader=False)



