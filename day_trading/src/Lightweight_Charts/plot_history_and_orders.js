import { Mycustomplugin } from './mycustomplugin/mycustomplugin.mjs';
//import { createTimeScale } from 'lightweight-charts';


// Fetch data from a JSON file and use it to populate the chart
const stockHistoryFile = prompt('Please enter the path to the Stocks price history JSON file:', 'stock_order_2025-06-03_MCTR_1m.json');
const orderHistoryFile = prompt('Please enter the path to the Stocks Order buy/sell history JSON file:', 'order_history.json');


//const orderHistoryOptions = { pointRadius: 10}; // { layout: { textColor: 'black', background: { type: 'solid', color: 'white' } } };

const chart = LightweightCharts.createChart(
            document.getElementById('container'))


// Configure the chart's time scale to show minute tick marks
chart.applyOptions({
    timeScale: {
        timeVisible: true,
        secondsVisible: false,
        tickMarkFormatter: (time, tickMarkType, locale) => {
            // time is a business day or timestamp (in seconds)
            const date = new Date(time * 1000);
            const hours = date.getHours().toString().padStart(2, '0');
            const minutes = date.getMinutes().toString().padStart(2, '0');
            return `${hours}:${minutes}`;
        }
    }
});

// Create both series
const orderHistorySeries = chart.addCustomSeries(new Mycustomplugin()); // { lineColor: '#2962FF', topColor: '#2962FF', bottomColor: 'rgba(41, 98, 255, 0.28)' });
const stockHistorySeries = chart.addSeries(LightweightCharts.CandlestickSeries);

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

fetch(stockHistoryFile)
    .then(response => response.json())
    .then(data => {

        // TODO: this will be passed by an internal function
        let buyData = [];
        generateBuyData(orderHistoryFile).then(data => buyData = data);
        // Set the data for the Main Series
        console.log('Stock history data loaded:', data);
        stockHistorySeries.setData(data);

        // // Generate sample data to use within a candlestick series
        //const candleStickData = generateCandlestickData();
        const lineData = buyData.map(datapoint => ({
            time: datapoint.time,
            value: datapoint.value,
        }));

        const areaSeries = chart.addSeries(LightweightCharts.LineSeries)
        // Set the data for the Area Series
        areaSeries.setData(lineData);

    })
    .catch(error => console.error('Error fetching JSON data:', error));


fetch(orderHistoryFile)
    .then(response => response.json())
    .then(data => {
        orderHistorySeries.setData(data.map(entry => ({
            time: entry.time,
            value: entry.value,
            color: entry.color //|| '#2962FF', // Default color if not specified
        })));
    })
    .catch(error => console.error('Error loading order history file JSON data:', error));
