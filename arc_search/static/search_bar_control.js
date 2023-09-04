var eanExact = true;
var nameSearch = false;
var eanSearch = false;
var basketMode = false

const searchButtonImages = {
    'exact-ean-btn': ['/static/search_btn_images/exact_ean_off.png', '/static/search_btn_images/exact_ean_on.png'],
    'name-search-btn': ['/static/search_btn_images/name_search_off.png', '/static/search_btn_images/name_search_on.png'],
    'ean-search-btn': ['/static/search_btn_images/ean_search_off.png', '/static/search_btn_images/ean_search_on.png'],
    'basket-btn': ['/static/search_btn_images/basket_off.png', '/static/search_btn_images/basket_on.png']
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
    setSearchImage('basket-btn', basketMode);
};

function isTableEmpty(table) {
    const rows = table.getElementsByTagName("tr");
    // Exclude the header row by starting the loop from index 1
    for (let i = 1; i < rows.length; i++) {
      if (rows[i].getElementsByTagName("td").length > 0) {
        return false; // Table is not empty
      }
    }
    return true; // Table is empty
  }

function clickExactEAN() {
    if (eanExact == false) {
        eanExact = true;
        nameSearch = false;
        eanSearch = false;
        basketMode = false;
        updateAllSearchImages();
        var ean_input = document.getElementById("search-field-typebox");
        ean_input.value = "";
        ean_input.placeholder = "EAN";

        const compTable = document.getElementById("search-result-table");
        if (isTableEmpty(compTable) == false) {
            var specContainer = document.getElementById("specContainer");
            var componentContainer = document.getElementById("componentContainer");
            componentContainer.style.visibility = "visible";
            specContainer.style.display = "none";
        };

        var basketContainer = document.getElementById("basketContainer");
        basketContainer.style.display = 'none';

    } else {};
}

function clickNameSearch() {
    if (nameSearch == false) {
        eanExact = false;
        nameSearch = true;
        eanSearch = false;
        basketMode = false;
        updateAllSearchImages();
        var ean_input = document.getElementById("search-field-typebox");
        ean_input.value = "";
        ean_input.placeholder = "NAME";

        const specTable = document.getElementById("spec-search-result-table");
        if (isTableEmpty(specTable) == false) {
            var specContainer = document.getElementById("specContainer");
            var componentContainer = document.getElementById("componentContainer");
            componentContainer.style.visibility = "hidden";
            specContainer.style.display = "block";
        };

        var basketContainer = document.getElementById("basketContainer");
        basketContainer.style.display = 'none';

    } else {};
}

function clickEANSearch() {
    if (eanSearch == false) {
        eanExact = false;
        nameSearch = false;
        eanSearch = true;
        basketMode = false;
        updateAllSearchImages();
        var ean_input = document.getElementById("search-field-typebox");
        ean_input.value = "";
        ean_input.placeholder = "EAN";

        const specTable = document.getElementById("spec-search-result-table");
        if (isTableEmpty(specTable) == false) {
            var specContainer = document.getElementById("specContainer");
            var componentContainer = document.getElementById("componentContainer");
            componentContainer.style.visibility = "hidden";
            specContainer.style.display = "block";
        };

        var basketContainer = document.getElementById("basketContainer");
        basketContainer.style.display = 'none';

    } else {};
}

function clickBasketMode() {
    if (basketMode == false) {
        eanExact = false;
        nameSearch = false;
        eanSearch = false;
        basketMode = true;
        updateAllSearchImages();
        var ean_input = document.getElementById("search-field-typebox");
        ean_input.value = "";
        ean_input.placeholder = "Key Phrase";

        var basketContainer = document.getElementById("basketContainer");
        basketContainer.style.display = 'block';

    } else {};
}