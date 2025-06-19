import { createChart } from 'lightweight-charts';
import { Mycustomplugin } from '../mycustomplugin';
import { MycustompluginData } from '../data';
import { generateSampleData } from '../sample-data';

const chart = ((window as unknown as any).chart = createChart('chart', {
	autoSize: true,
}));

const series = chart.addCustomSeries(new Mycustomplugin(), {
	/* Options */
});

const data: MycustompluginData[] = generateSampleData(100, 50);
series.setData(data);
