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

dropzone.addEventListener('click', ()=>{
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
      progressBar.style.width = percent + "%";
    }
  });

  xhr.onload = () => {
    progressBar.style.width = "0%";
    location.reload();
  };

  xhr.send(formData);
}
