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
});
