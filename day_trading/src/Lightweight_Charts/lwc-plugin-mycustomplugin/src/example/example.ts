import { createChart } from 'lightweight-charts';
import { Mycustomplugin } from '../mycustomplugin';
import { MycustompluginData } from '../data';
//import { generateSampleData } from '../sample-data';
import dataJson from '/Users/stevensmith/Projects/Random_Projects/day_trading/src/Lightweight_Charts/order_history.json';

const chart = ((window as unknown as any).chart = createChart('chart', {
	autoSize: true,
}));

const series = chart.addCustomSeries(new Mycustomplugin(), {
	/* Options */
});

const data: MycustompluginData[] = dataJson as MycustompluginData[];
//const data: MycustompluginData[] = generateSampleData(10, 50);
series.setData(data);
