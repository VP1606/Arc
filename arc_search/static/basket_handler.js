function do_basket_search() {
    var key = document.getElementById("search-field-typebox").value;

    var loaderUI = document.getElementById("loader-wheel");
    var searchButton = document.getElementById("search-button-clicker");
    var basketContainer = document.getElementById("basketContainer");
    var noneFound = document.getElementById("noneFoundContainer");

    loaderUI.style.display = "block";
    searchButton.style.display = "none";
    basketContainer.style.display = "none";
    basketContainer.innerHTML = '';
    noneFound.style.display = "none";

    var url = `/operate_basket?id=iahfiasfdosai2313212**7613&key=${encodeURIComponent(key)}`;

    fetch(url, {
        method: "GET"
      })
      .then((response) => response.json())
      .then((json) => {

        loaderUI.style.display = "none";
        searchButton.style.display = "block";

        if (json == false) {
            noneFound.style.display = "flex";
            return;
        };

        try {
          json.forEach(item => {
            basket_createItemCard(item);
          });
        }

        catch {
          noneFound.style.display = "flex";
          return;
        };

        basketContainer.style.display = "block";
      });
};

function basket_createItemCard(item) {
  fetch('/static/basket_mode/basket_element.html')
      .then(response => response.text())
      .then(data => {
        data = data.replace("[NAME]", item.name);
        data = data.replace("[EAN]", item.ean);
        data = data.replace("[QTY]", item.quantity);
        data = data.replace("[BEST_SUP]", item.best_supplier);

        data = data.replace("[BW-INSTOCK]", item.bw_instock);
        data = data.replace("[BW-PCKZ]", item.bw_pack_size);
        data = data.replace("[BW-UNP]", item.bw_unit_price);
        data = data.replace("[BW-TLP]", item.bw_total);

        data = data.replace("[BK-INSTOCK]", item.bk_instock);
        data = data.replace("[BK-PCKZ]", item.bk_pack_size);
        data = data.replace("[BK-UNP]", item.bk_unit_price);
        data = data.replace("[BK-TLP]", item.bk_total);

        data = data.replace("[PF-INSTOCK]", item.pf_instock);
        data = data.replace("[PF-PCKZ]", item.pf_pack_size);
        data = data.replace("[PF-UNP]", item.pf_unit_price);
        data = data.replace("[PF-TLP]", item.pf_total);

        var basketContainer = document.getElementById('basketContainer');
        var newdiv = document.createElement('div');
        newdiv.innerHTML = data;
        newdiv.style.paddingBottom = '20px';

        basketContainer.appendChild(newdiv);
      })
      .catch(error => {
        console.error('Error fetching component:', error);
      });
};