<template>
  <div id="statsContainer">
    <button id="downloadChartBtn"
          class="btn btn-primary button"
          @click="downloadChart"
    >Télécharger</button>
    <div class="stats">
      <div class="side-panel left-panel">
        <div>
          <h2 id="graphSelectionTitle">Mes Spectacles</h2>
          <div class="graph-list">
            <div class="graph-item selected-item" v-for="concert in concerts" :key="concert.id">
              <div class="item-title">
                <div>{{concert.name}}</div>
              </div>
              <div>
                <div>Période : {{getConcertDate(concert)}}</div>
                <div v-bind:id="'graphVisibilityBtn' + concert.id" 
                  @click="toggleGraphElemVisibility(concert.id)" 
                  class="graph-visibility-trigger">Ajouter</div>
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
          <div>Scannés</div>
          <div>Vendus</div>
          <div>Total</div>
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
import Swal from 'sweetalert2';

const MAX_DOWNLOAD_RETRIES = 5;

export default {
  name: "stats",
  data: () => {
    return {
      concerts: [],
      statistics: {}
    };
  },
  async created() {
    this.statistics = {};
    let customActions = {
      stats: { methods: "GET", url: "shows/{id}/stats" },
      tickets: { methods: "GET", url: "shows/{id}/tickets" }
    };
    this.resource = this.$resource("shows/{id}", {}, customActions);
    this.resource.get().then(response => {
      console.debug('resources', response.body);
      this.concerts = response.body;
      onLoad(this);
    });
  },
  methods: {
    getConcertDate(concert) {
      return this.$moment(concert.date || new Date()).format("YYYY-MM-DD HH:mm");
    },
    async getStats(id) {
      return this.resource.stats({ id: id }).then(response => {
        if (response.status === 200) {
          this.statistics[id] = response.body;
        }
      });
    },
    downloadChart() {
      let filename = 'RapportDeVentes_' + new Date().toString().split(/\sGMT/)[0];
      let imgOptions = {
        outputImage: {
          quality: 1,
          name: filename
        },
        download: true,
        format: "jpeg",
        log: true
      };
      genImage();
      async function genImage(){
        await chartist2image.toJpeg("chartElement", imgOptions, window.chart).then(
          res => {
            // failover if download fails - might not work in localhost
            fetch(res.content)
              .then(r => r.blob())
              .then(blob => {
                var reader = new FileReader();
                reader.onload = function() {
                  Swal.mixin({
                    toast: true,
                    position: 'top-end',
                    timer: 5000,
                    showConfirmButton: false
                  }).fire({
                    type: 'info',
                    html: `&nbsp;Problème de téléchargement?&nbsp;<a download="${filename}.jpg" href="${this.result}">Cliquez ici</a>`
                  });
                };
                reader.readAsDataURL(blob) ;
              });
        });
      }
    },
    toggleGraphElemVisibility(concertId) {
      console.debug('toggling visibility', concertId);
      let concertToTrigger = this.concerts.find(c => c.id == concertId);
      let nbOfVisibleConcerts = this.concerts.filter(c => c.isVisible).length;
      if(!concertToTrigger.isVisible && nbOfVisibleConcerts >= 4
        || concertToTrigger.isVisible && nbOfVisibleConcerts <= 1 && false) { // unactivated minimum
        Swal.mixin({
          toast: true,
          position: 'top-end',
          timer: 5000,
          showConfirmButton: false
        }).fire({
          type: 'warning',
          title: concertToTrigger.isVisible 
            ?'Minimum 1 concert par graphique'
            :'Maximum 4 concerts par graphique'
        });
      } else {
        concertToTrigger.isVisible = !concertToTrigger.isVisible;
        fetchGraphData(this).then(graphData => createBarChart(graphData[0]));
      }
    }
  },
  beforeRouteLeave(from, to, next) {
    document.getElementById("app").classList.remove("stats");
    next();
  }
};

function onLoad(vue) {
  document.getElementById("app").classList.add("stats");
  vue.concerts
    .sort((c1,c2) => new Date(c2.date).getTime() - new Date(c1.date).getTime())
    .forEach((c, idx) => c.isVisible = idx < 4);
  fetchGraphData(vue)
    .then(graphData => {
      createBarChart(graphData[0]);
      // createLineChart(graphData[0]); // deprecated
      // prepareGraphAnimation(graphData[0]); // deprecated
      initListeners(graphData);
    })
    .catch(err => {
      console.error(err);
    });
}

function fetchGraphData(vue) {
  return new Promise(resolve => {
    console.debug('concerts', vue.concerts);
    let visibleConcerts = vue.concerts
      .sort((c1,c2) => new Date(c2.date).getTime() - new Date(c1.date).getTime())
      .filter(c => c.isVisible);
    Promise.all(visibleConcerts.map(c => {
      return new Promise(res => {
        vue.getStats(c.id).then(res);
      });
    })).then(() => {
      vue.concerts.forEach(c => {
        let visibilityTriggerBtn = document
          .getElementById('graphVisibilityBtn' + c.id);
        visibilityTriggerBtn.textContent = c.isVisible
          ?'Retirer'
          :'Ajouter';
        visibilityTriggerBtn.classList[c.isVisible ?'add' :'remove']('visible-in-graph');
      });
      console.debug('statistics', vue.statistics);
      ///////// HARDCOCED DATA FOR PRETTY RESULTS (REMOVE FOR DEMO) /////////
      // visibleConcerts.forEach(c => {
      //   vue.statistics[c.id].sold = parseInt(vue.statistics[c.id].total*Math.random());
      //   vue.statistics[c.id].scanned = parseInt(vue.statistics[c.id].sold*Math.random());
      // });
      ///////////////////////////////////////////////////////////////////////
      resolve([
        {
          labels: visibleConcerts.map(c => c.name.length > 20 
            ?(c.name.substring(0,18) + '...') 
            :c.name),
          series: [
            visibleConcerts.map(c => vue.statistics[c.id].scanned),
            visibleConcerts.map(c => vue.statistics[c.id].sold),
            visibleConcerts.map(c => vue.statistics[c.id].total)
          ]
        }
      ]);
    });
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

function SuppressForeignObjectPlugin(chart) {
  window.chart.supportsForeignObject = false;
}

function createBarChart(data) {
  let options = {
    seriesBarDistance: 20,
    chartPadding: {
      left: 35
    },
    axisY: {
      onlyInteger: true,
      showLabel: true,
    },
    plugins: [
      Chartist.plugins.ctAxisTitle({
        axisY: {
          axisTitle: "Nombre de Billets",
          axisClass: "ct-axis-title",
          offset: {
            x: 0,
            y: 25
          },
          textAnchor: "middle",
          flipTitle: true
        }
      }),
      SuppressForeignObjectPlugin
    ]
  };

  window.chart = new Chartist.Bar(".ct-chart", data, options).on('draw', drawnData => {
    if(drawnData.type === 'bar') {
      drawnData.element.attr({
        style: 'stroke-width: 20px'
      });
    }
    // forcing x-axis titles to be centered
    if(drawnData.type === 'label' && drawnData.axis.units.pos === 'x') {
      drawnData.element.attr({
        x: drawnData.x + drawnData.width / 2, 'text-anchor': 'middle'
      });
    }
    // drawing individual bar value labels
    if (drawnData.type === "bar") {
      let value = parseInt(drawnData.element.attr('ct:value'));
      if (value) {
        let label = new Chartist.Svg('text');
        label.addClass('ct-custom-bar-label');
        label.text(value.toString());
        let x, y;
        label.attr({
          x: x = (drawnData.x1 + drawnData.element.width() / 2),
          y: y = (drawnData.y1 + drawnData.element.height() * -1 - 10),
          'text-anchor': 'middle',
          fill: 'rgba(0,0,0,0.4)',
          transform: `rotate(-45 ${x},${y})`
        });
        drawnData.group.append(label);
      }
    }
  });
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
  // for (let item of allGraphItems) {
  //   item.onclick = async function(event) {
  //     let idx = [].indexOf.call(allGraphItems, this);
  //     let hasGraphChanged = false;
  //     for (let item of allGraphItems) {
  //       if (item !== this) {
  //         if (item.classList.contains("selected-item")) {
  //           hasGraphChanged = true;
  //           item.classList.remove("selected-item");
  //         }
  //       } else {
  //         item.classList.add("selected-item");
  //       }
  //     }
  //     updateGraphTitle(this);
  //     let data = graphData[idx];
  //     switch (data.type) {
  //       case "line":
  //         createLineChart(data);
  //         break;
  //       case "bar":
  //         createBarChart(data);
  //         break;
  //     }
  //     if (event.target.classList.contains("download-btn")) {
  //       console.debug("downloading chart");
  //       if (hasGraphChanged) {
  //         console.debug("waiting for graph to update");
  //         await new Promise(r => setTimeout(r, 1000));
  //       }
  //       window.chart.supportsForeignObject = false;
  //       downloadChart(this);
  //     }
  //   };
  // }
}
</script>

<style>
/* cannot be scoped */
.ct-axis-title {
  fill: rgba(0, 0, 0, 0.4);
  color: rgba(0, 0, 0, 0.4);
  font-size: 0.8rem;
}
.ct-chart-bar .ct-label.ct-horizontal.ct-end {
  text-anchor: middle !important;
}
.ct-custom-bar-label {
  font-size: 11px;
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

div.graph-visibility-trigger {
  color: #3d9970 !important;
  cursor: pointer;
}

div.graph-visibility-trigger.visible-in-graph {
  color: lightcoral !important;
}

div.graph-visibility-trigger:hover {
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
  padding-bottom: 4rem;
}

div.graph-list > div.graph-item {
  width: 60%;
  height: 4.8rem;
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
  height: 60%;
  border-bottom: 2px dashed rgba(0, 0, 0, 0.2);
  position: relative;
  padding-left: 1rem;
  padding-right: 1rem;
  white-space: nowrap;
}

div.graph-item > div.item-title > div {
  color: #36454f;
  font-family: "Nunito Sans", sans-serif;
  text-shadow: 1px 1px px black;
  text-align: left;
  letter-spacing: 0.8px;
  text-overflow: ellipsis;
}

div.graph-item > div.item-title > div:nth-child(1) {
  font-size: 1.4rem;
  margin-top: 0.5rem;
  overflow-x: hidden;
  height: 75%;
}

div.graph-item > div.item-title > div:nth-child(2) {
  font-size: 0.9rem;
  margin-top: -0.3rem;
}

div.graph-item > div:not(.item-title) {
  height: 40%;
  padding-top: 0.1rem;
}

.button {
  font-family: "Sniglet", cursive;
  padding-left: 2rem;
  padding-right: 2rem;
  background-color: rgba(240, 240, 240, 1);
  border-color: rgba(0, 0, 0, 0.8);
  border-width: 2px;
  font-size: 1.5rem;
  color: rgba(0, 0, 0, 0.8);
  z-index: 3;
  position: relative;
}

.button:hover {
  background-color: rgba(240, 240, 240, 1);
  border-color: #42b983;
  color: #42b983;
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
  height: 50vh !important;
  min-height: 19rem !important;
  max-height: 50vh !important;
  padding: 1.5rem 0.5rem 0 0 !important;
  border-radius: 0.2rem;
}

div.side-panel {
  display: table-cell;
  vertical-align: top;
  width: 50%;
  background-color: rgba(0, 0, 0, 0.3);
  padding-bottom: 5rem;
  padding-top: 2rem;
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
  position: relative;
  height: calc(100% - 85px);
}

#downloadChartBtn {
  position: fixed;
  left: 3rem;
  bottom: 4.5rem;
  font-size: 1.2rem;
}

</style>
