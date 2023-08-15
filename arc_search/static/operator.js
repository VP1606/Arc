function do_search() {
    var searchEAN = document.getElementById("search-field-typebox").value;
    // searchEAN = "5024993732477";
    // console.log(searchEAN);

    var returnDumper = document.getElementById("return-dump");
    returnDumper.textContent = "-----LOADING-----";

    var loaderUI = document.getElementById("loader-wheel");
    var searchButton = document.getElementById("search-button-clicker");
    var componentContainer = document.getElementById("componentContainer");
    var specContainer = document.getElementById("specContainer");

    loaderUI.style.display = "block";
    searchButton.style.display = "none";
    // document.getElementById('componentContainer').innerHTML = '';
    componentContainer.style.visibility = "hidden";
    specContainer.style.display = "none";
    resetTable();

    var url = `/search_all?id=iahfiasfdosai2313212**7613&ean=${encodeURIComponent(searchEAN)}&product_name=?`

    fetch(url, {
        method: "GET"
    })
    .then((response) => response.json())
    .then((json) => {
        console.log(json);
        returnDumper.textContent = JSON.stringify(json);

        jsonHandler(json);

        componentContainer.style.visibility = "visible";
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
        var b_price = bestway.wholesale_price;
        if (b_price == "£0.00") {
          b_price = "-";
        };

        createRow(
            "Bestway", "OK", bestway.item_name, bestway.ean, bestway.supplier_code, bestway.rsp, 
            bestway.wholesale_unit_size, b_price
        );
    }

    // BOOKER
    const booker = data.booker;
    if ("status" in booker) {
        console.log("Error detected in Booker.")
    } else {
        createRow(
            "Booker", "OK", booker.item_name, booker.ean, booker.supplier_code, booker.rsp, 
            booker.wholesale_unit_size, booker.wholesale_price
        );
    }

    // PARFETTS
    const parfetts = data.parfetts;
    if ("status" in parfetts) {
        console.log("Error detected in Parfetts.")
    } else {
        createRow(
            "Parfetts", "OK", parfetts.item_name, parfetts.ean, parfetts.supplier_code, parfetts.rsp,
            parfetts.wholesale_unit_size, parfetts.wholesale_price
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

function createTable() {
    fetch('/static/search_result_tabular.html')
      .then(response => response.text())
      .then(data => {
        const component = document.createElement("div");
        component.classList.add("return-table-component");
        component.innerHTML = data;

        document.getElementById('componentContainer').appendChild(component);
      })
      .catch(error => {
        console.error('Error fetching component:', error);
      });
}

function createRow(source, status, name, ean, code, rrp, pack_size, wholesale_price) {
    fetch('/static/search_result_row.html')
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

        // const component = document.createElement("tr");
        // component.innerHTML = data;

        var table = document.getElementById('search-result-table');
        var newRow = table.insertRow(-1);
        newRow.classList.add("search-return-row");
        newRow.innerHTML = data;
        
      })
      .catch(error => {
        console.error('Error fetching component:', error);
      });
}

function resetTable() {
  // const container = document.getElementById('componentContainer');
  // container.style.display = "none";

  const className = "search-return-row";
  const rowsToDelete = document.querySelectorAll(`.${className}`);

    // Get the reference to the table's <tbody> element
  const tableBody = document.getElementById("search-result-table").getElementsByTagName("tbody")[0];

    // Loop through the rows to delete and remove each row from the table
  rowsToDelete.forEach(row => {
    tableBody.removeChild(row);
  });
}