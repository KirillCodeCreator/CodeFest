document.addEventListener("DOMContentLoaded", function() {
    const searchInput = document.querySelector(".search-input");
    const searchIcon = document.querySelector(".search-icon");
    const chatItems = document.querySelectorAll(".chat-item");
    let lastActiveChat = document.querySelector(".chat-item.active");

    searchIcon.addEventListener("click", function() {
        const query = searchInput.value.toLowerCase();
        let found = false;

        chatItems.forEach(item => {
            item.classList.remove("active");
            const text = item.textContent.toLowerCase();
            if (text.includes(query)) {
                item.classList.add("active");
                lastActiveChat = item;
                found = true;
            }
        });

        if (!found && lastActiveChat) {
            lastActiveChat.classList.add("active");
        }
    });

    const recordButton = document.getElementById('record-button');
    const waveContainer = document.getElementById('wave-container');
    const wave = document.getElementById('wave');
    let mediaRecorder;
    let audioChunks = [];
    let isRecording = false;

    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        recordButton.addEventListener('click', async () => {
            if (!isRecording) {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                mediaRecorder = new MediaRecorder(stream);

                mediaRecorder.ondataavailable = event => {
                    audioChunks.push(event.data);
                };

                mediaRecorder.onstop = () => {
                    const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                    const audioUrl = URL.createObjectURL(audioBlob);
                    const audio = new Audio(audioUrl);
                    audio.play();
                    audioChunks = [];
                };

                mediaRecorder.start();
                waveContainer.style.display = 'block';
                isRecording = true;

                const audioContext = new (window.AudioContext || window.webkitAudioContext)();
                const analyser = audioContext.createAnalyser();
                const source = audioContext.createMediaStreamSource(stream);
                source.connect(analyser);
                analyser.fftSize = 256;
                const bufferLength = analyser.frequencyBinCount;
                const dataArray = new Uint8Array(bufferLength);

                const draw = () => {
                    requestAnimationFrame(draw);
                    analyser.getByteTimeDomainData(dataArray);
                    let sum = 0;
                    for (let i = 0; i < bufferLength; i++) {
                        sum += dataArray[i];
                    }
                    const average = sum / bufferLength;
                    wave.style.width = `${average / 2}%`;
                };

                draw();
            } else {
                mediaRecorder.stop();
                waveContainer.style.display = 'none';
                isRecording = false;
            }
        });
    } else {
        console.error('Обновите версию вашего браузера!');
    }
});
