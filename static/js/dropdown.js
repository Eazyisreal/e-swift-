const dropDown = document.getElementById('dropdown');
const dropDownDetails = document.getElementById('dropdown-details')


function toggleDropDown(){
    dropDownDetails.classList.toggle('visible')
}

dropDown.addEventListener('click', toggleDropDown);