import {
	CustomSeriesPricePlotValues,
	ICustomSeriesPaneView,
	PaneRendererCustomData,
	WhitespaceData,
	Time,
} from 'lightweight-charts';
import { MycustompluginOptions, defaultOptions } from './options';
import { MycustompluginRenderer } from './renderer';
import { MycustompluginData } from './data';

export class Mycustomplugin<TData extends MycustompluginData>
	implements ICustomSeriesPaneView<Time, TData, MycustompluginOptions>
{
	_renderer: MycustompluginRenderer<TData>;

	constructor() {
		this._renderer = new MycustompluginRenderer();
	}

	priceValueBuilder(plotRow: TData): CustomSeriesPricePlotValues {
		const maxval = Math.max(plotRow.value, plotRow.value);
		const midPoint = (0 + maxval) / 2;
		//* The values returned here are used for the autoscaling behaviour on the chart,
		//* and the last value is also used as the price value for the crosshair and price label.
		//return [plotRow.value, plotRow.value, midPoint];
		return [0,maxval, midPoint];
	}

	isWhitespace(data: TData | WhitespaceData): data is WhitespaceData {
		//* Method for checking if a specific datapoint should be considered whitespace
		//* Use this to filter out the data points which should be whitespace on the chart (and
		//* not get provided to the renderer).
		//return (data as Partial<TData>).low === undefined || (data as Partial<TData>).high === undefined;
		return (data as Partial<TData>).value === undefined;
	}

	renderer(): MycustompluginRenderer<TData> {
		return this._renderer;
	}

	update(
		data: PaneRendererCustomData<Time, TData>,
		options: MycustompluginOptions
	): void {
		this._renderer.update(data, options);
	}

	defaultOptions() {
		return defaultOptions;
	}
}
