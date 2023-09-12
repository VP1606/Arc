var eanExact = true;
var nameSearch = false;
var eanSearch = false;
var basketMode = false;
var scanMode = false;

const modeIconBindings = {
    'exact-ean-btn': ['/static/UI2/img_assets/mode_icons/exact_ean.png', 'Exact EAN', true],
    'name-search-btn': ['/static/UI2/img_assets/mode_icons/name_search.png', 'Name Search', false],
    'ean-search-btn': ['/static/UI2/img_assets/mode_icons/ean_search.png', 'EAN Search', false],
    'basket-btn': ['/static/UI2/img_assets/mode_icons/basket.png', 'Basket', false],
    'scan-btn': ['/static/UI2/img_assets/mode_icons/scan.png', 'Scan', false]
};

function ClickMode(sender) {
    var main_mode_show = document.getElementById("main_mode_show");
    const binding = modeIconBindings[sender.id];

    document.getElementById("main_mode_image").src = binding[0];
    main_mode_show.querySelector('#mode_select_title').textContent = binding[1];
    modeIconBindings[sender.id][2] = true;

    var search_box = document.getElementById("search-field-typebox");
    search_box.value = "";

    if (sender.id == 'exact-ean-btn' || sender.id == 'ean-search-btn') {
        search_box.placeholder = "EAN";
    } else if (sender.id == 'name-search-btn') {
        search_box.placeholder = "Name";
    } else if (sender.id == 'basket-btn') {
        search_box.placeholder = "Key Phrase";
    } else {};
};