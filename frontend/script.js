const productsContainer =
    document.getElementById("products-container");

const searchInput =
    document.getElementById("search-input");

const searchButton =
    document.getElementById("search-button");

const clearButton =
    document.getElementById("clear-button");

const statusMessage =
    document.getElementById("status-message");


async function loadProducts() {

    statusMessage.textContent = "Loading products...";

    try {

        const response =
            await fetch("/api/products?active=true");

        if (!response.ok) {
            throw new Error("Failed to load products");
        }

        const products =
            await response.json();

        displayProducts(products);

    } catch (error) {

        productsContainer.innerHTML = "";

        statusMessage.textContent =
            "Unable to load products.";

        console.error(error);
    }
}


async function searchProducts() {

    const searchText =
        searchInput.value.trim();

    if (!searchText) {
        loadProducts();
        return;
    }

    statusMessage.textContent =
        "Searching...";

    try {

        const response =
            await fetch(
                `/api/products/search?name=${encodeURIComponent(searchText)}`
            );

        if (!response.ok) {
            throw new Error("Search request failed");
        }

        const products =
            await response.json();

        displayProducts(products);

    } catch (error) {

        productsContainer.innerHTML = "";

        statusMessage.textContent =
            "Unable to search products.";

        console.error(error);
    }
}


function displayProducts(products) {

    productsContainer.innerHTML = "";

    if (products.length === 0) {

        statusMessage.textContent =
            "No products found.";

        return;
    }

    statusMessage.textContent =
        `${products.length} product(s) found.`;

    products.forEach(product => {

        const productCard =
            document.createElement("div");

        productCard.className =
            "product-card";

        productCard.innerHTML = `
            <h3>${product.Name}</h3>

            <p>
                <strong>Price:</strong>
                ₹${product.Price}
            </p>

            <p>
                <strong>Unit:</strong>
                ${product.UOM}
            </p>

            <p>
                <strong>Category:</strong>
                ${product.CategoryName || "Uncategorized"}
            </p>
        `;

        productsContainer.appendChild(productCard);
    });
}


searchButton.addEventListener(
    "click",
    searchProducts
);


clearButton.addEventListener(
    "click",
    () => {

        searchInput.value = "";

        loadProducts();
    }
);


loadProducts();