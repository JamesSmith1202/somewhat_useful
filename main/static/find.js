var canvas = document.getElementById('myCanvas');
var mouseX;
var mouseY;
var radius = 10;
var context = canvas.getContext('2d');
var background = new Image();
var drop = document.getElementById('dropdown');

var changePic = function(e){
    console.log("calling");
    var selection = drop.options[drop.selectedIndex].value;
    if (selection == "gm"){
	background.src = "https://hypb.imgix.net/image/ht/2014/06/check-out-savons-remix-of-the-yeet-vine-we-up-yah-0.jpg?w=960&q=90&fit=max&auto=compress%2Cformat";
    }
    if(selection == "bm"){
	background.src = "https://images-na.ssl-images-amazon.com/images/I/51FFG4iz1FL._SX355_.jpg";
    }
    context.clearRect(0, 0, canvas.width, canvas.height);
    canvas.width = background.width;
    canvas.height = background.height;
    context.drawImage(background,0,0);
}

var placeDot = function(e){
    context.clearRect(0, 0, canvas.width, canvas.height);
    context.drawImage(background,0,0);
    var bounds = canvas.getBoundingClientRect();
    mouseX = e.pageX - bounds.left - scrollX;
    mouseY = e.pageY - bounds.top - scrollY;
    context.beginPath();
    context.arc(mouseX, mouseY, radius, 0, 2 * Math.PI, false);
    context.fillStyle = 'red';
    context.fill();
    context.lineWidth = 5;
    context.strokeStyle = '#003300';
    context.stroke();
}

canvas.addEventListener("click", placeDot);
drop.addEventListener("change", changePic);

