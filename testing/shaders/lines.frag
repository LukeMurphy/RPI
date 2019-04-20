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

float lines(vec2 pos, float b, float a){
    float scale = 3.10;
    //scale = abs(sin(u_time/20.0) * 2.2);
    pos *= (1.0 - scale);
    return smoothstep(a, a + b * 3.0 , 0.8 + abs((sin(pos.x * 3.1415) + b * 4.0)) * .5 );
}


void lines() {

    vec2 st = gl_FragCoord.xy/u_resolution.xy;
    st.y *= u_resolution.y/u_resolution.x;

    // period of gradients
    vec2 pos = st.yx *1.0;

    timec = u_time + sin(u_time * st.y/100.0);



    float freq = 10.0;
    
    vec2 pos_r = st.xy * 1.0 * freq ;//+ vec2(0.0,1.0);
    vec2 pos_g = st.xy * 1.0 * freq ;//+ vec2(-8.0,1.0);
    vec2 pos_b = st.xy * 1.0 * freq ;//+ vec2(-12.0,0.0);


    float pattern = pos.x;

    // Add noise
    pos = rotate2d( noise(pos) ) * pos * 10.0;//+ (tan(u_time/10.0)) + (sin(u_time/20.0) + 10.0);
    pos_r = rotate2d( noise(pos_r * sin(timec/100.0)) ) * pos_r * 2.200;
    pos_g = rotate2d( noise(pos_g * sin(timec/100.0)) ) * pos_g * 2.310;
    pos_b = rotate2d( noise(pos_b * sin(timec/100.0)) ) * pos_b * 2.210;

    // Draw lines
    float darkness = 1.35;
    float whiteness = 0.6;
    float pattern_r = lines(pos_r, whiteness, darkness);
    float pattern_g = lines(pos_g, whiteness, darkness);
    float pattern_b = lines(pos_b, whiteness, darkness);

    gl_FragColor = vec4(vec3(pattern_r,pattern_g,pattern_b),1.0);
}


void shps()
{    
    vec2 uv = gl_FragCoord.xy/u_resolution.xy;
           
    uv *= 20.;
    vec2 id = floor(uv);
    uv = fract(uv) - 0.5;    
            
    vec2 mxy = smoothstep(0.15, 0.14, abs(uv));    
    float m = clamp(mxy.x + mxy.y, 0., 1.);        
    vec3 col = mix(vec3(1.), vec3(1., 0.75, .9), m);
        
    vec2 v = smoothstep(0.45, 0.19, abs(uv)) - smoothstep(0.15, 0.14, abs(uv));
              
    vec2 p = step(0.15, abs(uv));
    vec2 mid = floor(mod(id, 2.));
    
    vec3 P = vec3(p,1.);
    v *= mix(P.zx, P.yz, step(mid.x, 1.-mid.y) * step(1.-mid.x, mid.y));
        
    col *=  mix(col, vec3(0.), v.x);
    col *=  mix(col, vec3(0.), v.y);            

    gl_FragColor = vec4(col,1.0);
}

vec3 GetColor(float normalizedValue)
{
    float angle = normalizedValue * 360.;
    if(angle < 60.)
    {
    return vec3(1.,(angle/60.),0.);   
    }
    else if(angle < 120.)
    {
        return vec3(1.-((angle - 60.)/60.),1.,0.);
    }
    else if(angle < 180.)
    {
        return vec3(0.,1.,((angle-120.)/60.));
    }
    else if(angle < 240.)
    {
        return vec3(0.,1. - (angle -180.)/60.,1.);
    }
        else if(angle < 300.)
    {
        return vec3((angle -240.)/60.,0.,1.);
    }
            else// if(angle <= 360.)
    {
        return vec3(1.,0.,1.-(angle -300.)/60.);
    }
}


// Smooth HSV to RGB conversion 
vec3 hsv2rgb_smooth( vec3 c)
{
    vec2 pos = gl_FragCoord.xy/u_resolution.xy;
    pos = rotate2d( noise(pos) ) * pos * 10.0;
    //vec3 rgb = clamp( (mod(c.x * 6.0 + vec3(1.0, 4.0, 2.0), 6.0) - 3.0) - 1.0, 0.0, 0.9 );
    float bandDensity = 8.0;
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
    float time = u_time/speedFactor + sin(uv.y /.050);
    vec3 hsvColor = hsv2rgb_smooth(vec3(time, 1.0, 1.0));
    float vol = 6.;
    //hsvColor += sin((4.0 - (1.0 * vol)) * (pow(uv.x * (3.0 + (10.0 * vol) + sin(time * 0.9)), 2.0) + pow(uv.y * (1.0 + (-1.0 * vol) + sin(time * 1.1)), 2.0)));
    //hsvColor = rotate2d(time);
    float brightness = 0.65;
    gl_FragColor = vec4(hsvColor, brightness);
}


float GetDistanceFromPoint(vec2 point)
{
    float xDist = abs(point.x- gl_FragCoord.x);
    float yDist = abs(point.y - gl_FragCoord.y);
    return sqrt(xDist*xDist + yDist*yDist);
}


vec3 getHSV(float angleVal) {
    float angle = angleVal * 3.0;
    float edgeStrength = 10.0;
    float red = edgeStrength * sin(angle);
    float green = edgeStrength * sin(angle + 2.0 * PI / 3.0); // + 60°
    float blue = edgeStrength * sin(angle + 4.0 * PI / 3.0); // + 120°
    return vec3(red, green, blue);
}

void radial() {
    float density = 1.0;
    float speed = 100.;
    float brightness = 0.65;
    float normalizedDistance = GetDistanceFromPoint(u_resolution/2.20);
    vec2 uv = gl_FragCoord.xy / u_resolution.xy;
    float time = u_time + sin(uv.y /.050);
    //float soundValue = (texture(iChannel0, vec2(0.1, 0.0)).x);
    normalizedDistance -= speed * time;
    normalizedDistance = 1.0 * mod(density * normalizedDistance,360.0)/360.0;
    gl_FragColor = vec4(GetColor(normalizedDistance), brightness);
    //gl_FragColor = vec4(getHSV(normalizedDistance), brightness);
}


void main() {
    //lines();
    //shps();
    //radial();
    bands();
}

