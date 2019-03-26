<template>
  <div id="statsContainer">
    <div class="stats">
      <div class="side-panel left-panel">
        <div v-if="statistics">
          <span>Vendus:{{statistics}}</span>
          <b-button variant="link" @click="seeStats()">Console</b-button>
        </div>
        <div>
          <h2 id="graphSelectionTitle">Rapports Disponibles</h2>
          <div class="graph-list">
            <div class="graph-item selected-item" v-for="concert in concerts" :key="concert.id">
              <div class="item-title">
                <div>{{concert.name}}</div>
                <b-button variant="link" @click="getStats(concert.id)">Voir stats</b-button>
              </div>
              <div>
                <div>Période : {{concert.date | moment("YYYY-MM-DD HH:MM")}}</div>
                <div class="download-btn">Télécharger</div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="side-panel right-panel">
        <h2 id="reportTitle" class="by-events">Sommaire des ventes</h2>
        <hr>
        <div id="chartElement" class="ct-chart"></div>
        <div id="legend">
          <div>Événement A</div>
          <div>Événement B</div>
          <div>Événement C</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Chartist from "chartist";
import AxisTitle from "chartist-plugin-axistitle";
import chartist2image from "chartist-to-image";
import "../libs/chartlist/chartist.css";

const MAX_DOWNLOAD_RETRIES = 5;

export default {
  name: "stats",
  mounted: onLoad,
  data: () => {
    return {
      concerts: [],
      statistics: {}
    };
  },
  async created() {
    let customActions = {
      stats: { methods: "GET", url: "shows/{id}/stats" },
      tickets: { methods: "GET", url: "shows/{id}/tickets" }
    };
    this.resource = this.$resource("shows/{id}", {}, customActions);
    this.resource.get().then(response => {
      this.concerts = response.body;
    });
  },
  methods: {
    async getStats(id) {
      this.resource.stats({ id: id }).then(response => {
        if (response.status === 200) {
          this.statistics = response.body;
        }
      });
    },
    seeStats() {
      console.log(JSON.stringify(this.statistics));
    }
  },
  beforeRouteLeave(from, to, next) {
    document.getElementById("app").classList.remove("stats");
    next();
  }
};

function onLoad() {
  document.getElementById("app").classList.add("stats");
  fetchGraphData()
    .then(graphData => {
      createLineChart(graphData[0]);
      prepareGraphAnimation(graphData[0]);
      initListeners(graphData);
    })
    .catch(err => {
      console.error(err);
    });
}

function downloadChart(chartItem) {
  let imgOptions = {
    outputImage: {
      quality: 1,
      name: getGraphTitle(chartItem).join(" (") + ")"
    },
    download: true,
    format: "jpeg",
    log: false
  };

  let nbOfTriesLeft = 3;
  tryToRenderJpeg();

  function tryToRenderJpeg() {
    console.debug("trying to render jpeg");
    chartist2image
      .toJpeg("chartElement", imgOptions, window.chart)
      .then(base64Img => {
        window.downloadTriesLeft = MAX_DOWNLOAD_RETRIES;
        console.debug("jpeg rendering success");
      })
      .catch(async function(err) {
        if (nbOfTriesLeft-- > 0) {
          await new Promise(r => setTimeout(r, 0));
          tryToRenderJpeg();
        } else {
          if (window.downloadTriesLeft > 0) {
            window.downloadTriesLeft--;
            console.debug("download failure - retrying");
            // sometimes only simulating a new click will get the file to download
            // seems to be a bug in the library
            chartItem.querySelector("div.download-btn").click();
          } else {
            window.downloadTriesLeft = MAX_DOWNLOAD_RETRIES;
            console.error(err);
          }
        }
      });
  }
}

function fetchGraphData() {
  return new Promise(resolve => {
    // TODO fetch data from backend
    let defaultLabels = [
      "Oct",
      "Nov",
      "Dec",
      "Jan",
      "Fev",
      "Mars",
      "Avril",
      "Mai",
      "Jun",
      "Jul",
      "Aout",
      "Sept"
    ];
    resolve([
      {
        labels: defaultLabels.slice(),
        series: [
          [880, 850, 600, 750, 800, 750, 950, 800, 860, 740, 820, 960],
          [800, 820, 780, 550, 600, 650, 720, 800, 860, 690, 650, 680],
          [930, 960, 860, 850, 800, 760, 920, 900, 920, 820, 800, 760]
        ],
        type: "line"
      },
      {
        labels: defaultLabels.slice(),
        series: [
          [88, 85, 60, 75, 80, 75, 95, 80, 86, 74, 82, 96],
          [80, 82, 78, 55, 60, 65, 72, 80, 86, 69, 65, 68],
          [93, 96, 86, 85, 80, 76, 92, 90, 92, 82, 80, 76]
        ],
        type: "bar"
      },
      {
        labels: defaultLabels.slice(),
        series: [[880, 850, 600, 750, 800, 750, 950, 800, 860, 740, 820, 960]],
        type: "line"
      },
      {
        labels: defaultLabels.slice(),
        series: [[88, 85, 60, 75, 80, 75, 95, 80, 86, 74, 82, 96]],
        type: "bar"
      }
    ]);
  });
}

function getGraphTitle(chartItem) {
  let title = chartItem.querySelector("div.item-title > div:nth-child(1)")
    .textContent;
  let subTitle = chartItem.querySelector("div.item-title > div:nth-child(2)")
    .textContent;
  return [title, subTitle];
}

function updateGraphTitle(chartItem) {
  let fullTitle = getGraphTitle(chartItem);
  let title = fullTitle[0];
  let subTitle = fullTitle[1];
  let reportTitle = document.getElementById("reportTitle");
  reportTitle.textContent = title;
  if (/cumulatif/i.test(subTitle)) {
    reportTitle.classList.remove("by-events");
  } else {
    reportTitle.classList.add("by-events");
  }
}

function createBarChart(data) {
  var options = {
    seriesBarDistance: 10,
    chartPadding: {
      left: 25
    },
    axisY: {
      low: 0,
      high: 100,
      type: Chartist.FixedScaleAxis,
      ticks: [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
      onlyInteger: true,
      showLabel: true
    },
    plugins: [
      Chartist.plugins.ctAxisTitle({
        axisY: {
          axisTitle: "Taux d'assistance (%)",
          axisClass: "ct-axis-title",
          offset: {
            x: 0,
            y: 25
          },
          textAnchor: "middle",
          flipTitle: true
        }
      })
    ]
  };

  window.chart = new Chartist.Bar(".ct-chart", data, options);
}

function createLineChart(data) {
  let allValues = [].concat(...data.series);
  let minValue = Math.min(...allValues);
  minValue = minValue - (minValue % 50);
  let maxValue = Math.max(...allValues);
  maxValue = maxValue - (maxValue % 50) + 50;
  window.chart = new Chartist.Line(".ct-chart", data, {
    chartPadding: {
      left: 30,
      right: 40
    },
    axisY: {
      onlyInteger: true,
      showLabel: true,
      low: minValue,
      high: maxValue,
      type: Chartist.FixedScaleAxis,
      divisor: 10
    },
    plugins: [
      Chartist.plugins.ctAxisTitle({
        axisY: {
          axisTitle: "Revenus (k$)",
          axisClass: "ct-axis-title",
          offset: {
            x: 0,
            y: 25
          },
          textAnchor: "middle",
          flipTitle: true
        }
      })
    ],
    fullWidth: true
  });
}

/**
 * This function is used to animate the graph on the first page load.
 * Its content was copied from the official documentation with very little
 * changes, mainly affecting some variable names. We, GTI525 students, do not
 * claim to have written said function.
 * @see {@link https://gionkunz.github.io/chartist-js/examples.html|Documentation}
 */
function prepareGraphAnimation() {
  // Let's put a sequence number aside so we can use it in the event callbacks
  var seq = 0,
    delays = 80,
    durations = 500;

  // Once the chart is fully created we reset the sequence
  window.chart.on("created", function() {
    seq = 0;
  });

  // On each drawn element by Chartist we use the Chartist.Svg API to trigger SMIL animations
  window.chart.on("draw", function(data) {
    seq++;

    if (data.type === "line") {
      // If the drawn element is a line we do a simple opacity fade in. This could also be achieved using CSS3 animations.
      data.element.animate({
        opacity: {
          // The delay when we like to start the animation
          begin: seq * delays + 1000,
          // Duration of the animation
          dur: durations,
          // The value where the animation should start
          from: 0,
          // The value where it should end
          to: 1
        }
      });
    } else if (data.type === "label" && data.axis === "x") {
      data.element.animate({
        y: {
          begin: seq * delays,
          dur: durations,
          from: data.y + 100,
          to: data.y,
          // We can specify an easing function from Chartist.Svg.Easing
          easing: "easeOutQuart"
        }
      });
    } else if (data.type === "label" && data.axis === "y") {
      data.element.animate({
        x: {
          begin: seq * delays,
          dur: durations,
          from: data.x - 100,
          to: data.x,
          easing: "easeOutQuart"
        }
      });
    } else if (data.type === "point") {
      data.element.animate({
        x1: {
          begin: seq * delays,
          dur: durations,
          from: data.x - 10,
          to: data.x,
          easing: "easeOutQuart"
        },
        x2: {
          begin: seq * delays,
          dur: durations,
          from: data.x - 10,
          to: data.x,
          easing: "easeOutQuart"
        },
        opacity: {
          begin: seq * delays,
          dur: durations,
          from: 0,
          to: 1,
          easing: "easeOutQuart"
        }
      });
    } else if (data.type === "grid") {
      // Using data.axis we get x or y which we can use to construct our animation definition objects
      var pos1Animation = {
        begin: seq * delays,
        dur: durations,
        from: data[data.axis.units.pos + "1"] - 30,
        to: data[data.axis.units.pos + "1"],
        easing: "easeOutQuart"
      };

      var pos2Animation = {
        begin: seq * delays,
        dur: durations,
        from: data[data.axis.units.pos + "2"] - 100,
        to: data[data.axis.units.pos + "2"],
        easing: "easeOutQuart"
      };

      var animations = {};
      animations[data.axis.units.pos + "1"] = pos1Animation;
      animations[data.axis.units.pos + "2"] = pos2Animation;
      animations["opacity"] = {
        begin: seq * delays,
        dur: durations,
        from: 0,
        to: 1,
        easing: "easeOutQuart"
      };

      data.element.animate(animations);
    }
  });

  // For the sake of the example we update the chart every time it's created with a delay of 10 seconds (disabled)
  window.chart.on("created", function() {
    if (window.__exampleAnimateTimeout) {
      clearTimeout(window.__exampleAnimateTimeout);
      window.__exampleAnimateTimeout = null;
    }
    // window.__exampleAnimateTimeout = setTimeout(chart.update.bind(chart), 12000);
  });
}

function initListeners(graphData) {
  let allGraphItems = document.querySelectorAll(
    "div.graph-list > div.graph-item"
  );
  window.downloadTriesLeft = MAX_DOWNLOAD_RETRIES;
  for (let item of allGraphItems) {
    item.onclick = async function(event) {
      let idx = [].indexOf.call(allGraphItems, this);
      let hasGraphChanged = false;
      for (let item of allGraphItems) {
        if (item !== this) {
          if (item.classList.contains("selected-item")) {
            hasGraphChanged = true;
            item.classList.remove("selected-item");
          }
        } else {
          item.classList.add("selected-item");
        }
      }
      updateGraphTitle(this);
      let data = graphData[idx];
      switch (data.type) {
        case "line":
          createLineChart(data);
          break;
        case "bar":
          createBarChart(data);
          break;
      }
      if (event.target.classList.contains("download-btn")) {
        console.debug("downloading chart");
        if (hasGraphChanged) {
          console.debug("waiting for graph to update");
          await new Promise(r => setTimeout(r, 1000));
        }
        window.chart.supportsForeignObject = false;
        downloadChart(this);
      }
    };
  }
}
</script>

<style>
/* cannot be scoped */
.ct-axis-title {
  fill: rgba(0, 0, 0, 0.4);
  color: rgba(0, 0, 0, 0.4);
  font-size: 0.8rem;
}
</style>

<style scoped>
@import url("https://fonts.googleapis.com/css?family=Acme|Nunito+Sans");

#legend {
  margin-top: 1rem;
  color: #fafafa;
  font-family: "Nunito Sans", sans-serif;
  text-shadow: 1px 1px 1px black;
  letter-spacing: 0.8px;
}

#legend > div:after {
  content: "wa";
  margin-left: 0.5rem;
  text-shadow: none;
  border-radius: 5px;
}

#legend > div:nth-child(1):after {
  color: #d70206;
  background-color: #d70206;
}

#legend > div:nth-child(2):after {
  color: #f05b4f;
  background-color: #f05b4f;
}

#legend > div:nth-child(3):after {
  color: #f4c63d;
  background-color: #f4c63d;
}

#legend > div {
  display: inline-block;
  width: 32%;
}

#graphSelectionTitle {
  margin-top: 0.5rem;
  margin-bottom: 2.5rem;
  color: #fafafa;
  font-family: "Nunito Sans", sans-serif;
  letter-spacing: 1.5px;
  text-shadow: 2px 2px 5px black;
  font-weight: bold;
  padding-top: 1rem;
  padding-bottom: 1rem;
  background-color: rgba(0, 0, 0, 0.3);
  width: 520px;
  margin-left: calc(50% - 260px);
}

div.download-btn {
  color: #3d9970 !important;
  cursor: pointer;
}

div.download-btn:hover {
  text-decoration: underline;
}

#graphSelectionOverlay {
  position: absolute;
  left: calc(25% - 260px);
  width: 520px;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.1);
  overflow: hidden;
  top: 0;
}

div.graph-list {
  height: 80%;
}

div.graph-list > div.graph-item {
  width: 60%;
  height: 6rem;
  background-color: rgb(234, 219, 196);
  margin-bottom: 1rem;
  display: inline-block;
  border-radius: 5px;
  cursor: pointer;
  box-shadow: 4px 4px 3px 2px rgba(0, 0, 0, 0.2);
}

div.graph-item.selected-item {
  box-shadow: 0px 0px 4px 6px rgba(0, 0, 0, 0.35) !important;
}

div.graph-item > div {
  width: 100%;
  display: inline-block;
}

div.graph-item > div.item-title {
  height: 70%;
  border-bottom: 2px dashed rgba(0, 0, 0, 0.2);
  position: relative;
  padding-left: 1rem;
}

div.graph-item > div.item-title > div {
  height: 50%;
  color: #36454f;
  font-family: "Nunito Sans", sans-serif;
  text-shadow: 1px 1px px black;
  text-align: left;
  letter-spacing: 0.8px;
}

div.graph-item > div.item-title > div:nth-child(1) {
  font-size: 1.4rem;
  margin-top: 0.5rem;
}

div.graph-item > div.item-title > div:nth-child(2) {
  font-size: 0.9rem;
  margin-top: -0.3rem;
}

div.graph-item > div:not(.item-title) {
  height: 30%;
}

div.graph-item > div:not(.item-title) > div {
  display: inline-block;
  font-size: 0.8rem;
  color: #36454f;
  font-family: "Nunito Sans", sans-serif;
  letter-spacing: 0.8px;
}

div.graph-item > div:not(.item-title) > div:nth-child(1) {
  width: 70%;
  text-align: left;
  padding-left: 1rem;
}

div.graph-item > div:not(.item-title) > div:nth-child(2) {
  width: 30%;
}

div.ct-chart {
  background-color: rgb(234, 219, 196) !important;
  height: 75%;
  padding: 1.5rem 0.5rem 0 0 !important;
  border-radius: 0.2rem;
}

div.side-panel {
  display: table-cell;
  vertical-align: middle;
  width: 50%;
  background-color: rgba(0, 0, 0, 0.3);
}

div.side-panel.right-panel {
  padding-left: 2rem;
  padding-right: 1rem;
  box-sizing: border-box;
}

div.side-panel > div {
  display: block;
  width: 100%;
  padding: 0 2rem;
}

div.side-panel.left-panel > div {
  position: relative;
}

#reportTitle {
  margin-top: 1.5rem;
  margin-bottom: 0rem;
  color: #fafafa;
  font-family: "Nunito Sans", sans-serif;
  text-shadow: 2px 2px 5px black;
  text-align: left;
  letter-spacing: 0.8px;
  font-weight: bold;
}

#reportTitle:after {
  font-size: 1.1rem;
}

#reportTitle.by-events:after {
  content: " \2015 Par événement";
}

#reportTitle:not(.by-events):after {
  content: " \2015 Cumulatif";
}

#reportTitle + hr {
  margin: 0.2rem 0.2rem 1rem 0.1rem;
  border: 1px solid #fafafa;
  border-radius: 0.1rem;
  box-shadow: 1px 1px 1px 1px beige;
}

div.stats {
  display: table;
  position: relative;
  height: 100%;
  width: 100%;
}

#statsContainer {
  width: 100%;
  height: calc(100% - 85px);
}
</style>
