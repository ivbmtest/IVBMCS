
let sidebar = document.querySelector(".sidebar");
let sidebarBtn = document.querySelector(".sidebarBtn");
sidebarBtn.onclick = function () {
  sidebar.classList.toggle("active");
  if (sidebar.classList.contains("active")) {
    sidebarBtn.classList.replace("bx-menu", "bx-menu-alt-right");
  } else sidebarBtn.classList.replace("bx-menu-alt-right", "bx-menu");
};



function simulatePageLoad() {
  document.getElementById('loading-screen').style.display = '';

  // Simulating a 3-second delay (you can adjust this value)
  setTimeout(function () {
      document.getElementById('loading-screen').style.display = 'none';
  }, 1000);
}

// Call the function to simulate page load
simulatePageLoad();


function sndload(){
simulatePageLoad();
}

// select all js

function toggleCheckboxes() {
  var checkAllCheckbox = document.getElementById('selectAll');
  var checkboxes = document.querySelectorAll('.checkbox');
  var okButton = document.getElementById('okButton');

  for (var i = 0; i < checkboxes.length; i++) {
    checkboxes[i].checked = checkAllCheckbox.checked;
  }

  // Enable or disable the OK button based on whether any checkbox is checked
  updateOkButtonState();
}

function updateOkButtonState() {
  var checkboxes = document.querySelectorAll('.checkbox');
  var okButton = document.getElementById('okButton');

  // Enable or disable the OK button based on whether any checkbox is checked
  okButton.disabled = !Array.from(checkboxes).some(checkbox => checkbox.checked);
}

function getCheckedValues() {
  var checkboxes = document.querySelectorAll('.checkbox');
  var checkedValues = [];
 
  for (var i = 0; i < checkboxes.length; i++) {
    if (checkboxes[i].checked) {
      checkedValues.push(checkboxes[i].value);
    }
  }

 
  document.getElementById('tot').innerHTML = checkedValues.length
  // Do something with the checked values, e.g., send them to the server or process them in some way.
}
//  confirm button disabled

function postselectdel() {
  var checkboxes = document.querySelectorAll('.checkbox');
  var checkedValues = [];
 
  for (var i = 0; i < checkboxes.length; i++) {
    if (checkboxes[i].checked) {
      checkedValues.push(checkboxes[i].value);
    }
  }

 
  console.log(checkedValues);
  // Do something with the checked values, e.g., send them to the server or process them in some way.
}