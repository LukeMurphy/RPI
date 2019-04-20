// Author @patriciogv - 2015
// http://patriciogonzalezvivo.com

#ifdef GL_ES
precision mediump float;
#endif

uniform vec2 u_resolution;
uniform vec2 u_mouse;
uniform float u_time;
float timec;
const float tau = 6.2831853071795864769;
const float PI = 3.1415;

float random (in vec2 st) {
    return fract(sin(dot(st.xy,
                         vec2(12.9898,78.233)))
                * 43758.5453123);
}

// Value noise by Inigo Quilez - iq/2013
// https://www.shadertoy.com/view/lsf3WH
float noise(vec2 st) {
    vec2 i = floor(st) * 1.0;
    vec2 f = fract(st) * 1.0;
    vec2 u = f*f*(3.0-2.0*f);
    return mix( mix( random( i + vec2(0.0, 0.0) ),
                     random( i + vec2(1.0, 0.0) ), u.x),
                mix( random( i + vec2(0.0, 1.0) ),
                     random( i + vec2(1.0, 1.0) ), u.x), u.y);
}

mat2 rotate2d(float angle){
    return mat2(cos(angle),-cos(angle), sin(angle),cos(angle));
}


// Smooth HSV to RGB conversion 
vec3 hsv2rgb_smooth( vec3 c)
{
    vec2 pos = gl_FragCoord.xy/u_resolution.xy;
    pos = rotate2d( noise(pos) ) * pos * 10.0;
    //vec3 rgb = clamp( (mod(c.x * 6.0 + vec3(1.0, 4.0, 2.0), 6.0) - 3.0) - 1.0, 0.0, 0.9 );
    float bandDensity = 8.0;
    //bandDensity = 8.0+ pos.y/5.0 + pos.x/10.0;
    float whiteValue = 0.0;
    float brightness = 1.0;
    vec3 rgb = clamp( abs(mod(c.x * bandDensity + vec3(0.0, 4.0, 8.0), 6.0) - 2.0) - 1.0, whiteValue, brightness );
    // cubic smoothing 
    //rgb = rgb * rgb * (3.0 - 2.0 * rgb); 
    //return c.z * mix(vec3(1.0, 1.0, 1.0), rgb, c.y);
    return rgb;
}

void bands() {
    vec2 uv = gl_FragCoord.xy / u_resolution.xy;
    float speedFactor = 4.0;
    float frequency = 0.05;
    float time = u_time/speedFactor + sin(uv.y /frequency);
    vec3 hsvColor = hsv2rgb_smooth(vec3(time, 1.0, 1.0));
    float vol = 6.;
    //hsvColor += sin((4.0 - (1.0 * vol)) * (pow(uv.x * (3.0 + (10.0 * vol) + sin(time * 0.9)), 2.0) + pow(uv.y * (1.0 + (-1.0 * vol) + sin(time * 1.1)), 2.0)));
    //hsvColor = rotate2d(time);
    float brightness = 0.65;
    gl_FragColor = vec4(hsvColor, brightness);
}


void main() {
    bands();
}

