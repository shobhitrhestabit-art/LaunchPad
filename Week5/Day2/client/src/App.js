async function loadMessage() {
  const res = await fetch("http://localhost:5000");
  const data = await res.json();
  document.getElementById("root").innerText = data.message;
}

loadMessage();
