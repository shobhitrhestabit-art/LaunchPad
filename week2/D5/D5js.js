const contentDiv = document.querySelector(".content");
const searchInput = document.querySelector(".searchbar");
const sortButton = document.querySelector(".srtbtn");

let allProducts = [];
let sortState = "none";   // to toggle sorting

// Fetch products
async function loadProducts() {
    const res = await fetch("https://dummyjson.com/products");
    const data = await res.json();

    allProducts = data.products; 
    displayProducts(allProducts);
}

function displayProducts(products) {
    contentDiv.innerHTML = "";

    products.forEach(p => {
        contentDiv.innerHTML += `
            <div class="product-card">
                <img src="${p.thumbnail}" class="p-img">
                <h3>${p.title}</h3>
                <p>₹${p.price}</p>
                <p>Rating: ${p.rating}</p>
            </div>
        `;
    });
}

loadProducts();


// ⭐ SEARCH FUNCTION
searchInput.addEventListener("input", () => {
    const value = searchInput.value.toLowerCase();

    const filtered = allProducts.filter(product =>
        product.title.toLowerCase().includes(value)
    );

    displayProducts(filtered);
});


// ⭐ SORT BUTTON FUNCTION
function sortbtn() {

    let sorted = [...allProducts];  // copy array

    if (sortState === "none" || sortState === "high") {
        // sort low → high
        sorted.sort((a, b) => a.price - b.price);
        sortState = "low";
        sortButton.innerText = "SORT (Low → High)";
    } 
    else {
        // sort high → low
        sorted.sort((a, b) => b.price - a.price);
        sortState = "high";
        sortButton.innerText = "SORT (High → Low)";
    }

    displayProducts(sorted);
}
