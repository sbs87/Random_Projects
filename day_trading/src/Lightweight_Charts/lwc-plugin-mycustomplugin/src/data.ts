import { CustomData } from 'lightweight-charts';

/**
 * Mycustomplugin Data
 */
export interface MycustompluginData extends CustomData {
	//* Define the structure of the data required for the series.
	//* You could also 'extend' an existing Lightweight Charts Data type like LineData or CandlestickData
	value: number;
}

// export interface MycustompluginData extends CustomData {
// 	//* Define the structure of the data required for the series.
// 	//* You could also 'extend' an existing Lightweight Charts Data type like LineData or CandlestickData
// 	high: number;
// 	low: number;
// }
