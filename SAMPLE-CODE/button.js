// Get the create div button and div container
const createDivBtn = document.getElementById('create-div');
const divContainer = document.getElementById('div-container');

// Initialize an array to store the created divs
let createdDivs = [];

// Add click event listener to create div button
createDivBtn.addEventListener('click', () => {
    // Create a new div element
    const newDiv = document.createElement('div');

    // Create a new input element to get the div content
    const contentInput = document.createElement('input');
    contentInput.type = 'text';
    contentInput.placeholder = 'Enter div content';
    newDiv.appendChild(contentInput);

    // Create a delete button for the new div
    const deleteBtn = document.createElement('button');
    deleteBtn.textContent = 'Delete Div';
    deleteBtn.addEventListener('click', () => {
    // Remove the div from the array and the DOM
    const index = createdDivs.indexOf(newDivData);
    if (index > -1) {
        createdDivs.splice(index, 1);
    }
    divContainer.removeChild(newDiv);

    // Save the updated list of created divs to local storage
    localStorage.setItem('createdDivs', JSON.stringify(createdDivs));
    });

    // Add the delete button to the new div
    newDiv.appendChild(deleteBtn);

    // Add the new div to the div container
    divContainer.appendChild(newDiv);

    // Add the new div and its content to the created divs array
    const newDivData = { element: newDiv, content: contentInput.value };
    createdDivs.push(newDivData);

    // Save the updated list of created divs to local storage
    localStorage.setItem('createdDivs', JSON.stringify(createdDivs));
});

// On page load, check if there are any divs in local storage and add them to the page
const storedDivs = JSON.parse(localStorage.getItem('createdDivs'));
if (storedDivs && storedDivs.length > 0) {
    storedDivs.forEach(storedDivData => {
    // Create a new div element based on the saved data
    const newDiv = document.createElement('div');

    // Set the content of the div based on the saved data
    const content = storedDivData.content;
    if (content) {
        newDiv.textContent = content;
    }

    // Create a delete button for the new div
    const deleteBtn = document.createElement('button');
    deleteBtn.textContent = 'Delete Div';
    deleteBtn.addEventListener('click', () => {
        // Remove the div from the array and the DOM
        const index = createdDivs.indexOf(storedDivData);
        if (index > -1) {
        createdDivs.splice(index, 1);
        }
        divContainer.removeChild(newDiv);

        // Save the updated list of created divs to local storage
        localStorage.setItem('createdDivs', JSON.stringify(createdDivs));
    });

    // Add the delete button to the new div
    newDiv.appendChild(deleteBtn);

    // Add the new div and its content to the created divs array
    const newDivData = { element: newDiv, content: content };
    createdDivs.push(newDivData);

    // Add the new div to the div container
    divContainer.appendChild(newDiv);
    });
}
