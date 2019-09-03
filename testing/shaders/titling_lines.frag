//#define TAU 6.283185307179

#ifdef GL_ES
precision mediump float;
#endif

uniform vec2 u_resolution;
uniform vec2 u_mouse;
uniform float u_time;
float timec;
const float TAU = 6.2831853071795864769;
const float PI = 3.1415;
const float brightness = .9;
const float speedFactor = 1.0;
//out vec4 fragColor, in vec2 fragCoord 

void mainImage()
{
	vec2 uv = (1. * gl_FragCoord.xy - u_resolution.xy) / u_resolution.y;
	
	const float gridNum = 1.5;
	
	vec2 gpos = fract(uv * gridNum);
	
	// translate to center
	gpos = gpos * 2. - 1.;

	// diagonal distance 
	float diag = (abs(gpos.x) + abs(gpos.y)) * .45;
	
	float colOffset = .5 * TAU * diag; //*(gpos.x + gpos.y);
	vec3 colOffsetv = vec3(-colOffset, 0, colOffset);
	
	const float stripeNum = 3.;

	// diagonal stripes  
	vec3 val = vec3(sin(diag * stripeNum * TAU - u_time/speedFactor * TAU + colOffsetv));
	
	float b = 100./u_resolution.y;
	vec3 col = smoothstep(-b, b, val);
 
	gl_FragColor = vec4(col,brightness);

}

void main() {
	mainImage();
}