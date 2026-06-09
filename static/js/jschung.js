const uploadBox = document.querySelector(".upload-box");
const fileInput = document.getElementById("fileInput");
const videoBox = document.querySelector(".video-box");
const resultBox = document.querySelector(".right-box");

uploadBox.addEventListener("click", () => {
    fileInput.click();
});
fileInput.addEventListener("change", async function () { //hàm bất đồng bộ  luôn trả về kết quả
    const file = this.files[0];//khi người dùng click vào đối tượng chuyển input file thì  Đối tượng này được mặc định tích hợp sẵn một thuộc tính tên là .files 
    if (!file) {
        return; //cancel thoát
    }
    const formData = new FormData();
    formData.append("file", file);
    videoBox.innerHTML = `<p style="color:white">Đang xử lý...</p>`;
    const response = await fetch("/predict", {
        method: "POST",
        body: formData
    });
    const data = await response.json();
    if (!data.success) {
        alert(data.message);
        return;
    }
    if (file.type.startsWith("image/")) {
        videoBox.innerHTML = `
            <img src="${data.filename}" 
                 style="width:100%;height:100%;object-fit:contain">
        `;
        renderImageResult(data.diseases);
    }
    if (file.type.startsWith("video/")) {
        videoBox.innerHTML = `
            <video controls autoplay muted
                   style="width:100%;height:100%;object-fit:contain">
                <source src="${data.filename}" type="video/mp4">
            </video>
        `;
        renderVideoResult(data.summary);
    }
    //khi đẩy một file lên server xử lý thì có các thuộc tính dùng sẵn 
    //file.filename trả về tên gốc của file người dùng tải lên
})
function createResultCard(name, confidence, severity, affectedParts, symptoms, solutions) {
    let solutionsHTML = "";
    solutions.forEach(solution => {
        solutionsHTML += `
            <div class="solution">
                <h4>${solution.title}</h4>
                <p>${solution.description}</p>
            </div>
        `;
    });
    return ` <div class="result-card">
                    <div class="row">
                        <span>Loại bệnh:</span>
                        <p>${name}</p>
                    </div>

                    <div class="row">
                        <span>Mức độ:</span>
                        <p class="orange">${severity}</p>
                    </div>
                    <div class="row">
                        <span>Độ tin cậy:</span>
                        <p>${confidence}</p>
                    </div>

                    <div class="row">
                        <span>Các bộ phận ảnh hưởng:</span>
                        <p>${affectedParts}</p>
                    </div>

                    <h3>📌 Symptoms</h3>
                    <p>${symptoms}</p>

                    <h3>🌿 giải pháp</h3>
                    ${solutionsHTML}
                </div>`;
}
function renderImageResult(diseases) {
    if (!diseases || diseases.length === 0)
        return;
    resultBox.innerHTML = `
        <div class="timeline-container">
             <h4 style="margin-bottom: 10px; font-size: 15px; color: #8cff9c;"><i class="fa-solid fa-list-check"></i> Các kết quả phát hiện:</h4>
                <div id="timeline-buttons" class="timeline-buttons"></div>
        </div>
        <div id="detail-card-container"></div>
    `;
    const buttonsContainer = document.getElementById("timeline-buttons");
    const detailContainer = document.getElementById("detail-card-container");
    function showDetail(item, clickedButton) {
        const allButtons = buttonsContainer.querySelectorAll('button');
        allButtons.forEach(btn => btn.classList.remove('active'));
        clickedButton.classList.add('active');
        detailContainer.innerHTML = createResultCard(
            item.name, item.confidence + "%", item.severity,
            item.affected_parts, item.symptoms, item.solutions
        );
    }
    diseases.forEach((item, index) => {
        const btn = document.createElement("button");
        btn.className = "btn-timeline";
        btn.innerHTML = `${item.name} (${item.confidence}%)`;
        btn.onclick = () => showDetail(item, btn);
        buttonsContainer.appendChild(btn);
        if (index === 0) showDetail(item, btn);

    });
}
function renderVideoResult(summary) {
    if (!summary || summary.length == 0)
        return;
    resultBox.innerHTML = `
        <div class="timeline-container">
            <h4 style="margin-bottom: 10px; font-size: 15px; color: #8cff9c;"><i class="fa-solid fa-list-check"></i> Các kết quả phát hiện:</h4>
            <div id="timeline-buttons" class="timeline-buttons"></div>
        </div>
        <div id="detail-card-container"></div>
    `;
    const buttonsContainer = document.getElementById("timeline-buttons");
    const detailContainer = document.getElementById("detail-card-container");
    function showDetail(item, clickedButton) {
        const allButtons = buttonsContainer.querySelectorAll('button');
        allButtons.forEach(btn => btn.classList.remove('active'));
        clickedButton.classList.add('active');
        detailContainer.innerHTML = createResultCard(
            item.disease, item.avg_confidence + "%", item.severity,
            item.affected_parts, item.symptoms, item.solutions
        );
    }
    summary.forEach((item, index) => {
        const btn = document.createElement("button");
        btn.className = "btn-timeline";
        btn.innerHTML = `${item.disease} (${item.avg_confidence}%)`;
        btn.onclick = () => showDetail(item, btn);
        buttonsContainer.appendChild(btn);
        if (index === 0) showDetail(item, btn);
    });
}
// xử lý các nút btn
const btnclear = document.getElementById("btnclear");
btnclear.addEventListener("click", () => {

    videoBox.innerHTML = `
        <img src="#" alt="Leaf Image">
    `;

    resultBox.innerHTML = `
        <div class="result-card">
            <div class="row">
                <span>Loại bệnh:</span>
                <p>Chưa có dữ liệu</p>
            </div>

            <div class="row">
                <span>Mức độ:</span>
                <p>--</p>
            </div>

            <div class="row">
                <span>Bộ phận ảnh hưởng:</span>
                <p>--</p>
            </div>

            <h3>📌 Dấu hiệu</h3>
            <p>Vui lòng tải ảnh hoặc video để bắt đầu nhận diện.</p>

            <h3>🌿 Giải pháp</h3>

            <div class="solution">
                <h4>Khuyến nghị</h4>
                <p>Hệ thống sẽ hiển thị kết quả sau khi phân tích.</p>
            </div>
        </div>
    `;

    fileInput.value = "";
});
const btnplay = document.getElementById("btnplay")
btnplay.addEventListener("click", () => {
    const video = videoBox.querySelector("video");
    if(video)
    {
          if (video.paused) {
            video.play();
            btnplay.innerHTML = `<i class="fa-solid fa-pause"></i> Pause`;
    }
    else {
            video.pause();
            btnplay.innerHTML = `<i class="fa-solid fa-play"></i> Play`;
        }
    }

});



