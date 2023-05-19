function answersDisplayFunc(anchorTag) {
    answersDiv = anchorTag.parentElement.parentElement.nextElementSibling;
    display = answersDiv.style.display;
    answersDiv.style.display = display == "block" ? "none": "block";
}