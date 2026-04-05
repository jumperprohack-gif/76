<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Clicker Game</title>

<style>
  body {
    font-family: Arial;
    background: #0f172a;
    color: white;
    text-align: center;
    margin-top: 50px;
  }

  .box {
    background: #1e293b;
    padding: 30px;
    border-radius: 10px;
    display: inline-block;
  }

  button {
    padding: 15px 25px;
    margin: 10px;
    font-size: 16px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
  }

  .main-btn { background: #3b82f6; color: white; }
  .upgrade { background: #22c55e; color: white; }
</style>
</head>

<body>

<div class="box">
  <h1>🎮 Clicker Game</h1>

  <h2 id="score">0</h2>
  <p>Per Click: <span id="perClick">1</span></p>
  <p>Auto Clickers: <span id="auto">0</span></p>

  <button class="main-btn" onclick="clickGame()">CLICK</button>

  <hr>

  <button class="upgrade" onclick="buyUpgrade()">Upgrade Click (Cost: <span id="upgradeCost">10</span>)</button>
  <br>
  <button class="upgrade" onclick="buyAuto()">Auto Clicker (Cost: <span id="autoCost">50</span>)</button>
</div>

<script>
let score = localStorage.getItem("score") ? parseInt(localStorage.getItem("score")) : 0;
let perClick = localStorage.getItem("perClick") ? parseInt(localStorage.getItem("perClick")) : 1;
let auto = localStorage.getItem("auto") ? parseInt(localStorage.getItem("auto")) : 0;

let upgradeCost = 10;
let autoCost = 50;

function updateUI() {
  document.getElementById("score").innerText = score;
  document.getElementById("perClick").innerText = perClick;
  document.getElementById("auto").innerText = auto;
  document.getElementById("upgradeCost").innerText = upgradeCost;
  document.getElementById("autoCost").innerText = autoCost;
}

function clickGame() {
  score += perClick;
  save();
  updateUI();
}

function buyUpgrade() {
  if (score >= upgradeCost) {
    score -= upgradeCost;
    perClick++;
    upgradeCost = Math.floor(upgradeCost * 1.5);
    save();
    updateUI();
  }
}

function buyAuto() {
  if (score >= autoCost) {
    score -= autoCost;
    auto++;
    autoCost = Math.floor(autoCost * 1.8);
    save();
    updateUI();
  }
}

function save() {
  localStorage.setItem("score", score);
  localStorage.setItem("perClick", perClick);
  localStorage.setItem("auto", auto);
}

setInterval(() => {
  score += auto;
  save();
  updateUI();
}, 1000);

updateUI();
</script>

</body>
</html>
