#ifdef GL_ES
precision mediump float;
#endif

float fixedPositonX = 10;
float fixedPositonY= 10;

varying vec2 position;
//attribute vec2  position;

uniform sampler2D texture;
uniform vec2 resolution;
uniform float time;
uniform float lineScale;
uniform float rTimeMult;
uniform float gTimeMult;
uniform float bTimeMult;
uniform float distortionScale;
uniform float brightness;

uniform float rMax = 1.0;
uniform float gMax = 1.0;
uniform float bMax = 1.0;

uniform float min = .0;

uniform int mono = 0;

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

void action(void) {
    vec2 p = -1.0 + 2.0 * gl_FragCoord.xy / resolution.xy;
    vec2 m = -1.0 + 2.0 * fixedPositonY / resolution.xy;

    float a1 = atan(p.y - m.y, p.x - m.x);
    float r1 = sqrt(dot(p - m, p - m));
    float a2 = atan(p.y + m.y, p.x + m.x);
    float r2 = sqrt(dot(p + m, p + m));

    vec2 uv;
    uv.x = 0.1 * time + (r1 - r2) * 0.25;
    uv.y = sin(2.0 * (a1 - a2));

    float w = r1 * r2 * 0.8;
    vec3 col = texture2D(texture, 0.5 - 0.495 * uv).xyz;

    gl_FragColor = vec4(col / (0.1 + w), 1.0);
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
    float r = smoothstep(0.01, rMax, sin(PI*2 * distance  + time* rTimeMult)) * brightness + min;
    float g = smoothstep(0.01, gMax, sin(2. * PI*2 * distance + time*gTimeMult)) * brightness + min;
    float b = smoothstep(0.01, bMax, cos(PI*2 * distance + time*bTimeMult)) * brightness + min;

    vec3 color = vec3(r,g,b);

    if (mono == 1) {
        color = vec3(b,b,b);
    }
    
    gl_FragColor = vec4(color,1.0);
}
