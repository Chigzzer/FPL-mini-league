var divItems = document.getElementsByClassName("bingo-cell");
function selected(item) {
    if (item.style.backgroundColor == 'green'){
        item.style.backgroundColor = 'red';
    }
    else{
        item.style.backgroundColor = 'green';
    }
}