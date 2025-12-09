function callAPI() {
  fetch("/api/time")
    .then(res => res.json())
    .then(data => {
      document.getElementById("response").innerHTML = "Server Time: " + data.time;
    });
}
