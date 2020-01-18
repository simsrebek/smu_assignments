function buildMetadata(inpSample) {
  d3.json(`/metadata/${inpSample}`).then((data) => {
    // Use d3 to select the panel with id of `#inpSample-metadata`
    var panel = d3.select("#sample-metadata");

    // Use `.html("") to clear any existing metadata
    panel.html("");

    // Use `Object.entries` to add each key and value pair to the panel
    // Hint: Inside the loop, you will need to use d3 to append new
    // tags for each key-value in the metadata.
    Object.entries(data).forEach(([key, value]) => {
      panel.append("h4").text(`${key}: ${value}`);
    });

    // BONUS: Build the Gauge Chart
    buildGauge(data.WFREQ);
  });
}

function buildCharts(inpSample) {
  d3.json(`/samples/${inpSample}`).then((data) => {
    const otu_ids = data.otu_ids;
    const otu_labels = data.otu_labels;
    const inpSample_values = data.sample_values;

    // Build a Bubble Chart
    var bubbleLayout = {
      margin: { t: 0 },
      hovermode: "closest",
      xaxis: { title: "IDs from Sample" }
    };
    var bubbleData = [
      {
        x: otu_ids,
        y: inpSample_values,
        text: otu_labels,
        mode: "markers",
        marker: {
          size: inpSample_values,
          color: otu_ids,
          colorscale: "Electric"
        }
      }
    ];

    Plotly.plot("bubble", bubbleData, bubbleLayout);

    // Build a Pie Chart
    // HINT: You will need to use slice() to grab the top 10 inpSample_values,
    // otu_ids, and labels (10 each).
    var pieData = [
      {
        values: inpSample_values.slice(0, 10),
        labels: otu_ids.slice(0, 10),
        hovertext: otu_labels.slice(0, 10),
        hoverinfo: "hovertext",
        type: "pie"
      }
    ];

    var pieLayout = {
      margin: { t: 0, l: 0 }
    };

    Plotly.plot("pie", pieData, pieLayout);
  });
}

function init() {
  // Grab a reference to the dropdown select element
  var selector = d3.select("#selDataset");

  // Use the list of inpSample names to populate the select options
  d3.json("/names").then((inpSampleNames) => {
    inpSampleNames.forEach((inpSample) => {
      selector
        .append("option")
        .text(inpSample)
        .property("value", inpSample);
    });

    // Use the first inpSample from the list to build the initial plots
    const firstSample = inpSampleNames[0];
    buildCharts(firstSample);
    buildMetadata(firstSample);
  });
}

function optionChanged(newSample) {
  // Fetch new data each time a new inpSample is selected
  buildCharts(newSample);
  buildMetadata(newSample);
}

// Initialize the dashboard
init();
