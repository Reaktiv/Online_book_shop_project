document.addEventListener("DOMContentLoaded", function () {
    const toggleBtn = document.getElementById("mode-toggle");
    const body = document.body;

    // faqat dark-mode qo‘shamiz, light avto default bo‘lsin
    const currentMode = localStorage.getItem("mode");
    if (currentMode === "dark") {
        body.classList.add("dark-mode");
    }

    toggleBtn.addEventListener("click", function () {
        if (body.classList.contains("dark-mode")) {
            body.classList.remove("dark-mode");
            localStorage.setItem("mode", "light");
        } else {
            body.classList.add("dark-mode");
            localStorage.setItem("mode", "dark");
        }
    });
});
