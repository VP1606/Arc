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