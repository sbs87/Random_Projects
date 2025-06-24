import { Mycustomplugin } from './mycustomplugin/mycustomplugin.mjs';


// Fetch data from a JSON file and use it to populate the chart
const stockHistoryFile = prompt('Please enter the path to the Stocks price history JSON file:', 'stock_order_2025-06-03_MCTR_1m.json');
const orderHistoryFile = prompt('Please enter the path to the Stocks Order buy/sell history JSON file:', 'order_history.json');

const chart = LightweightCharts.createChart(
            document.getElementById('container')
        );

// Create both series
const orderHistorySeries = chart.addCustomSeries(new Mycustomplugin(), {
	/* Options */
});
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


fetch(orderHistoryFile)
    .then(response => response.json())
    .then(data => {
        orderHistorySeries.setData(data.map(entry => ({
            time: entry.time,
            value: entry.value
        })));
    })
    .catch(error => console.error('Error loading order history file JSON data:', error));

fetch(stockHistoryFile)
    .then(response => response.json())
    .then(data => {

        // TODO: this will be passed by an internal function
        let buyData = [];
        generateBuyData(orderHistoryFile).then(data => buyData = data);
        // Set the data for the Main Series
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

