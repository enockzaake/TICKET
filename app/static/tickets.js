// Check if any div elements are stored in local storage and add them to the DOM on page load
window.addEventListener('load', function() {
  const storedDivs = localStorage.getItem('myDivs');
  if (storedDivs) {
    const divContainer = document.getElementById('div-container');
    divContainer.innerHTML = storedDivs;
    
    // add event listeners to delete buttons for each div
    const deleteBtns = document.querySelectorAll('.delete-btn');
    deleteBtns.forEach(function(btn) {
      btn.addEventListener('click', function() {
        const div = this.parentNode;
        div.parentNode.removeChild(div);
        storeDivs();
      });
    });
  }
});

// add event listener to create button
const createBtn = document.getElementById('create-btn');
createBtn.addEventListener('click', function() {
  const divContainer = document.getElementById('div-container');
  const div = document.createElement('div');
  div.classList.add('styled-div');
  
  // add content to new div
  const text = document.createElement('span');
  text.innerHTML = ` 
  <table>
  <tr>
    <td><input type="text" placeholder="ticket name" name="ticket_name" style="width:220px"></td>
    <td><input type="number" placeholder="price" name="ticket_price"></td>
    <td><input type="number" placeholder="quantity" name="ticket_quantity"></td>
  </tr>
</table>
            `;


  div.appendChild(text);
  
  // add delete button for new div
  const deleteBtn = document.createElement('button');
  deleteBtn.innerHTML = 'Delete Element';
  deleteBtn.classList.add('delete-btn');
  deleteBtn.addEventListener('click', function() {
    const div = this.parentNode;
    div.parentNode.removeChild(div);
    storeDivs();
  });
  div.appendChild(deleteBtn);
  
  divContainer.appendChild(div);
  storeDivs();
});

// add event listener to delete all button
const deleteAllBtn = document.getElementById('delete-all-btn');
deleteAllBtn.addEventListener('click', function() {
  const divContainer = document.getElementById('div-container');
  divContainer.innerHTML = '';
  localStorage.removeItem('myDivs');
  count=1;
});

// store all div elements in local storage
function storeDivs() {
  const divContainer = document.getElementById('div-container');
  const divs = divContainer.querySelectorAll('.styled-div');
  let divsHtml = '';
  divs.forEach(function(el) {
    divsHtml += el.outerHTML;
  });
  localStorage.setItem('myDivs', divsHtml);
}