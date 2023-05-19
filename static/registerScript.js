const COMMON_PASSWORDS = ['123456', 'password', '123456789', '12345678', '12345', '1234567', '1234567890', 'qwerty', 'abc123', '111111', 'admin', 'letmein', 'monkey', 'welcome', 'password1', 'sunshine', 'iloveyou', 'superman', 'princess', 'football']

function maintenance() {
    const pass1 = document.getElementById("id_password1");

    addPassword1CheckFunc(pass1);
    addPassword2CheckFunc(pass1);
    addEmailCheckFunc();
    addNameCheck();
}

function addPassword1CheckFunc(pass1) {
    const alert1 = document.getElementById("password1Alert");
    const charsLi = document.getElementById("chars");
    const numLi = document.getElementById("numeric");
    const commonLi = document.getElementById("common");

    pass1.addEventListener("keyup", () => {
        const pass = pass1.value;
        checkAlertChildrenDisplay(charsLi, numLi, commonLi, pass);
        hideOrShowAlert(alert1);
    })
}

function checkAlertChildrenDisplay(charsLi, numLi, commonLi, pass) {
    charsLi.style.display = pass.length < 8 ? "block" : "none";
    numLi.style.display = /^\d+$/.test(pass) ? "block" : "none";
    commonLi.style.display = COMMON_PASSWORDS.includes(pass) ? "block" : "none";
}

function hideOrShowAlert(alert1) {
    for (const child of alert1.children) {
        if (child.style.display === "block") {
            alert1.style.display = "block";
            return;
        }
        alert1.style.display = "none";
    }
}

function addPassword2CheckFunc(pass1) {
    const pass2 = document.getElementById("id_password2");
    const alert2 = document.getElementById("password2Alert");

    for (const pass of [pass1, pass2]) {
        pass.addEventListener("keyup", () =>{
            const passwordsMatch = pass1.value === pass2.value;
            alert2.style.display =  passwordsMatch ? "none": "block";
        })
    }
}

function addEmailCheckFunc() {
    const emailInput = document.getElementById("id_email");
    const emailAlert = document.getElementById("emailAlert");

    emailInput.addEventListener("keyup", () => {
        const email = emailInput.value;
        const emailIsValid = /^\S+@\S+\.\S+$/.test(email);
        emailAlert.style.display = emailIsValid ? "none" : "block";
    })
}

function addNameCheck() {
    const nameInput = document.getElementById("id_username");
    const nameAlert = document.getElementById("nameAlert");
    nameInput.addEventListener("keyup", () => {
        const name = nameInput.value;
        nameAlert.style.display = names.includes(name) ? "block" : "none";

    })
}