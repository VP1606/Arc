function createSpecTable() {
    fetch('/static/spec_search/spec_search_table.html')
      .then(response => response.text())
      .then(data => {
        const component = document.createElement("div");
        component.classList.add("spec-table-component");
        component.innerHTML = data;

        document.getElementById('specContainer').appendChild(component);
      })
      .catch(error => {
        console.error('Error fetching component:', error);
      });
};

function createSpecRow(name, ean, sources) {
    fetch('/static/spec_search/spec_row.html')
      .then(response => response.text())
      .then(data => {

        data = data.replace("[NAME]", name);
        data = data.replace("[EAN]", ean);

        const bway_logo = '<img src="/static/supplier_logos/bestway-logo.png" class="supplier_icon" style="width: 45px; height: 45px; visibility: hidden;">';
        const booker_logo = ' <img src="/static/supplier_logos/booker-logo.png" class="supplier_icon" style="width: 45px; height: 45px; visibility: hidden;">';
        const parfetts_logo = '<img src="/static/supplier_logos/parfetts-logo.png" class="supplier_icon" style="width: 45px; height: 45px; visibility: hidden;">';

        if ('bestway' in sources && sources.bestway == true) {
          data = data.replace(bway_logo, bway_logo.replace("hidden", "visible"));
        };

        if ('booker' in sources && sources.booker == true) {
          data = data.replace(booker_logo, booker_logo.replace("hidden", "visible"));
        };

        if ('parfetts' in sources && sources.parfetts == true) {
          data = data.replace(parfetts_logo, parfetts_logo.replace("hidden", "visible"));
        }

        var table = document.getElementById('spec-search-result-table');
        var newRow = table.insertRow(-1);
        newRow.classList.add("spec-search-return-row");
        newRow.innerHTML = data;
        
      })
      .catch(error => {
        console.error('Error fetching component:', error);
      });
};

function resetSpecTable() {
  // const container = document.getElementById('componentContainer');
  // container.style.display = "none";

  const className = "spec-search-return-row";
  const rowsToDelete = document.querySelectorAll(`.${className}`);

    // Get the reference to the table's <tbody> element
  const tableBody = document.getElementById("spec-search-result-table").getElementsByTagName("tbody")[0];

    // Loop through the rows to delete and remove each row from the table
  rowsToDelete.forEach(row => {
    tableBody.removeChild(row);
  });
}

function do_ean_search() {
  var searchEAN = document.getElementById("search-field-typebox").value;

  var loaderUI = document.getElementById("loader-wheel");
  var searchButton = document.getElementById("search-button-clicker");
  var specContainer = document.getElementById("specContainer")

  loaderUI.style.display = "block";
  searchButton.style.display = "none";
  specContainer.style.display = "none";

  resetSpecTable();

  var url = `/search_ean?id=iahfiasfdosai2313212**7613&query=${encodeURIComponent(searchEAN)}`;

  fetch(url, {
    method: "GET"
  })
  .then((response) => response.json())
  .then((json) => {
    SearchConstructor(json);

    specContainer.style.display = "block";
    loaderUI.style.display = "none";
    searchButton.style.display = "block";
  });
};

function do_name_search() {
  var searchName = document.getElementById("search-field-typebox").value;

  var loaderUI = document.getElementById("loader-wheel");
  var searchButton = document.getElementById("search-button-clicker");
  var specContainer = document.getElementById("specContainer");

  loaderUI.style.display = "block";
  searchButton.style.display = "none";
  specContainer.style.display = "none";

  resetSpecTable();

  var url = `/search_name?id=iahfiasfdosai2313212**7613&query=${encodeURIComponent(searchName)}`;

  fetch(url, {
    method: "GET"
  })
  .then((response) => response.json())
  .then((json) => {
    SearchConstructor(json);

    specContainer.style.display = "block";
    loaderUI.style.display = "none";
    searchButton.style.display = "block";
  });
};

function SearchConstructor(results) {
  for (var row of results) {
    createSpecRow(row[2], row[0], row[6]);
  };
}