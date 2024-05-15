const dropDown = document.getElementById('dropdown');
const dropDownDetails = document.getElementById('dropdown-details')
const sortActive = document.getElementById('sort-active');
const sortCategory = document.getElementById('sort-category');
const sort = document.getElementById('sort');

function toggleDropDown(){
    dropDownDetails.classList.toggle('visible')
}

function toggleCategories(){
    sortCategory.classList.toggle('visible')
    sortActive.classList.toggle('visible')
}


dropDown.addEventListener('click', toggleDropDown);
sort.addEventListener('click', toggleCategories);
