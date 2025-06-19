import type { Time } from 'lightweight-charts';
import { MycustompluginData } from './data';

type LineData = {
	time: Time;
	value: number;
};

let randomFactor = 25 + Math.random() * 25;
const samplePoint = (i: number) =>
	i *
		(0.5 +
			Math.sin(i / 10) * 0.2 +
			Math.sin(i / 20) * 0.4 +
			Math.sin(i / randomFactor) * 0.8 +
			Math.sin(i / 500) * 0.5) +
	200;

function generateLineData(numberOfPoints: number = 500): LineData[] {
	randomFactor = 25 + Math.random() * 25;
	const res = [];
	const date = new Date(Date.UTC(2023, 0, 1, 12, 0, 0, 0));
	for (let i = 0; i < numberOfPoints; ++i) {
		const time = (date.getTime() / 1000) as Time;
		const value = i;//samplePoint(i);
		res.push({
			time,
			value,
		});

		date.setUTCDate(date.getUTCDate() + 1);
	}

	return res;
}

export function generateSampleData(
	numberOfPoints: number = 1000,
	averageWidth: number = 50
): MycustompluginData[] {
	return generateLineData(numberOfPoints).map(lineDataPoint => {
		//const high = lineDataPoint.value + Math.random() * averageWidth;
		const valuemod = lineDataPoint.value; //* averageWidth;

		console.log(`time: ${lineDataPoint.time}, value: ${valuemod}`);
		return {
			time: lineDataPoint.time,
			value: valuemod
		};
	});
}
