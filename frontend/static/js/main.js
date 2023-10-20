const uploadForm = document.getElementById("upload-form");
const imageUpload = document.getElementById("image-upload");
const languageSelect = document.getElementById("language");
const resultImage = document.getElementById("result-image");

imageUpload.addEventListener('change', function(event) {
    const image = event.target.files[0];
    const imageURL = URL.createObjectURL(image);

    // Display the selected image in the "Original Image" section
    document.getElementById('original-image').src = imageURL;
});

uploadForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const formData = new FormData();
    formData.append("file", imageUpload.files[0]);
    formData.append("target_language", languageSelect.value);

    try {
        const response = await fetch("/translate_image/", {
            method: "POST",
            body: formData
        });

        if (response.ok) {
            const data = await response.json();
            resultImage.src = data.result_image; // If result_image is base64 encoded
            resultImage.style.display = "block";
        } else {
            console.error("Failed to translate image.", response.statusText);
        }
    } catch (error) {
        console.error("Error:", error);
    }
});

