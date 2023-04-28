// create a div element
const div = document.createElement('div');

// set some content for the div
div.innerHTML = 'Hello World';

// add the div to the DOM
document.body.appendChild(div);

// store the div in local storage
localStorage.setItem('myDiv', div.outerHTML);

// get the div element from local storage
const storedDiv = localStorage.getItem('myDiv');

if (storedDiv) {
  // create a temporary div element
  const tempDiv = document.createElement('div');

  // set the stored HTML as the content of the temporary div
  tempDiv.innerHTML = storedDiv;

  // add the temporary div to the DOM
  document.body.appendChild(tempDiv.firstChild);
}
