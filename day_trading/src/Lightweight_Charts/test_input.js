//import './mycustomplugin/mycustomplugin.mjs';
import { Mycustomplugin } from './mycustomplugin/mycustomplugin.mjs';
//import { Mycustomplugin } from '../mycustomplugin';
//import { MycustompluginData } from '../data';

//import { generateSampleData } from '../sample-data';
//import dataJson from '/Users/stevensmith/Projects/Random_Projects/day_trading/src/Lightweight_Charts/order_history.json';
//import { BackgroundShadeSeries } from '../plugins/background-shade-series/background-shade-series';

import { createChart, LineSeries } from "./mycustomplugin/node_modules/lightweight-charts/dist/lightweight-charts.standalone.production.mjs";

//const chart = createChart(document.body, { width: 400, height: 300 });
const chart = LightweightCharts.createChart(
            document.getElementById('container')
        );


const series = chart.addCustomSeries(new Mycustomplugin(), {
	/* Options */
});

//const data: MycustompluginData[] = dataJson as MycustompluginData[];

series.setData( [
   { time: 1748967720, value: 10 },
{ time: 1748967900, value: 7},
{ time: 1748967960, value: 9 }
]);



// new

function generateBuyData(jsonFilePath) {
    return fetch(jsonFilePath)
        .then(response => response.json())
        .then(jsonData => jsonData.map(entry => ({
            time: entry.time,
            value: entry.value,
        })))
        .catch(error => {
            console.error('Error fetching JSON data:', error);
            return [];
        });
};
// Fetch data from a JSON file and use it to populate the chart
//const buyData = generateBuyData();
const jsonFilePath = prompt('Please enter the path to the JSON file:', 'stock_order_2025-06-03_MCTR_1m.json');
fetch(jsonFilePath)
    .then(response => response.json())
    .then(data => {
        // Create the Lightweight Chart within the container element
        // const chart = LightweightCharts.createChart(
        //     document.getElementById('container')
        // );

        // Create the Main Series (Candlesticks)
        const mainSeries = chart.addSeries(LightweightCharts.CandlestickSeries);

        // TODO: this will be passed by an internal function
        const jsonFilePath = 'order_history.json' //prompt('Please enter the path to the JSON file:', 'order_history.json');
        let buyData = [];
        generateBuyData(jsonFilePath).then(data => buyData = data);
        // Set the data for the Main Series
        mainSeries.setData(data);

        // // Generate sample data to use within a candlestick series
        //const candleStickData = generateCandlestickData();
        const lineData = buyData.map(datapoint => ({
            time: datapoint.time,
            value: datapoint.value,
        }));


        // Add an area series to the chart,
        // Adding this before we add the candlestick chart
        // so that it will appear beneath the candlesticks
        // const areaSeries = chart.addSeries(LightweightCharts.LineSeries, {
        //     lastValueVisible: false, // hide the last value marker for this series
        //     crosshairMarkerVisible: false, // hide the crosshair marker for this series
        //     lineColor: 'transparent', // hide the line
        //     topColor: 'rgba(56, 33, 110,0.6)',
        //     bottomColor: 'rgba(56, 33, 110, 0.1)',
        // });

        const areaSeries = chart.addSeries(LightweightCharts.LineSeries)
        // Set the data for the Area Series
        areaSeries.setData(lineData);


    })
    .catch(error => console.error('Error fetching JSON data:', error));

