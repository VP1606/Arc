function do_search() {
    var searchEAN = document.getElementById("search-field-typebox").value;
    // searchEAN = "5024993732477";
    // console.log(searchEAN);

    var returnDumper = document.getElementById("return-dump");
    returnDumper.textContent = "-----LOADING-----";

    var loaderUI = document.getElementById("loader-wheel")
    var searchButton = document.getElementById("search-button-clicker")

    loaderUI.style.display = "block";
    searchButton.style.display = "none";
    document.getElementById('componentContainer').innerHTML = '';

    var url = `/search_all?id=iahfiasfdosai2313212**7613&ean=${encodeURIComponent(searchEAN)}&product_name=?`

    fetch(url, {
        method: "GET"
    })
    .then((response) => response.json())
    .then((json) => {
        console.log(json);
        returnDumper.textContent = JSON.stringify(json);

        jsonHandler(json);

        loaderUI.style.display = "none";
        searchButton.style.display = "block";
    });
}

function jsonHandler(data) {
    // BESTWAY
    const bestway = data.bestway;
    if ("status" in bestway) {
        console.log("Error detected in Bestway.")
    } else {
        createComponent(
            "Bestway", "OK", bestway.item_name, bestway.ean, bestway.supplier_code, bestway.rsp, 
            bestway.wholesale_unit_size, bestway.wholesale_price
        );
    }

    // BOOKER
    const booker = data.booker;
    if ("status" in booker) {
        console.log("Error detected in Booker.")
    } else {
        createComponent(
            "Booker", "OK", booker.item_name, booker.ean, booker.supplier_code, booker.rsp, 
            booker.wholesale_unit_size, booker.wholesale_price
        );
    }

    // PARFETTS
    const parfetts = data.parfetts;
    if ("status" in parfetts) {
        console.log("Error detected in Parfetts.")
    } else {
        createComponent(
            "Parfetts", "OK", parfetts.item_name, parfetts.ean, "-", parfetts.rsp,
            "-", parfetts.wholesale_price
        );
    }

}

// source, status, name, ean, code, rrp, pack_size, wholesale_price

function createComponent(source, status, name, ean, code, rrp, pack_size, wholesale_price) {
    fetch('/static/search_result.html')
      .then(response => response.text())
      .then(data => {

        data = data.replace("[SOURCE]", source);
        data = data.replace("[STATUS]", status);
        data = data.replace("[NAME]", name);
        data = data.replace("[EAN]", ean);
        data = data.replace("[CODE]", code);
        data = data.replace("[RRP]", rrp);
        data = data.replace("[PCKZ]", pack_size);
        data = data.replace("[WHP]", wholesale_price);

        const component = document.createElement("div");
        component.classList.add("return-component");
        component.innerHTML = data;

        document.getElementById('componentContainer').appendChild(component);
      })
      .catch(error => {
        console.error('Error fetching component:', error);
      });
}