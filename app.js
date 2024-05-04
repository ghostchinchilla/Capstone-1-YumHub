// Define a function to render categories
async function renderCuisines() {  // Render categories to a list
    const categories = await fetchCuisines();
    const cuisineList = document.getElementById('cuisine-list');
    if (cuisineList) {
        cuisineList.innerHTML = '';  // Clear existing content
        categories.forEach(category => {
            const listItem = document.createElement('li');
            listItem.textContent = category.strCategory;  // Add category name
            cuisineList.appendChild(listItem);
        });
    } else {
        console.error('Element with ID "cuisine-list" not found.');
    }
}



// Function to fetch categories from TheMealDB API
async function fetchCuisines() {
    console.log('Fetched categories:', categories);

    try {
        const response = await fetch('https://www.themealdb.com/api/json/v1/1/categories.php');  // Correct endpoint
        if (!response.ok) {
            throw new Error('Failed to fetch categories');
        }
        const data = (await response.json()).categories || [];
        return data;
    } catch (error) {
        console.error('Error fetching cuisines:', error);
        return [];
    }
}

// Function to render categories in a dropdown
async function renderCategoryDropdown() {
    const categories = await fetchCuisines();  // Fetch categories
    const categorySelect = document.getElementById('category-select');

    if (categorySelect) {
        categorySelect.innerHTML = '';  // Clear existing content
        categories.forEach(category => {
            const option = document.createElement('option');
            option.value = category.strCategory;
            option.textContent = category.strCategory;
            categorySelect.appendChild(option);
        });

        // Handle dropdown selection
        categorySelect.addEventListener('change', async (e) => {
            const selectedCategory = e.target.value;
            await renderMealsByCategory(selectedCategory);  // Render meals by category
        });
    } else {
        console.error('Element with ID "category-select" not found.');
    }
}


// Call the renderCategoryDropdown function to populate the dropdown
renderCategoryDropdown();  // This triggers the fetching and rendering of categories





async function fetchMealsByCategory(category) {
    try {
        const response = await fetch(`https://www.themealdb.com/api/json/v1/1/filter.php?c=${category}`);
        const data = (await response.json()).meals || [];
        return data;
    } catch (error) {
        console.error(`Error fetching meals for category ${category}:`, error);
        return [];
    }
}



async function renderMealsByCategory(category) {
    const meals = await fetchMealsByCategory(category);  // Fetch meals based on category
    const mealList = document.getElementById('meal-list');  // Reference to the meal list

    if (mealList) {
        mealList.innerHTML = '';  // Clear existing content
        meals.forEach(meal => {  // Loop through meals and add to list
            const listItem = document.createElement('li');  // Create new list item
            listItem.textContent = meal.strMeal;  // Set text content
            mealList.appendChild(listItem);  // Add to the list
        });
    } else {
        console.error('Element with ID "meal-list" not found.');
    }
}




async function fetchMealsByName(mealName) {
    try {
        const response = await fetch(`https://www.themealdb.com/api/json/v1/1/search.php?s=${mealName}`);
        const data = (await response.json()).meals || [];
        return data;
    } catch (error) {
        console.error(`Error fetching meals with name ${mealName}:`, error);
        return [];
    }
}

async function renderMealsByName(mealName) {
    const meals = await fetchMealsByName(mealName);
    const mealSearchResults = document.getElementById('meal-search-results');

    if (mealSearchResults) {
        mealSearchResults.innerHTML = '';  // Clear existing content
        meals.forEach(meal => {
            const listItem = document.createElement('li');
            listItem.textContent = meal.strMeal;  // Add meal name
            mealSearchResults.appendChild(listItem);
        });
    } else {
        console.error('Element with ID "meal-search-results" not found.');
    }
}


