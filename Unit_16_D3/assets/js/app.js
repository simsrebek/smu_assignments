// @TODO: YOUR CODE HERE!
var svgWidth = 960;
var svgHeight = 500;

var margin = {
    top: 20,
    right: 40,
    bottom: 60,
    left: 100
};

var width = svgWidth - margin.left - margin.right;
var height = svgHeight - margin.top - margin.bottom;

// Create an SVG wrapper, append an SVG group that will hold our chart, and shift the latter by left and top margins.
var svg = d3.select("#scatter")
    .append("svg")
    .attr("width", svgWidth)
    .attr("height", svgHeight);

var chartGroup = svg.append("g")
    .attr("transform", `translate(${margin.left}, ${margin.top})`);

// Import Data
d3.csv("assets/data/data.csv").then(function(povData) {

    // Step 1: Parse Data/Cast as numbers
    // ==============================
    povData.forEach(function(data) {
        data.poverty = parseFloat(data.poverty);
        data.healthcare = parseFloat(data.healthcare);
    });

    // Step 2: Create scale functions
    // ==============================
    var xLinearScale = d3.scaleLinear()
        .domain([0, d3.max(povData, d => d.poverty)])
        .range([0, width]);

    var yLinearScale = d3.scaleLinear()
        .domain([0, d3.max(povData, d => d.healthcare) + 5])
        .range([height, 0]);

    // Step 3: Create axis functions
    // ==============================
    var bottomAxis = d3.axisBottom(xLinearScale);
    var leftAxis = d3.axisLeft(yLinearScale);

    // Step 4: Append Axes to the chart
    // ==============================
    chartGroup.append("g")
        .attr("transform", `translate(0, ${height})`)
        .call(bottomAxis);

    chartGroup.append("g")
        .call(leftAxis);

    // Step 5: Create Circles
    // ==============================
    // var nodes = svg.append("g")
    //     .attr("class", "nodes")
    //     .selectAll("circle")
    //     .data(povData)
    //     .enter()
    //     // Add one g element for each data node here.
    //     .append("g")
    //     // Position the g element like the circle element used to be.
    //     .attr("transform", function(d, i) {
    //         return "translate(" + xLinearScale(d.poverty) + "," +
    //             yLinearScale(d.healthcare) + ")";
    //     });

    // nodes.append("circle")
    //     .attr("r", "15")
    //     .attr("fill", "pink")
    //     .attr("opacity", ".5");

    // nodes.append("text")
    //     .attr("text-anchor", "middle")
    //     .text(function(d) {
    //         return d.abbr;
    //     })
    //     .attr('color', 'black')
    //     .attr('font-size', 15);


    var circlesGroup = chartGroup.selectAll("circle")
        .data(povData)
        .enter()
        .append("circle")
        .attr("cx", d => xLinearScale(d.poverty))
        .attr("cy", d => yLinearScale(d.healthcare))
        .attr("r", "15")
        .attr("fill", "pink")
        .attr("opacity", ".5");

    //Step 5.5 f*ck around with some text in circles
    let texts = svg.selectAll(null)
        .data(povData)
        .enter()
        .append('text')
        .text(d => d.abbr)
        .attr('color', 'black')
        .attr('font-size', 15) //BELOW IS A HACK
        .attr("x", d => xLinearScale(d.poverty) + 90)
        .attr("y", d => yLinearScale(d.healthcare) + 25);


    // Step 6: Initialize tool tip
    // ==============================
    var toolTip = d3.tip()
        .attr("class", "tooltip")
        .offset([80, -60])
        .html(function(d) {
            return (`${d.state}<br>Poverty: ${d.poverty}%<br>Healthcare: ${d.healthcare}%`);
        });

    // Step 7: Create tooltip in the chart
    // ==============================
    chartGroup.call(toolTip);

    // Step 8: Create event listeners to display and hide the tooltip
    // ==============================
    circlesGroup.on("click", function(data) {
            toolTip.show(data, this);
        })
        // onmouseout event
        .on("mouseout", function(data, index) {
            toolTip.hide(data);
        });
    texts.on("click", function(data) {
            toolTip.show(data, this);
        })
        // onmouseout event
        .on("mouseout", function(data, index) {
            toolTip.hide(data);
        });

    // Create axes labels
    chartGroup.append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 0 - margin.left + 40)
        .attr("x", 0 - (height / 2))
        .attr("dy", "1em")
        .attr("class", "axisText")
        .text("Healthcare %");

    chartGroup.append("text")
        .attr("transform", `translate(${width / 2}, ${height + margin.top + 30})`)
        .attr("class", "axisText")
        .text("Poverty %");
}).catch(function(error) {
    console.log(error);
});