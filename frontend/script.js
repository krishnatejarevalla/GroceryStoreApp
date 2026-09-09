const productsContainer = document.getElementById("products-container");

async function loadProducts() {
    try {
        const response = await fetch("/api/products?active=true");

        if (!response.ok) {
            throw new Error("Failed to load products");
        }

        const products = await response.json();

        productsContainer.innerHTML = "";

        if (products.length === 0) {
            productsContainer.innerHTML = "<p>No products available.</p>";
            return;
        }

        products.forEach(product => {
            const productCard = document.createElement("div");

            productCard.className = "product-card";

            productCard.innerHTML = `
                <h3>${product.Name}</h3>
                <p><strong>Price:</strong> ₹${product.Price}</p>
                <p><strong>Unit:</strong> ${product.UOM}</p>
                <p><strong>Category:</strong> ${product.CategoryName || "Uncategorized"}</p>
            `;

            productsContainer.appendChild(productCard);
        });

    } catch (error) {
        productsContainer.innerHTML =
            "<p>Unable to load products.</p>";

        console.error(error);
    }
}

loadProducts();