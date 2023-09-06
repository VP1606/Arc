var eanExact = true;
var nameSearch = false;
var eanSearch = false;
var basketMode = false;
var scanMode = false;

const searchButtonImages = {
    'exact-ean-btn': ['/static/search_btn_images/exact_ean_off.png', '/static/search_btn_images/exact_ean_on.png'],
    'name-search-btn': ['/static/search_btn_images/name_search_off.png', '/static/search_btn_images/name_search_on.png'],
    'ean-search-btn': ['/static/search_btn_images/ean_search_off.png', '/static/search_btn_images/ean_search_on.png'],
    'basket-btn': ['/static/search_btn_images/basket_off.png', '/static/search_btn_images/basket_on.png'],
    'scan-btn': ['/static/search_btn_images/scan_off.png', '/static/search_btn_images/scan_on.png']
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
    setSearchImage('scan-btn', scanMode);
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
        scanMode = false;
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

        var scanContainer = document.getElementById("scanContainer");
        scanContainer.style.display = 'none';

        Operate_SC_Content();

    } else {};
}

function clickNameSearch() {
    if (nameSearch == false) {
        eanExact = false;
        nameSearch = true;
        eanSearch = false;
        basketMode = false;
        scanMode = false;
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

        var scanContainer = document.getElementById("scanContainer");
        scanContainer.style.display = 'none';

        Operate_SC_Content();

    } else {};
}

function clickEANSearch() {
    if (eanSearch == false) {
        eanExact = false;
        nameSearch = false;
        eanSearch = true;
        basketMode = false;
        scanMode = false;
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

        var scanContainer = document.getElementById("scanContainer");
        scanContainer.style.display = 'none';

        Operate_SC_Content();

    } else {};
}

function clickBasketMode() {
    if (basketMode == false) {
        eanExact = false;
        nameSearch = false;
        eanSearch = false;
        basketMode = true;
        scanMode = false;
        updateAllSearchImages();
        var ean_input = document.getElementById("search-field-typebox");
        ean_input.value = "";
        ean_input.placeholder = "Key Phrase";

        var basketContainer = document.getElementById("basketContainer");
        basketContainer.style.display = 'block';

        var scanContainer = document.getElementById("scanContainer");
        scanContainer.style.display = 'none';

        Operate_SC_Content();

    } else {};
}

function clickScanMode() {
    if (scanMode == false) {
        eanExact = false;
        nameSearch = false;
        eanSearch = false;
        basketMode = false;
        scanMode = true
        updateAllSearchImages();

        var specContainer = document.getElementById("specContainer");
        var componentContainer = document.getElementById("componentContainer");
        var basketContainer = document.getElementById("basketContainer");

        componentContainer.style.visibility = "hidden";
        specContainer.style.display = "none";
        basketContainer.style.display = 'none';

        var scanContainer = document.getElementById("scanContainer");
        scanContainer.style.display = 'block';

        Operate_SC_Content();
        
    } else {};
}

function Operate_SC_Content() {
    var scanContainer = document.getElementById("scanContainer");
    if (scanMode == true) {
        console.log("Going to Build QR");
        const new_inner = '<iframe src="static/barcode_scan/test.html" frameborder="0" width="100%" height="100%"></iframe>';
        scanContainer.innerHTML = new_inner;
    }

    else {
        console.log("Going to Reset QR");
        scanContainer.innerHTML = '';
    };
}