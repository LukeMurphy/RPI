// Author @patriciogv - 2015
// Title: Mosaic

#ifdef GL_ES
precision mediump float;
#endif

uniform vec2 u_resolution;
uniform vec2 u_mouse;
uniform float u_time;

float random (vec2 st) {
	return fract(sin(dot(st.xy,
	                     vec2(12.9898,78.233)))*
	    43758.5453123 + (sin(u_time)/1.0 * cos(u_time)/1.0));
}


float random2 (vec2 st) {
    return fract(sin(dot(st.xy,
                         vec2(12.9898,78.233)))*
        43758.5453123);
}

void main() {
	vec2 st = 1.30 * gl_FragCoord.xy/u_resolution.xy;

	st *= 10.0 ; // Scale the coordinate system by 10
	vec2 ipos = floor(st);  // get the integer coords
	vec2 fpos = fract(st);  // get the fractional coords

	// Assign a random value based on the integer coord
	vec3 color = vec3(random( ipos  ));

	// Uncomment to see the subdivided grid
	//color = vec3(fpos,0.0);

	gl_FragColor = vec4(color,1.0);
	gl_FragColor = vec4(vec3(color.x - cos(u_time/2.0), color.y - sin(u_time/1.0), color.z - sin(u_time/1.0)/10.0),1.0);
}