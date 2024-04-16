const photoUpload = document.getElementById("photo-upload");
const uploadButton = document.getElementById("upload-button");
const photoPreview = document.getElementById("photo-preview");

uploadButton.addEventListener("click", function() {
      photoUpload.click();
    });

photoUpload.addEventListener("change", function() {
      const file = this.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = function(event) {
          photoPreview.src = event.target.result;
        };
        reader.readAsDataURL(file);
      }
    });