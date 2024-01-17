
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