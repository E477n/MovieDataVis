import 'plotly.js/dist/plotly';

var Plotly = require('plotly.js/lib/core');
Plotly.register([
    require('plotly.js/lib/pie'),
    require('plotly.js/lib/choropleth'),
	require('plotly.js/lib/surface')
]);

var TESTER = document.getElementById('tester');
Plotly.plot( TESTER, [{
x: [1, 2, 3, 4, 5],
y: [1, 2, 4, 8, 16] }], {
margin: { t: 0 } } );

function getData(){
	var arr = [];
	for(let i=0; i<10; i++){
		arr.push(Array(10).fill().map(() => Math.random()));
	}
	return arr;
}

console.log(getData());
Plotly.newPlot('myDiv', [{
	z: getData(),
	type: 'surface'
}]);