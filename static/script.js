const dropzone = document.getElementById("drop-zone");
const fileInput = document.getElementById("file-input");

dropzone.addEventListener("dragover", (e) => {
  e.preventDefault();
  dropzone.classList.add("dragover");
});

dropzone.addEventListener("dragleave", () => {
  dropzone.classList.remove("dragover");
});

dropzone.addEventListener("drop", (e) => {
  e.preventDefault();
  dropzone.classList.remove("dragover");
  const files = e.dataTransfer.files;
  uploadfiles(files);
});

fileInput.addEventListener("change", (e) => {
  uploadfiles(fileInput.files);
});

dropzone.addEventListener("click", () => {
  fileInput.click();
});

function uploadfiles(files = fileInput.files) {
  const formData = new FormData();
  const progressBar = document.getElementById("progress-bar");

  for (let file of files) {
    formData.append("files", file);
  }

  const xhr = new XMLHttpRequest();

  xhr.open("POST", "/upload", true);

  xhr.upload.addEventListener("progress", (e) => {
    if (e.lengthComputable) {
      const percent = (e.loaded / e.total) * 100;

      const elapsed = (Date.now() - startTime) / 1000;

      const speed = elapsed > 0 ? e.loaded / elapsed : 0;

      const remaining = (e.total - e.loaded) / speed;

      document.getElementById("upload-stats").innerText = `

        ${(speed / 1024 / 1024).toFixed(2)} MB/s
        • ETA: ${remaining.toFixed(1)}s
        `;
      progressBar.style.width = percent + "%";
    }
  });

  xhr.onload = () => {
    progressBar.style.width = "0%";
    // location.reload();
  };
  const startTime = Date.now();
  xhr.send(formData);
}

const socketio = io();

socketio.on("file_updated", (files) => {
  const filelist = document.querySelector(".file-list");
  filelist.innerHTML = "";
  files.forEach((file) => {
    const li = document.createElement("li");
    li.className = "file-item";
    li.innerHTML = `
    <div>
            <a href="/generate-link/${file.stored_name}">${file.name}</a>
            <span class="size">${file.size}</span>
          </div>
          <div class="actions">

    <button

        type="button"

        class="preview-btn"

        onclick="
            previewFile(
                '${file.stored_name}',
                '${file.type}'
            )
        "
    >
        Preview
    </button>

    <form
        action="/delete/${file.id}"
        method="post"
    >

        <button class="delete-btn">
            Delete
        </button>

    </form>

</div>
    `;
    filelist.appendChild(li);
  });
});

function previewFile(filename, type) {
  const modal = document.getElementById("preview-modal");
  const area = document.getElementById("preview-area");

  area.innerHTML = "";

  const url = `/preview/${filename}`;

  if (type === "image") {
    area.innerHTML = `
            <img
                src="${url}"
                class="preview-image"
            >
        `;
  } else if (type === "video") {
    area.innerHTML = `
            <video
                controls
                class="preview-video"
            >
                <source src="${url}">
            </video>
        `;
  } else if (type === "pdf") {
    area.innerHTML = `
            <iframe
                src="${url}"
                class="preview-pdf"
            ></iframe>
        `;
  } else if (type === "text") {
    fetch(url)
      .then((res) => res.text())
      .then((data) => {
        area.innerHTML = `
                    <pre class="preview-text">
${data}
                    </pre>
                `;
      });
  } else {
    area.innerHTML = `
            <p>
                Preview not supported
            </p>
        `;
  }

  modal.style.display = "flex";
}

document.getElementById("close-preview").addEventListener("click", () => {
  document.getElementById("preview-modal").style.display = "none";
});

const searchInput = document.getElementById("search-input");

searchInput.addEventListener("input", () => {
  const value = searchInput.value.toLowerCase();

  const items = document.querySelectorAll(".file-item");

  items.forEach((item) => {
    const text = item.innerText.toLowerCase();

    if (text.includes(value)) {
      item.style.display = "flex";
    } else {
      item.style.display = "none";
    }
  });
});

const aiSearch = document.getElementById("ai-search");

aiSearch.addEventListener("input", async () => {
  const query = aiSearch.value;
  const response = await fetch(`/search?q=${query}`);

  const results = await response.json();
  console.log(results);

  const items = document.querySelectorAll(".file-item");

  items.forEach((item) => {
    const filename = item.querySelector("a").innerHTML.trim();

    if (results.some((result) => result.trim() === filename) || query === "") {
      item.style.display = "flex";
    } else {
      item.style.display = "none";
    }
  });
});
