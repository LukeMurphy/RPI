// Author @patriciogv - 2015
// http://patriciogonzalezvivo.com

#ifdef GL_ES
precision mediump float;
#endif


uniform vec2 resolution;
uniform vec2 mouse;
uniform float time;
uniform float lineScale;
uniform float rTimeMult;
uniform float gTimeMult;
uniform float bTimeMult;
uniform float distortionScale;
uniform float brightness;

//attribute vec2  position;

#define PI 3.14159265359


// Plot a line on Y using a value between 0.0-1.0
float plot(vec2 st, float pct){
	return  smoothstep( pct-0.02, pct, st.y) -
	        smoothstep( pct, pct+0.02, st.y);
}

float random (in vec2 st) {
	return fract(sin(dot(st.xy,
	                     vec2(12.9898,78.233)))
	            * 43758.5453123);
}

// Value noise by Inigo Quilez - iq/2013
// https://www.shadertoy.com/view/lsf3WH
float noise(vec2 st) {
	vec2 i = floor(st);
	vec2 f = fract(st);
	vec2 u = f*f*(2.0-1.0*f);
	return mix( mix( random( i + vec2(0.0, 0.0) ),
	                 random( i + vec2(1.0, 0.0) ), u.x),
	            mix( random( i + vec2(0.0, 1.0) ),
	                 random( i + vec2(1.0, 1.0) ), u.x), u.y);
}

mat2 rotate2d(float angle){
	//return mat2(cos(angle * sin(time/8.)*4),-sin(angle * sin(time/8.)*4),
	//            sin(angle * sin(time/16.)*4),cos(angle * sin(time/8.)*4));
	return mat2( cos(angle * sin(time/8.)*4), sin(angle * sin(time/8.)*4), 0.0, 0.0);
}


void main() {

	vec2 position = vec2(320,180);
	vec2 st = 5. * (gl_FragCoord.xy)/resolution;

	vec2 pos = st.xy*vec2(5.,10.);
	// Add noise
	pos = rotate2d( noise(pos ) ) * pos;

	float distanceX = gl_FragCoord.x - position[0] - pos[0];
	float distanceY = gl_FragCoord.y - position[1] - pos[1];
	float distance = -distortionScale * sqrt(distanceX*distanceX + distanceY*distanceY);
	
	// Smooth interpolation between 0.1 and 0.9
	float r = smoothstep(0.01, 1.0, sin(PI*2 * distance  + time* rTimeMult)) * brightness;
	float g = smoothstep(0.01, 1.0, sin(2. * PI*2 * distance + time*gTimeMult)) * brightness;
	float b = smoothstep(0.01, 1.0, cos(PI*2 * distance + time*bTimeMult)) * brightness;
	vec3 color = vec3(r,g,b);
	
	// Plot a line
	//float pct = plot(st,y);
	//color = (1.0-pct)*color+pct*vec3(st.x,abs(sin(time/30)),0.0);
	gl_FragColor = vec4(color,1.0);


	//gl_FragColor = vec4(st.x,abs(cos(time/30)),abs(tan(time/2)),1.0);
}
