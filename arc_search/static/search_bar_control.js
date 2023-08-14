var eanExact = true;
var nameSearch = false;
var eanSearch = false;

const searchButtonImages = {
    'exact-ean-btn': ['/static/search_btn_images/exact_ean_off.png', '/static/search_btn_images/exact_ean_on.png'],
    'name-search-btn': ['/static/search_btn_images/name_search_off.png', '/static/search_btn_images/name_search_on.png'],
    'ean-search-btn': ['/static/search_btn_images/ean_search_off.png', '/static/search_btn_images/ean_search_on.png']
};

function setSearchImage(key, value) {
    const image = document.getElementById(key);
    var index;
    if (value == true) {
        index = 1;
    } else {
        index = 0;
    };
    image.src = searchButtonImages[key][index];
};

function updateAllSearchImages() {
    setSearchImage('exact-ean-btn', eanExact);
    setSearchImage('name-search-btn', nameSearch);
    setSearchImage('ean-search-btn', eanSearch);
};

function clickExactEAN() {
    if (eanExact == false) {
        eanExact = true;
        nameSearch = false;
        eanSearch = false;
        updateAllSearchImages();
        document.getElementById("specContainer").style.display = "none";
    } else {};
}

function clickNameSearch() {
    if (nameSearch == false) {
        eanExact = false;
        nameSearch = true;
        eanSearch = false;
        updateAllSearchImages();
        document.getElementById("specContainer").style.display = "none";
    } else {};
}

function clickEANSearch() {
    if (eanSearch == false) {
        eanExact = false;
        nameSearch = false;
        eanSearch = true;
        updateAllSearchImages();
        document.getElementById("specContainer").style.display = "none";
    } else {};
}