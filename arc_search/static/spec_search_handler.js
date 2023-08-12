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

function createSpecRow(name, ean) {
    fetch('/static/spec_search/spec_row.html')
      .then(response => response.text())
      .then(data => {

        data = data.replace("[NAME]", name);
        data = data.replace("[EAN]", ean);

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
    createSpecRow(row[2], row[0]);
  };
}