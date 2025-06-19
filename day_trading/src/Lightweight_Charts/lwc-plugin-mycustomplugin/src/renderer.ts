
import {
	BitmapCoordinatesRenderingScope,
	CanvasRenderingTarget2D,
} from 'fancy-canvas';
import {
	ICustomSeriesPaneRenderer,
	PaneRendererCustomData,
	PriceToCoordinateConverter,
	Time,
} from 'lightweight-charts';
import { MycustompluginData } from './data';
import { MycustompluginOptions } from './options';

interface MycustompluginItem {
	x: number;
	value: number;
}

export class MycustompluginRenderer<TData extends MycustompluginData>
	implements ICustomSeriesPaneRenderer
{
	_data: PaneRendererCustomData<Time, TData> | null = null;
	_options: MycustompluginOptions | null = null;

	draw(
		target: CanvasRenderingTarget2D,
		priceConverter: PriceToCoordinateConverter
	): void {
		target.useBitmapCoordinateSpace(scope =>
			this._drawImpl(scope, priceConverter)
		);
	}

	update(
		data: PaneRendererCustomData<Time, TData>,
		options: MycustompluginOptions
	): void {
		this._data = data;
		this._options = options;
	}

	_drawImpl(
		renderingScope: BitmapCoordinatesRenderingScope,
		priceToCoordinate: PriceToCoordinateConverter
	): void {
		if (
			this._data === null ||
			this._data.bars.length === 0 ||
			this._data.visibleRange === null ||
			this._options === null
		) {
			return;
		}
		const options = this._options;
		const bars: MycustompluginItem[] = this._data.bars.map(bar => {
			return {
				x: bar.x * renderingScope.horizontalPixelRatio,
				value: priceToCoordinate(bar.originalData.value)! * renderingScope.verticalPixelRatio,
			};
		});

		const ctx = renderingScope.context;

		ctx.beginPath();
		const lowLine = new Path2D();
		const highLine = new Path2D();
		const firstBar = bars[this._data.visibleRange.from];
		lowLine.moveTo(firstBar.x, firstBar.value);
		for (
			let i = this._data.visibleRange.from + 1;
			i < this._data.visibleRange.to;
			i++
		) {
			const bar = bars[i];
			lowLine.lineTo(bar.x, bar.value);
		}

		const lastBar = bars[this._data.visibleRange.to - 1];
		highLine.moveTo(lastBar.x, lastBar.value);
		for (
			let i = this._data.visibleRange.to - 2;
			i >= this._data.visibleRange.from;
			i--
		) {
			const bar = bars[i];
			highLine.lineTo(bar.x, bar.value);
		}

		// Draw all points
		for (let i = this._data.visibleRange.from; i < this._data.visibleRange.to; i++) {
			const bar = this._data.bars[i];
			const x = bar.x * renderingScope.horizontalPixelRatio;
			const y = priceToCoordinate(bar.originalData.value)! * renderingScope.verticalPixelRatio;

			ctx.beginPath();
			ctx.arc(x, y, options.pointRadius * renderingScope.verticalPixelRatio, 0, 2 * Math.PI);
			ctx.fillStyle = options.pointColor;
			ctx.fill();
		}
		
	}
}
