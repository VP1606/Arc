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

function createSpecRow(name, ean, sources, row_id) {
    fetch('/static/spec_search/spec_row.html')
      .then(response => response.text())
      .then(data => {

        var new_row_flag = `row-ean-field-${row_id}`;
        var regex = /\[ROW-EAN-ID\]/g;

        data = data.replace("[NAME]", name);
        data = data.replace("[EAN]", ean);
        data = data.replace(regex, new_row_flag);

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
  var specContainer = document.getElementById("specContainer");
  var noneFound = document.getElementById("noneFoundContainer");
  var componentContainer = document.getElementById("componentContainer")

  loaderUI.style.display = "block";
  searchButton.style.display = "none";
  specContainer.style.display = "none";
  noneFound.style.display = "none";
  componentContainer.style.visibility = "hidden";

  resetSpecTable();

  var url = `/search_ean?id=iahfiasfdosai2313212**7613&query=${encodeURIComponent(searchEAN)}`;

  fetch(url, {
    method: "GET"
  })
  .then((response) => response.json())
  .then((json) => {
    SearchConstructor(json);

    loaderUI.style.display = "none";
    searchButton.style.display = "block";

    if (json.length > 0) {
      specContainer.style.display = "block";
    } else {
      noneFound.style.display = "flex";
    };

  });
};

function do_name_search() {
  var searchName = document.getElementById("search-field-typebox").value;

  var loaderUI = document.getElementById("loader-wheel");
  var searchButton = document.getElementById("search-button-clicker");
  var specContainer = document.getElementById("specContainer");
  var noneFound = document.getElementById("noneFoundContainer");
  var componentContainer = document.getElementById("componentContainer")

  loaderUI.style.display = "block";
  searchButton.style.display = "none";
  specContainer.style.display = "none";
  noneFound.style.display = "none";
  componentContainer.style.visibility = "hidden";

  resetSpecTable();

  var url = `/search_name?id=iahfiasfdosai2313212**7613&query=${encodeURIComponent(searchName)}`;

  fetch(url, {
    method: "GET"
  })
  .then((response) => response.json())
  .then((json) => {
    SearchConstructor(json);

    loaderUI.style.display = "none";
    searchButton.style.display = "block";

    if (json.length > 0) {
      specContainer.style.display = "block";
    } else {
      noneFound.style.display = "flex";
    };

  });
};

function SearchConstructor(results) {
  var counter = 0;
  for (var row of results) {
    createSpecRow(row[2], row[0], row[6], counter);
    counter += 1;
  };
}

function specSelectHit(row_id) {
  const ean = document.getElementById(row_id).textContent;

  var exact_ean_button = document.getElementById("exact-ean-btn");
  var ean_input = document.getElementById("search-field-typebox");
  var search_button = document.getElementById("search-button-clicker");

  exact_ean_button.click();
  ean_input.value = ean;
  search_button.click();
}