var searchbar = document.getElementById("searchLocker");
var cards = document.getElementsByClassName("card");

var search = function(e){
    var title;
    var target = searchbar.value;
    for (var i = 0; i < cards.length; i++){
        title = cards[i].lastElementChild.childNodes[1].innerHTML.substr(11);
        if (title.includes(target)){
            cards[i].style.display = "block";
        }
        else{
            cards[i].style.display = "none";
        }
    }
}

searchbar.addEventListener("change", search);