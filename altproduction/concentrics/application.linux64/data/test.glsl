// Author @patriciogv - 2015
// http://patriciogonzalezvivo.com

#ifdef GL_ES
precision mediump float;
#endif


uniform vec2 resolution;
uniform vec2 mouse;
uniform float time;
uniform float lineScale;

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
	vec2 u = f*f*(3.0-2.0*f);
	return mix( mix( random( i + vec2(0.0, 0.0) ),
	                 random( i + vec2(1.0, 0.0) ), u.x),
	            mix( random( i + vec2(0.0, 1.0) ),
	                 random( i + vec2(1.0, 1.0) ), u.x), u.y);
}

mat2 rotate2d(float angle){
	//return mat2(cos(angle * sin(time/8.)*4),-sin(angle * sin(time/8.)*4),
	//            sin(angle * sin(time/16.)*4),cos(angle * sin(time/8.)*4));
	
	return mat2(cos(angle * sin(time/8.)*4),sin(angle * sin(time/8.)*4),
	            0.0,0.0);
}

float lines(in vec2 pos, float b){
	float scale = lineScale;
	pos *= scale;
	return smoothstep(1.0,
	                .5+b*.5,
	                abs((sin(pos.x*3.1415)+b*2.0))*.5);
}


void main() {
	vec2 st = gl_FragCoord.xy/resolution.xy;
	st.y *= resolution.y/resolution.x;

	vec2 pos = st.yx*vec2(10.,3.);

	float pattern = pos.x;

	// Add noise
	pos = rotate2d( noise(pos ) ) * pos;

	// Draw lines
	pattern = lines(pos,.95);
	
	vec3 color = vec3(.0);
	st *= 1.;
	
	// Show the 2D grid
	color.rb = fract(st);
	color.gr = fract(st);

	gl_FragColor = vec4(vec3(pattern) * color,1.0);
}
