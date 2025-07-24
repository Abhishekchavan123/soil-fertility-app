const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const snap = document.getElementById('snap');
const webcamResult = document.getElementById('webcam-result');
const ctx = canvas.getContext('2d');

// Get webcam
navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => { video.srcObject = stream; })
    .catch(err => console.error('Webcam error:', err));

snap.addEventListener('click', () => {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    const dataURL = canvas.toDataURL('image/png');

    fetch('/save_photo', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ image: dataURL })
    })
    .then(res => res.json())
    .then(data => {
        webcamResult.innerHTML = `📷 Prediction: <b>${data.prediction}</b><br><img src="${data.path}" width="300">`;
    })
    .catch(err => console.error('Prediction error:', err));
});
