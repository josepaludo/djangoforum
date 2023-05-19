groupSettingsScript();

function groupSettingsScript() {
    addGroupNameValidation();
    copyInviteLinkToClipboard();
}

function addGroupNameValidation() {
    const nameInput = document.getElementById("id_name");
    nameInput.addEventListener("keyup", () =>{
        const name = nameInput.value;
        if (name === GROUP_NAME) {
            return;
        }
        if (INVALID_NAMES.includes(name)) {
            nameInput.classList.add("is-invalid");
        } else {
            nameInput.classList.remove("is-invalid");
        }
    })
}

function copyInviteLinkToClipboard() {
    const button = document.getElementById("inviteLinkModalBtn");
    if (button) {
        button.addEventListener('click', () => {
            const root = window.location.origin;
            const url = button.getAttribute('data-invite-link-id');
            navigator.clipboard.writeText(root+url);
        })
    }
}
