answerScript();

function answerScript() {
    const inputs = document.querySelectorAll("textarea");
    for (const input of inputs) {
        console.log("a");
        applyFuncToInput(input);
    }
}

function applyFuncToInput(input) {
    setRows(input, 1);

    input.addEventListener('focus', () => {
        setRows(input, 8);
    })
    window.addEventListener('click', (e) => {
        if (e.target != input) {
            setRows(input, 1);
        }
    })
}

function setRows(input, rows) {
    input.rows = rows;

    switch (rows) {
        case 1:
            input.placeholder = "Answer";
            break;
        case 10:
            input.placeholder = "";
            break;
    }
}