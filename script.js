function predict(){

let avgPoints = document.getElementById("avgPoints").value;
let minutes = document.getElementById("minutes").value;

let points = Math.round(avgPoints * 1.05);
let rebounds = Math.round(minutes * 0.2);
let assists = Math.round(minutes * 0.15);

let pra = points + rebounds + assists;

document.getElementById("points").innerText = points;
document.getElementById("rebounds").innerText = rebounds;
document.getElementById("assists").innerText = assists;
document.getElementById("pra").innerText = pra;

}