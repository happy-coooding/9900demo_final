window.addEventListener("load", () => {
    let see = document.querySelector("#see");
    let notsee = document.querySelector("#notsee");
    let username = document.querySelector("#username");
    let passwd = document.querySelector("#passwd");
    let clear = document.querySelectorAll("#clear");
    see.addEventListener("click", () => {
        see.style.display = "none";
        notsee.style.display = "block";
        passwd.setAttribute("type", "text");
    });
    notsee.addEventListener("click", () => {
        see.style.display = "block";
        notsee.style.display = "none";
        passwd.setAttribute("type", "password");
    });
    username.addEventListener("input", () => {
        if (username.value.length != 0) {
            username.nextElementSibling.style.display = "block";
        }
    })
    passwd.addEventListener("input", () => {
        if (passwd.value.length != 0) {
            passwd.nextElementSibling.style.display = "block";
        }
    })
    clear.forEach((clearElement) => {
        clearElement.addEventListener("click", () => {
            clearElement.previousElementSibling.value = "";
            clearElement.style.display = "none";
        })
    })
})