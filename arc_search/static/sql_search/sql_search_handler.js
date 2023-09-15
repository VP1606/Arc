function sql_search(mode) {
    console.log(`SQL SEARCH. mode: ${mode}`);
    var searchParameter = document.getElementById("search-field-typebox").value;

    var loaderUI = document.getElementById("loader-wheel");
    var searchButton = document.getElementById("search_button");
    var specContainer = document.getElementById("sql-search-container");

    loaderUI.style.display = "block";
    searchButton.style.display = "none";
    // specContainer.style.display = "none";
    specContainer.innerHTML = '';

    var url = `/search_name?id=iahfiasfdosai2313212**7613&query=${encodeURIComponent(searchParameter)}`;
    if (mode == "ean") {
        var url = `/search_ean?id=iahfiasfdosai2313212**7613&query=${encodeURIComponent(searchParameter)}`;
        console.log("EAN MODE.")
    };

    fetch(url, {
        method: "GET"
      })
      .then((response) => response.json())
      .then((json) => {
        // SearchConstructor(json);
    
        loaderUI.style.display = "none";
        searchButton.style.display = "block";
    
        // if (json.length > 0) {
        //   specContainer.style.display = "block";
        // } else {
        //   noneFound.style.display = "flex";
        // };

        console.log(json);
        
        fetch('/static/sql_search/sql_search_page.html')
        .then(response => response.text())
        .then(data => {
            specContainer.innerHTML = data;
            for (const index in json) {
                const block = json[index];
                console.log(block);
                MakeSQLRow(block[2], block[0]);
            };
        });
        
      });

};

function MakeSQLRow(name, ean) {
    fetch('/static/sql_search/sql_search_row.html')
            .then(response => response.text())
            .then(data => {
                data = data.replace("[NAME]", name);
                data = data.replace("[EAN]", ean);

                var main_box = document.getElementById('sql-search-box');
                main_box.innerHTML = main_box.innerHTML + ' ' + data;
            });
};