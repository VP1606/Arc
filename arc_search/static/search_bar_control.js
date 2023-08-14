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
        var ean_input = document.getElementById("search-field-typebox");
        ean_input.value = "";
        ean_input.placeholder = "EAN";
    } else {};
}

function clickNameSearch() {
    if (nameSearch == false) {
        eanExact = false;
        nameSearch = true;
        eanSearch = false;
        updateAllSearchImages();
        var ean_input = document.getElementById("search-field-typebox");
        ean_input.value = "";
        ean_input.placeholder = "NAME";
    } else {};
}

function clickEANSearch() {
    if (eanSearch == false) {
        eanExact = false;
        nameSearch = false;
        eanSearch = true;
        updateAllSearchImages();
        var ean_input = document.getElementById("search-field-typebox");
        ean_input.value = "";
        ean_input.placeholder = "EAN";
    } else {};
}