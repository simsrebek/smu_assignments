// from data.js
var tableData = data;

// console.log(data)
var tbody = d3.select("tbody");
// console.log(tbody)
// // Console.log the weather data from data.js
// // console.log(tableData);

tableData.forEach((sheepleReport) => {
  var row = tbody.append("tr");
  Object.values(sheepleReport).forEach((value) => {
    var cell = row.append("td");
    cell.text(value);
  });
});

// // Select the button
var button = d3.select("#filter-btn");

button.on("click", function () {

  // Select the input element and get the raw HTML node
  var inputElement = d3.select("#datetime");

  // Get the value property of the input element
  var inputValue = inputElement.property("value");

  let inputCity = d3.select("#city").property("value");

  // alert(inputValue);  

  d3.select("tbody").selectAll("tr").remove();


  // this is to include logic to avoid null values
  let filterData = tableData;
  if (inputValue !== "") {
    filterData = tableData.filter(ufoRow => ufoRow.datetime === inputValue);
  };
  if (inputCity !== "") {
    filterData = filterData.filter(ufoRow => ufoRow.city === inputCity);
  }
  // console.log(filterData)

  filterData.forEach((sheepleReport) => {
    var row = tbody.append("tr");
    Object.values(sheepleReport).forEach(value => {
      var cell = row.append("td");
      cell.text(value);

      // alert(inputValue);     
    });
  });

});
