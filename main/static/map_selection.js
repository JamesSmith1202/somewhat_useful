var drop = document.getElementById('dropdown');
var canvas = document.getElementById('myCanvas');
var coords = document.getElementById('coords');
var floors=new Array();
var selection = 0;
var mouseX;
var mouseY;
var radius = 10;
var context = canvas.getContext('2d');

var changePic = function(e){
    selection = drop.options[drop.selectedIndex].value;
    context.clearRect(0, 0, canvas.width, canvas.height);
    canvas.width = floors[selection].width;
    canvas.height = floors[selection].height;
    context.drawImage(floors[selection],0,0);
}

var placeDot = function(e){
    context.clearRect(0, 0, canvas.width, canvas.height);
    context.drawImage(floors[selection],0,0);
    var bounds = canvas.getBoundingClientRect();
    mouseX = e.pageX - bounds.left - scrollX;
    mouseY = e.pageY - bounds.top - scrollY;
    context.beginPath();
    context.arc(mouseX, mouseY, radius, 0, 2 * Math.PI, false);
    context.fillStyle = 'red';
    context.fill();
    context.lineWidth = 3;
    context.strokeStyle = 'black';
    context.stroke();
    coords.value = "["+mouseX+","+mouseY+"]";
}

var preloadImages = function(){
    for (i=0;i<11;i++){
        floors[i]=new Image()
        floors[i].src= "http://127.0.0.1:5000/static/" + i + ".jpg";
    }
    floors[0].onload = function(){
        context.drawImage(floors[0],0,0);
    }
}

window.onload = preloadImages;
canvas.addEventListener("click", placeDot);
drop.addEventListener("change", changePic);

