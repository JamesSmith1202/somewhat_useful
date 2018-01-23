var canvas = document.getElementById('myCanvas');
var floor = {{ floor }};
var coords = {{ coords }}
var floorImage = new Image()
floorImage.src="http://127.0.0.1:5000/static/"+floor+".jpg";
var mouseX;
var mouseY;
var radius = 10;
var context = canvas.getContext('2d');
canvas.width = floorImage.width;
canvas.height = floorImage.height;
context.drawImage(floorImage,0,0);

var placeDot = function(e){
    context.clearRect(0, 0, canvas.width, canvas.height);
    context.drawImage(floorImage,0,0);
    var bounds = canvas.getBoundingClientRect();
    context.beginPath();
    context.arc(coords[0], coords[1], radius, 0, 2 * Math.PI, false);
    context.fillStyle = 'red';
    context.fill();
    context.lineWidth = 5;
    context.strokeStyle = '#003300';
    context.stroke();
}