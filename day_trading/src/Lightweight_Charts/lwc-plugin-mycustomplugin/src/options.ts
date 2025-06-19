import {
	CustomSeriesOptions,
	customSeriesDefaultOptions,
} from 'lightweight-charts';

export interface MycustompluginOptions extends CustomSeriesOptions {
	//* Define the options for the series.
	highLineColor: string;
	lowLineColor: string;
	areaColor: string;
	highLineWidth: number;
	lowLineWidth: number;
		pointRadius: number;
		pointColor: string;
}

export const defaultOptions: MycustompluginOptions = {
	//* Define the default values for all the series options.
	...customSeriesDefaultOptions,
	highLineColor: '#049981',
	lowLineColor: '#F23645',
	areaColor: 'rgba(41, 98, 255, 0.2)',
	highLineWidth: 2,
	lowLineWidth: 2,
	pointRadius: 3,
	pointColor: '#049981',
} as const;
