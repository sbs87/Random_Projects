var p = Object.defineProperty;
var b = (o, t, a) => t in o ? p(o, t, { enumerable: !0, configurable: !0, writable: !0, value: a }) : o[t] = a;
var r = (o, t, a) => b(o, typeof t != "symbol" ? t + "" : t, a);
import { customSeriesDefaultOptions as m } from "./node_modules/lightweight-charts/dist/lightweight-charts.standalone.development.mjs";
const x = {
  //* Define the default values for all the series options.
  ...m,
  highLineColor: "#049981",
  lowLineColor: "#F23645",
  areaColor: "rgba(41, 98, 255, 0.2)",
  highLineWidth: 2,
  lowLineWidth: 2,
  pointRadius: 3,
  pointColor: "#049981"
};
class R {
  constructor() {
    r(this, "_data", null);
    r(this, "_options", null);
  }
  draw(t, a) {
    t.useBitmapCoordinateSpace(
      (s) => this._drawImpl(s, a)
    );
  }
  update(t, a) {
    this._data = t, this._options = a;
  }
  _drawImpl(t, a) {
    if (this._data === null || this._data.bars.length === 0 || this._data.visibleRange === null || this._options === null)
      return;
    const s = this._options, n = this._data.bars.map((i) => ({
      x: i.x * t.horizontalPixelRatio,
      value: a(i.originalData.value) * t.verticalPixelRatio
    })), l = t.context;
    l.beginPath();
    const h = new Path2D(), u = new Path2D(), d = n[this._data.visibleRange.from];
    h.moveTo(d.x, d.value);
    for (let i = this._data.visibleRange.from + 1; i < this._data.visibleRange.to; i++) {
      const e = n[i];
      h.lineTo(e.x, e.value);
    }
    const v = n[this._data.visibleRange.to - 1];
    u.moveTo(v.x, v.value);
    for (let i = this._data.visibleRange.to - 2; i >= this._data.visibleRange.from; i--) {
      const e = n[i];
      u.lineTo(e.x, e.value);
    }
    for (let i = this._data.visibleRange.from; i < this._data.visibleRange.to; i++) {
      const e = this._data.bars[i], c = e.x * t.horizontalPixelRatio, _ = a(e.originalData.value) * t.verticalPixelRatio;
      l.beginPath(), l.arc(c, _, s.pointRadius * t.verticalPixelRatio, 0, 2 * Math.PI), l.fillStyle = s.pointColor, l.fill();
    }
  }
}
class P {
  constructor() {
    r(this, "_renderer");
    this._renderer = new R();
  }
  priceValueBuilder(t) {
    const a = Math.max(t.value, t.value), s = (0 + a) / 2;
    return [0, a, s];
  }
  isWhitespace(t) {
    return t.value === void 0;
  }
  renderer() {
    return this._renderer;
  }
  update(t, a) {
    this._renderer.update(t, a);
  }
  defaultOptions() {
    return x;
  }
}
export {
  P as Mycustomplugin
};
