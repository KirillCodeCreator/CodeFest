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
    const messageBox = document.getElementById('message-box');
    const sendIcon = document.querySelector('.send-icon');
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

                    // Возвращаем форму в исходное состояние
                    messageBox.placeholder = "Запишите голосовое сообщение";
                    messageBox.classList.remove('recording');
                    sendIcon.src = '../styles/voice.svg';
                    isRecording = false;
                };

                mediaRecorder.start();
                messageBox.placeholder = "Идёт запись голосового сообщения";
                messageBox.classList.add('recording');
                sendIcon.src = '../styles/voice2.svg';
                isRecording = true;
            } else {
                mediaRecorder.stop();
            }
        });
    } else {
        console.error('getUserMedia not supported on your browser!');
    }
});
