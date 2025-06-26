import { Mycustomplugin } from './mycustomplugin/mycustomplugin.mjs';
// Create a form for user input
// const form = document.createElement('form');
// form.style.textAlign = 'center';
// form.style.margin = '20px 0';

// const label = document.createElement('label');
// label.textContent = 'Stock Name: ';
// label.htmlFor = 'stockNameInput';

// const input = document.createElement('input');
// input.type = 'text';
// input.id = 'stockNameInput';
// input.value = 'ACXP';
// input.style.marginRight = '10px';

// const dateLabel = document.createElement('label');
// dateLabel.textContent = 'Date: ';
// dateLabel.htmlFor = 'stockDateInput';

// const dateInput = document.createElement('input');
// dateInput.type = 'date';
// dateInput.id = 'stockDateInput';
// dateInput.value = '2025-06-17';
// dateInput.style.marginRight = '10px';

// const submitBtn = document.createElement('button');
// submitBtn.type = 'submit';
// submitBtn.textContent = 'Load Chart';

// form.appendChild(label);
// form.appendChild(input);
// form.appendChild(dateLabel);
// form.appendChild(dateInput);
// form.appendChild(submitBtn);

// document.body.insertBefore(form, document.getElementById('container'));

// // Prevent default form submission and reload chart with new values
// form.addEventListener('submit', function(e) {
//     e.preventDefault();
//     location.search = `?stockName=${encodeURIComponent(input.value)}&stockDate=${encodeURIComponent(dateInput.value)}`;
// });

// // Parse URL parameters for stockName and stockDate
// function getQueryParam(param, defaultValue) {
//     const urlParams = new URLSearchParams(window.location.search);
//     return urlParams.get(param) || defaultValue;
// }

// const stockName = getQueryParam('stockName', input.value);
// const stockDate = getQueryParam('stockDate', dateInput.value);

// Fetch data from a JSON file and use it to populate the chart
const stockName = prompt('Please enter the stock name:', 'ACXP');
const stockDate = prompt('Please enter the stock date:', '2025-06-17');
const stockHistoryFile = `data/stock_hx_${stockName}_${stockDate}.json`;
const orderHistoryFile = `data/stock_order_${stockName}_${stockDate}.json`; //prompt('Please enter the path to the Stocks Order buy/sell history JSON file:', 'order_history.json');

const orderHistoryOptions = { pointRadius: 5}; // { layout: { textColor: 'black', background: { type: 'solid', color: 'white' } } };

const chart = LightweightCharts.createChart(
            document.getElementById('container'))


const container = document.getElementById('container');
const title = document.createElement('h2');
title.textContent = `Stock: ${stockName} | Date: ${stockDate}`;
title.style.textAlign = 'center';
title.style.margin = '10px 0';
container.parentNode.insertBefore(title, container);



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
const stockHistorySeries = chart.addSeries(LightweightCharts.CandlestickSeries);

const orderHistorySeries = chart.addCustomSeries(new Mycustomplugin(),orderHistoryOptions); // { lineColor: '#2962FF', topColor: '#2962FF', bottomColor: 'rgba(41, 98, 255, 0.28)' });

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
        //console.log('Stock history data loaded:', data);
        stockHistorySeries.setData(data);

        // // Generate sample data to use within a candlestick series
        //const candleStickData = generateCandlestickData();
        const lineData = buyData.map(datapoint => {
            if (datapoint.value == null) {
            console.log('Null value at time:', datapoint.time);

            }else{
            return {
            time: datapoint.time,
            value: datapoint.value,
             
            }};
        });
         //console.log('Order history data loaded:', data);

        const areaSeries = chart.addSeries(LightweightCharts.LineSeries)
        // Set the data for the Area Series
        areaSeries.setData(lineData);

    })
    .catch(error => console.error('Error fetching JSON data:', error));


fetch(orderHistoryFile)
    .then(response => response.json())
    .then(data => {
        orderHistorySeries.setData(data.map(entry => ({
            ...(entry.value == null ? (console.log('Null value at time:', entry.time), false) : { value: entry.value }),
            time: entry.time,
            value: entry.value,
            color: entry.color //|| '#2962FF', // Default color if not specified
        })));
        console.log('Order history data loaded:', data);

    })
    .catch(error => console.error('Error loading order history file JSON data:', error));
