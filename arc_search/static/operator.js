function do_search() {
    console.log("HII2");
    var searchEAN = document.getElementById("search-field-typebox").value;
    // searchEAN = "5024993732477";
    // console.log(searchEAN);

    const UserID = 2;

    var loaderUI = document.getElementById("loader-wheel");
    var searchButton = document.getElementById("search_button");
    var specContainer = document.getElementById("spec-search-container");

    loaderUI.style.display = "block";
    searchButton.style.display = "none";
    // specContainer.style.display = "none";
    specContainer.innerHTML = '';

    // var url = `/search_all?id=iahfiasfdosai2313212**7613&ean=${encodeURIComponent(searchEAN)}&product_name=n&key_id=${UserID}`
    var url = `/test`

    fetch(url, {
        method: "GET"
    })
    .then((response) => response.json())
    .then((json) => {
        console.log(json);

        json = dummySpecData;
        console.log(json);

        fetch('/static/spec_search/spec_page.html')
            .then(response => response.text())
            .then(data => {

                var showing_desc_val = "flex";
                if (OnMobile == true) {
                    showing_desc_val = "flex";
                } else {
                    showing_desc_val = "none";
                };

                data = data.replace("[SHOWING-DESC-HEADER]", showing_desc_val);

                specContainer.innerHTML = data;

                const bestway = json.bestway;
                if ("status" in bestway) {
                    console.log("Error detected in Bestway.")
                } else {
                    var b_price = bestway.wholesale_price;
                    if (b_price == "£0.00") {
                        b_price = "-";
                    };
                    MakeSpecRow("bestway", bestway.ean, bestway.supplier_code, bestway.rsp, bestway.wholesale_unit_size, b_price, bestway.item_name);
                };

                const booker = json.booker;
                if ("status" in booker) {
                    console.log("Error detected in Booker.")
                } else {
                    MakeSpecRow("booker", booker.ean, booker.supplier_code, booker.rsp, booker.wholesale_unit_size, booker.wholesale_price, booker.item_name);
                };

                const parfetts = json.parfetts;
                if ("status" in parfetts) {
                    console.log("Error detected in Parfetts.")
                } else {
                    MakeSpecRow("parfetts", parfetts.ean, parfetts.supplier_code, parfetts.rsp, parfetts.wholesale_unit_size, parfetts.wholesale_price, parfetts.item_name);
                };
            });
        

        loaderUI.style.display = "none";
        searchButton.style.display = "block";
    });
};

function MakeSpecRow(source, ean, code, rrp, pack_size, wholesale_price, name) {
    fetch('/static/spec_search/spec_row.html')
            .then(response => response.text())
            .then(data => {
                data = data.replace("[SUPPLIER-ICON]", `"/static/supplier_logos/${source}-logo.png"`);
                data = data.replace("[EAN]", ean);
                data = data.replace("[CODE]", code);
                data = data.replace("[RRP]", rrp);
                data = data.replace("[PCKZ]", pack_size);
                data = data.replace("[WHP]", wholesale_price);
                data = data.replace("[NAME]", name);

                var showing_name_val = "none";
                if (OnMobile == true) {
                    showing_name_val = "none";
                } else {
                    showing_name_val = "block";
                };

                data = data.replace("[SHOWING-SPEC-NAME]", showing_name_val);

                var main_box = document.getElementById('spec-search-box');
                main_box.innerHTML = main_box.innerHTML + ' ' + data;
            });

    if (OnMobile == true) {
        fetch('/static/spec_search/spec_desc_row.html')
            .then(response => response.text())
            .then(data => {
                data = data.replace("[SUPPLIER-ICON]", `"/static/supplier_logos/${source}-logo.png"`);
                data = data.replace("[NAME]", name);

                var desc_box = document.getElementById('spec-search-desc-box');
                desc_box.innerHTML = desc_box.innerHTML + ' ' + data;
            });
    };
};

var dummySpecData = {
    bestway: {
        ean: "9002490264888",
        item_name: "Red Bull Energy Drink Summer Edition Juneberry 250ml x 12 PM",
        rsp: "£1.45",
        supplier_code: "815170",
        wholesale_price: "£8.75",
        wholesale_unit_size: "250ml × 12 × 1"
    },

    booker: {
        ean: "9002490264888",
        item_name: "Red Bull Energy Drink Summer Edition Juneberry 250ml x 12 PM",
        rsp: "£1.45",
        supplier_code: "285788",
        wholesale_price: "£9.65",
        wholesale_unit_size: "Case of 12"
    },

    parfetts: {
        ean: "9002490264888",
        item_name: "Red Bull Juneberry Summer 2023 Edition £1.45 250ml",
        rsp: "£1.00",
        supplier_code: "121288",
        wholesale_price: "£6.99",
        wholesale_unit_size: "1 x 12"
    }

};