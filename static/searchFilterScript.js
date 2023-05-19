searchFilterScript();

function searchFilterScript() {
    const buttonIds = ["groupDescription", "groupName", "userName", "userBio", "postContent", "postTitle"];

    for (const buttonId of buttonIds) {
        addFuncToButton(buttonId, buttonIds);
    }
}

function addFuncToButton(buttonId, buttonIds) {
    const button = document.getElementById(buttonId);
    button.addEventListener("click", () => {
        hideAllDisplayDivs(buttonIds);
        const displayResultDiv = document.getElementById(`${buttonId}Div`);
        displayResultDiv.style.display = "block";
    })
}

function hideAllDisplayDivs(buttonIds) {
    for (const buttonId of buttonIds) {
        const displayResultDiv = document.getElementById(`${buttonId}Div`);
        displayResultDiv.style.display = "none";
    }
}
