// Define a function to fetch categories from TheMealDB API
async function fetchCuisines() {
    try {
        const response = await fetch('https://www.themealdb.com/api/json/v1/1/categories.php?apikey=1');
        const data = await response.json();
        return data.categories;
    } catch (error) {
        console.error('Error fetching cuisines:', error);
        return [];
    }
}

// Define a function to render categories
async function renderCiusines() {
    const categories = await fetchCuisines();
    // Render categories using the fetched data
    // For example, you can create HTML elements dynamically and append them to the DOM
    const cuisineList = document.getElementById('cuisine-list');
    cuisines.forEach(cuisine => {
        const listItem = document.createElement('li');
        listItem.textContent = cuisine.strCuisine;
        cuisineList.appendChild(listItem);
    });
}

// Call the renderCategories function to fetch and render categories
renderCiusines();