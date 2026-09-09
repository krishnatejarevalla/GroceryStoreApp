const customerNameInput =
    document.getElementById("customer-name");

const createOrderButton =
    document.getElementById("create-order-button");

const orderMessage =
    document.getElementById("order-message");

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

const cartContainer =
    document.getElementById("cart-container");

let cart = [];
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

            <label>
                Quantity:
                <input
                    type="number"
                    class="quantity-input"
                    min="0"
                    step="${product.UOM.toLowerCase() === "kg" ? "0.1" : "1"}"
                    value="0"
                    data-product-id="${product.ProductID}"
                >
            </label>

            <button
                class="add-cart-button"
                data-product-id="${product.ProductID}"
            >
                Add to Cart
            </button>
        `;

        productsContainer.appendChild(productCard);
                const addButton =
        productCard.querySelector(".add-cart-button");

        addButton.addEventListener("click", () => {

            const quantityInput =
                productCard.querySelector(".quantity-input");

            const quantity =
                parseFloat(quantityInput.value);

            if (quantity <= 0) {

                alert("Please enter a quantity greater than 0.");

                return;
            }

            addToCart({
                ProductID: product.ProductID,
                Name: product.Name,
                Price: product.Price,
                UOM: product.UOM,
                Quantity: quantity
            });

            quantityInput.value = 0;
        });
    });
}

function addToCart(product) {

    const existingItem = cart.find(
        item => item.ProductID === product.ProductID
    );

    if (existingItem) {

        existingItem.Quantity += product.Quantity;

    } else {

        cart.push(product);
    }

    displayCart();
}

function displayCart() {

    cartContainer.innerHTML = "";

    if (cart.length === 0) {

        cartContainer.innerHTML =
            "<p>Your cart is empty.</p>";

        return;
    }

    let total = 0;

    cart.forEach(item => {

        const itemTotal =
            item.Price * item.Quantity;

        total += itemTotal;

        const cartItem =
            document.createElement("div");

        cartItem.className = "cart-item";

        cartItem.innerHTML = `
            <p>
                <strong>${item.Name}</strong>
            </p>

            <p>
                Quantity: ${item.Quantity} ${item.UOM}
            </p>

            <p>
                Price: ₹${item.Price}
            </p>

            <p>
                Item Total: ₹${itemTotal}
            </p>
        `;

        cartContainer.appendChild(cartItem);
    });

    const totalElement =
        document.createElement("h3");

    totalElement.textContent =
        `Total: ₹${total}`;

    cartContainer.appendChild(totalElement);
}

async function createOrder() {

    const customerName =
        customerNameInput.value.trim();

    if (!customerName) {

        orderMessage.textContent =
            "Customer name is required.";

        return;
    }

    if (cart.length === 0) {

        orderMessage.textContent =
            "Your cart is empty.";

        return;
    }

    const orderData = {
        CustomerName: customerName,

        Items: cart.map(item => ({
            ProductID: item.ProductID,
            Quantity: item.Quantity
        }))
    };

    orderMessage.textContent =
        "Creating order...";

    try {

        const response = await fetch(
            "/api/orders",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(orderData)
            }
        );

        const result =
            await response.json();

        if (!response.ok) {

            throw new Error(
                result.message || "Failed to create order"
            );
        }

        orderMessage.textContent =
            `Order created successfully! Order ID: ${result.OrderID}. Total: ₹${result.TotalAmount}`;

        cart = [];

        displayCart();

        customerNameInput.value = "";

    } catch (error) {

        orderMessage.textContent =
            error.message;

        console.error(error);
    }
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

createOrderButton.addEventListener(
    "click",
    createOrder
);



loadProducts();