var canvas = document.getElementById('myCanvas');
var floorImage;
var radius = 10;
var context = canvas.getContext('2d');

var preloadImages = function(){
    floorImage = new Image();
    floorImage.src="http://127.0.0.1:5000/static/"+floor+".jpg";
    floorImage.onload = function(){
        canvas.width = floorImage.width;
        canvas.height = floorImage.height;
        context.clearRect(0, 0, canvas.width, canvas.height);
        context.drawImage(floorImage,0,0);
        context.beginPath();
        context.arc(coords[0], coords[1], radius, 0, 2 * Math.PI, false);
        context.fillStyle = 'red';
        context.fill();
        context.lineWidth = 3;
        context.strokeStyle = 'black';
        context.stroke();
    }
}

window.onload = preloadImages;