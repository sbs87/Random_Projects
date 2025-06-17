
function generateBuyData() {
    return [
        {
            time: 1748958360,
            value: 7.6
        },
        {
            time: 1748958540,
            value: 8.3
        }
    ]
};
// Fetch data from a JSON file and use it to populate the chart
const buyData = generateBuyData();
const jsonFilePath = prompt('Please enter the path to the JSON file:', 'stock_order_2025-06-03_MCTR_1m.json');
fetch(jsonFilePath)
    .then(response => response.json())
    .then(data => {
        // Create the Lightweight Chart within the container element
        const chart = LightweightCharts.createChart(
            document.getElementById('container')
        );

        // Create the Main Series (Candlesticks)
        const mainSeries = chart.addSeries(LightweightCharts.CandlestickSeries);

        // Set the data for the Main Series
        mainSeries.setData(data);

        // // Generate sample data to use within a candlestick series
        const candleStickData = generateCandlestickData();
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
