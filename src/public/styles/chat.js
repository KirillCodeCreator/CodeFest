document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.querySelector(".search-input");
    const searchIcon = document.querySelector(".search-icon");
    const chatItems = document.querySelectorAll(".chat-item");
    let lastActiveChat = document.querySelector(".chat-item.active");

    searchIcon.addEventListener("click", function () {
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
    const themeToggle = document.getElementById('theme-toggle');
    const helpBtn = document.getElementById('help-btn');
    const helpModal = document.getElementById('helpModal');
    const closeBtn = document.querySelector('.close-btn');
    const messagesContainer = document.querySelector('.messages');
    const newChatBtn = document.getElementById('new-chat-btn');
    const newChatModal = document.getElementById('newChatModal');
    const closeNewChatBtn = document.getElementById('close-new-chat-btn');
    const createChatBtn = document.getElementById('create-chat-btn');
    let mediaRecorder;
    let audioChunks = [];
    let isRecording = false;

    // Функция для обновления иконки настроек и логотипа в зависимости от темы
    function updateThemeIcon() {
        const settingsIcon = themeToggle.querySelector('.settings-icon');
        const logo = document.querySelector('.logo');
        if (document.body.classList.contains('dark-theme')) {
            settingsIcon.src = '../styles/sun.svg';
            logo.src = '../styles/logo_dark.svg';
        } else {
            settingsIcon.src = '../styles/moon.svg';
            logo.src = '../styles/logo.svg';
        }
    }

    themeToggle.addEventListener('click', () => {
        document.body.classList.toggle('dark-theme');
        updateThemeIcon();
    });

    helpBtn.addEventListener('click', () => {
        helpModal.style.display = 'block';
    });

    closeBtn.addEventListener('click', () => {
        helpModal.style.display = 'none';
    });

    window.addEventListener('click', (event) => {
        if (event.target == helpModal) {
            helpModal.style.display = 'none';
        }
    });

    newChatBtn.addEventListener('click', () => {
        newChatModal.style.display = 'block';
    });

    closeNewChatBtn.addEventListener('click', () => {
        newChatModal.style.display = 'none';
    });

    createChatBtn.addEventListener('click', () => {
        const chatName = document.getElementById('new-chat-name').value;
        if (chatName) {
            // Перенаправление на новый URL с параметром имени нового чата
            window.location.href = `/add-new-chat?name=${encodeURIComponent(chatName)}`;
        }
    });

    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        recordButton.addEventListener('click', async () => {
            if (!isRecording) {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                mediaRecorder = new MediaRecorder(stream);

                mediaRecorder.ondataavailable = event => {
                    audioChunks.push(event.data);
                };

                mediaRecorder.onstop = async () => {
                    sendIcon.src = '../styles/voice.svg'; // Возвращаем иконку назад
                    messageBox.placeholder = "Запишите голосовое сообщение";
                    messageBox.classList.remove('recording');
                    isRecording = false;

                    const audioBlob = new Blob(audioChunks, { type: 'audio/ogg' });
                    const arrayBuffer = await audioBlob.arrayBuffer();
                    const binaryData = new Uint8Array(arrayBuffer);
                    const chunkSize = 1024 * 512;
                    let base64String = '';

                    for (let i = 0; i < binaryData.length; i += chunkSize) {
                        const chunk = binaryData.subarray(i, i + chunkSize);
                        const chunkString = String.fromCharCode(...chunk);
                        base64String += btoa(chunkString);
                    }

                    const currentTime = new Date();
                    const hours = currentTime.getHours().toString().padStart(2, '0');
                    const minutes = currentTime.getMinutes().toString().padStart(2, '0');
                    const seconds = currentTime.getSeconds().toString().padStart(2, '0');
                    const fileName = `${userId}_${hours}-${minutes}-${seconds}.ogg`;

                    try {
                        const response = await fetch('/save-audio', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({ data: base64String, fileName: fileName, chat_id: chatId })
                        });

                        if (response.ok) {
                            const result = await response.json();
                            console.log("Успешно! Ответ от сервера:", result);

                            // Создаем элемент для сообщения пользователя
                            const messageElement = document.createElement('div');
                            messageElement.className = 'chat-message user';
                            messageElement.textContent = result.transcription;
                            messagesContainer.appendChild(messageElement);

                            // Создаем элемент для сообщения бота
                            const messageBotElement = document.createElement('div');
                            messageBotElement.className = 'chat-message bot';
                            messageBotElement.textContent = result.answer;
                            messagesContainer.appendChild(messageBotElement);

                            // Прокручиваем контейнер сообщений вниз
                            messagesContainer.scrollTop = messagesContainer.scrollHeight;
                        } else {
                            console.error("Ошибка при отправке данных на сервер");
                        }
                    } catch (error) {
                        console.error("Ошибка при отправке данных на сервер:", error);
                    }

                    audioChunks = [];
                };

                mediaRecorder.start();
                messageBox.placeholder = "Идёт запись голосового сообщения";
                messageBox.classList.add('recording');
                sendIcon.src = '../styles/voice2.svg';
                isRecording = true;
            } else {
                sendIcon.src = '../styles/voice.svg'; // Возвращаем иконку назад
                messageBox.placeholder = "Запишите голосовое сообщение";
                messageBox.classList.remove('recording');
                isRecording = false;
                mediaRecorder.stop();
            }
        });
    } else {
        console.error('Обновите Ваш браузер для корректной работы голосового ввода!');
    }

    // Инициализация иконки настроек и логотипа при загрузке страницы
    updateThemeIcon();
});
