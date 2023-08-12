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

function createSpecRow() {
    fetch('/static/spec_search/spec_row.html')
      .then(response => response.text())
      .then(data => {

        var table = document.getElementById('spec-search-result-table');
        var newRow = table.insertRow(-1);
        newRow.classList.add("spec-search-return-row");
        newRow.innerHTML = data;
        
      })
      .catch(error => {
        console.error('Error fetching component:', error);
      });
};

function do_ean_search() {
  var searchEAN = document.getElementById("search-field-typebox").value;

  var loaderUI = document.getElementById("loader-wheel");
  var searchButton = document.getElementById("search-button-clicker");

  loaderUI.style.display = "block";
  searchButton.style.display = "none";

  var url = `/search_ean?id=iahfiasfdosai2313212**7613&query=${encodeURIComponent(searchEAN)}`;

  fetch(url, {
    method: "GET"
  })
  .then((response) => response.json())
  .then((json) => {
    console.log(json);
    loaderUI.style.display = "none";
    searchButton.style.display = "block";
  });
};

function do_name_search() {
  var searchName = document.getElementById("search-field-typebox").value;

  var loaderUI = document.getElementById("loader-wheel");
  var searchButton = document.getElementById("search-button-clicker");

  loaderUI.style.display = "block";
  searchButton.style.display = "none";

  var url = `/search_name?id=iahfiasfdosai2313212**7613&query=${encodeURIComponent(searchName)}`;

  fetch(url, {
    method: "GET"
  })
  .then((response) => response.json())
  .then((json) => {
    console.log(json);
    loaderUI.style.display = "none";
    searchButton.style.display = "block";
  });
};