"use strict";

document.addEventListener("DOMContentLoaded", init);

function init(){
	document.addEventListener("click", removeText);
}

function removeText(e){
	if (!e.target.closest("#user-texts button")) return;
	const textId = parseInt(e.target.getAttribute("data-id"));
	fetch("/delete-text", {
    method: "DELETE",
    body: JSON.stringify({ textId:textId }),
  }).then((res) => {
    window.location.href = "/";
  });
}