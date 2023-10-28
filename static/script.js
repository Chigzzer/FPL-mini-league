var divItems = document.getElementsByClassName("bingo-cell");
let instructionsShown = false;


function selected(item) {
    if (item.style.backgroundColor == 'green'){
        item.style.backgroundColor = 'red';
    }
    else{
        item.style.backgroundColor = 'green';
    }
}


function showInstructions(){
    console.log(instructionsShown)
    const section = document.getElementById('instructions');
    if (instructionsShown == false) {
        section.style.display = 'flex';
        instructionsShown = true;
    }
    else {
        section.style.display = 'none';
        instructionsShown = false;
    }
}
