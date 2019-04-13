import './index.css';


// create scene, camera and renderer
var THREE = require('three');
var scene = new THREE.Scene();
var camera = new THREE.PerspectiveCamera(200, window.innerWidth/window.innerHeight, 1, 500);
// PerspectiveCamera is one of the cameras
//PerspectiveCamera(field of view (degrees), aspect ratio, near, far)
camera.position.set(0, 0, 100);
camera.lookAt(0, 0, 0);

var renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

var material = new THREE.LineBasicMaterial({
	color: 0xC0C0C0
});
var geometry = new THREE.Geometry();
geometry.vertices.push(new THREE.Vector3(-10, 0, 0));
geometry.vertices.push(new THREE.Vector3(0, 10, 0));
geometry.vertices.push(new THREE.Vector3(10, 0, 0));
var line = new THREE.Line(geometry, material);
scene.add(line);

var geometry1 = new THREE.SphereBufferGeometry( 100, 100, 100 );

var wireframe = new THREE.WireframeGeometry( geometry1 );

var line2 = new THREE.LineSegments( wireframe );
line2.material.depthTest = false;
line2.material.opacity = 0.25;
line2.material.transparent = true;

scene.add( line2 );

camera.position.z = 5;

function animate(){
	requestAnimationFrame(animate); //this function pauses when user navigates to another browser tab
	line.rotation.x += 0.02;
	line.rotation.y += 0.02; //run every frame (60 times.second)
	renderer.render(scene, camera);
}



/**
 * @author alteredq / http://alteredqualia.com/
 * @author mr.doob / http://mrdoob.com/
 */

var WEBGL = {

	isWebGLAvailable: function () {

		try {

			var canvas = document.createElement( 'canvas' );
			return !! ( window.WebGLRenderingContext && ( canvas.getContext( 'webgl' ) || canvas.getContext( 'experimental-webgl' ) ) );

		} catch ( e ) {

			return false;

		}

	},

	isWebGL2Available: function () {

		try {

			var canvas = document.createElement( 'canvas' );
			return !! ( window.WebGL2RenderingContext && canvas.getContext( 'webgl2' ) );

		} catch ( e ) {

			return false;

		}

	},

	getWebGLErrorMessage: function () {

		return this.getErrorMessage( 1 );

	},

	getWebGL2ErrorMessage: function () {

		return this.getErrorMessage( 2 );

	},

	getErrorMessage: function ( version ) {

		var names = {
			1: 'WebGL',
			2: 'WebGL 2'
		};

		var contexts = {
			1: window.WebGLRenderingContext,
			2: window.WebGL2RenderingContext
		};

		var message = 'Your $0 does not seem to support <a href="http://khronos.org/webgl/wiki/Getting_a_WebGL_Implementation" style="color:#000">$1</a>';

		var element = document.createElement( 'div' );
		element.id = 'webglmessage';
		element.style.fontFamily = 'monospace';
		element.style.fontSize = '13px';
		element.style.fontWeight = 'normal';
		element.style.textAlign = 'center';
		element.style.background = '#fff';
		element.style.color = '#000';
		element.style.padding = '1.5em';
		element.style.width = '400px';
		element.style.margin = '5em auto 0';

		if ( contexts[ version ] ) {

			message = message.replace( '$0', 'graphics card' );

		} else {

			message = message.replace( '$0', 'browser' );

		}

		message = message.replace( '$1', names[ version ] );

		element.innerHTML = message;

		return element;

	}

};

// three.js does not support IE10 and below
if ( WEBGL.isWebGLAvailable() ) {
	animate();
} else {
	var warning = WEBGL.getWebGLErrorMessage();
	document.getElementById( 'container' ).appendChild( warning );
}