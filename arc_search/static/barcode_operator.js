function HitBarcodeConfirm(ean) {
    console.log(ean);
    console.log("STATIC 2");

    var parentWindow = window.parent;

    var exact_ean_button = parentWindow.document.getElementById("exact-ean-btn");
    var ean_input = parentWindow.document.getElementById("search-field-typebox");
    var search_button = parentWindow.document.getElementById("search-button-clicker");

    exact_ean_button.click();
    ean_input.value = ean;
    search_button.click();
};