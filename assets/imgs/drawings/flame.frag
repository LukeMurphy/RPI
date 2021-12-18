# define PIXELS 32.0
# ifdef GL_ES
precision mediump float;
# endif
const float PI = 3.14159;

uniform float u_time;
uniform vec2 u_resolution;
uniform sampler2D uTexture;


float mask(vec2 uv, float r) {
    uv -= .5;
    vec2 p = vec2(0., 0.);
    float dx = uv.x - p.x;
    float dy = uv.y - p.y;
    dx *= .75;
    dy *= .15;
    dy += .05;

    return (r * r) / (dx * dx + dy * dy);
}

float random(vec2 uv) {
    return fract(sin(dot(vec2(100., 213.), uv)) * 3141.);
}

float value_noise(vec2 uv) {
    vec2 i = floor(uv);
    vec2 f = fract(uv);

    f = f * f * (3. - 2. * f);

    float b = mix(random(i), random(i + vec2(1., 0.)), f.x);
    float t = mix(random(i + vec2(0., 1.)), random(i + vec2(1.)), f.x);

    return mix(b, t, f.y);
}

float noise(vec2 uv) {
    float n = value_noise(uv);
    n += value_noise(uv * 2.) * 0.5;
    //n += value_noise(uv * 4.) * 0.25;
    //n += value_noise(uv * 8.) * 0.125;
    //n += value_noise(uv * 16.) * 0.0625;

    return n / 1.9375;
}

vec4 ditherTest(vec4 s, vec4 s2) {

    if (s.x < s2.x) s.x += s2.x;
    if (s.y > s2.y) s.y += s2.y;
    if (s.z > s2.z) s.z += s2.z;
    return s;
}

vec4 src(float pt) {

    vec2 uv = gl_FragCoord.xy / u_resolution.xy;

    vec2 nuv1 = vec2((uv.x + pt) * 5., uv.y - u_time * 0.5);
    vec2 nuv2 = vec2((uv.x + pt) * 5., uv.y - u_time * 0.5);
    vec2 nuv3 = vec2((uv.x + pt) * 5., uv.y - u_time * 0.5);

    vec4 n1 = vec4(1., 0.5, 0., 1.) * noise(nuv1);
    vec4 n2 = vec4(0., 0., 1., 1.) * noise(nuv2);
    vec4 n3 = vec4(1., 1., 0., 1.) * noise(nuv3);

    vec4 s = (n1 + n2 + n3) * (mask(uv, .1) - 0.5);
    //s = (n1+n2 +n3) - 0.5;
    return s;
}


const int lookupSize = 32;
const float errorCarry1 = 0.1;
const float errorCarry2 = 0.3;
const float errorCarry3 = 0.5;

float getGrayscale(vec2 coords, vec3 sourcePixel) {
    //vec2 uv = coords / u_resolution.xy;
    //uv.y = 1.0-uv.y;
    //vec3 sourcePixel = texture2D(uTexture, uv).rgb;
    return length(sourcePixel * vec3(0.2126, 0.7152, 0.0722));
}



void main() {
    // Normalized pixel coordinates (from 0 to 1)
    // Output to screen
    float pointX = gl_FragCoord.x;
    float pointY = gl_FragCoord.y;

    vec4 s1 = src(0.0);
    vec4 s2 = src(0.0);

    //vec4 s1a = texture2D(s1, vec2(pointX, pointY) / u_resolution.xy);

    //gl_FragColor = ditherTest(s1,s2); 

    vec4 source = 1.0 * (texture2D(uTexture, vec2(pointX, pointY) / u_resolution.xy));
    vec4 source2 = texture2D(uTexture, vec2(pointX + 1.0, pointY) / u_resolution.xy);

    //gl_FragColor = ditherTest(s1,source2); 

    int topGapY = int(u_resolution.y - gl_FragCoord.y);
    int cornerGapX = int((gl_FragCoord.x < 10.0) ? gl_FragCoord.x : u_resolution.x - gl_FragCoord.x);
    int cornerGapY = int((gl_FragCoord.y < 10.0) ? gl_FragCoord.y : u_resolution.y - gl_FragCoord.y);
    int cornerThreshhold = ((cornerGapX == 0) || (topGapY == 0)) ? 5 : 4;

    vec2 uv = gl_FragCoord.yx / u_resolution.xy;
    //uv.y = 1.0-uv.y;
    //uv.x = 1.0-uv.x;
    vec3 sourcePixel = texture2D(uTexture, uv).rgb;

    sourcePixel = source.rgb;
    sourcePixel = s1.rgb;

    if (cornerGapX + cornerGapY < cornerThreshhold) {

        gl_FragColor = vec4(0, 0, 0, 1);

    } else if (topGapY < 2) {

        if (topGapY == 1) {

            gl_FragColor = vec4(0, 0, 0, 1);

        } else {

            gl_FragColor = vec4(1, 1, 1, 1);

        }

    } else {

        float xError1 = 0.0;
        float xError2 = 0.0;
        float xError3 = 0.0;
        for (int xLook = 0; xLook < lookupSize; xLook++) {
            float grayscale1 = getGrayscale(gl_FragCoord.xy + vec2(-lookupSize + xLook, 0), sourcePixel);
            float grayscale2 = getGrayscale(gl_FragCoord.xy + vec2(-lookupSize + xLook, 0), sourcePixel);
            float grayscale3 = getGrayscale(gl_FragCoord.xy + vec2(-lookupSize + xLook, 0), sourcePixel);
            grayscale1 += xError1;
            grayscale2 += xError2;
            grayscale3 += xError3;
            float bit1 = grayscale1 >= 0.5 ? 1.0 : 0.0;
            float bit2 = grayscale2 >= 0.5 ? 1.0 : 0.0;
            float bit3 = grayscale3 >= 0.5 ? 1.0 : 0.0;
            xError1 = (grayscale1 - bit1) * errorCarry1;
            xError2 = (grayscale2 - bit2) * errorCarry2;
            xError3 = (grayscale3 - bit3) * errorCarry3;
        }

        float yError1 = 0.0;
        float yError2 = 0.0;
        float yError3 = 0.0;
        for (int yLook = 0; yLook < lookupSize; yLook++) {
            float grayscale1 = getGrayscale(gl_FragCoord.xy + vec2(0, -lookupSize + yLook), sourcePixel);
            float grayscale2 = getGrayscale(gl_FragCoord.xy + vec2(0, -lookupSize + yLook), sourcePixel);
            float grayscale3 = getGrayscale(gl_FragCoord.xy + vec2(0, -lookupSize + yLook), sourcePixel);
            grayscale1 += yError1;
            grayscale2 += yError2;
            grayscale3 += yError3;
            float bit1 = grayscale1 >= 0.5 ? 1.0 : 0.0;
            float bit2 = grayscale2 >= 0.5 ? 1.0 : 0.0;
            float bit3 = grayscale3 >= 0.5 ? 1.0 : 0.0;
            yError1 = (grayscale1 - bit1) * errorCarry1;
            yError2 = (grayscale2 - bit2) * errorCarry2;
            yError3 = (grayscale3 - bit3) * errorCarry3;
        }

        float finalGrayscale1 = getGrayscale(gl_FragCoord.xy, sourcePixel);
        float finalGrayscale2 = getGrayscale(gl_FragCoord.xy, sourcePixel);
        float finalGrayscale3 = getGrayscale(gl_FragCoord.xy, sourcePixel);
        finalGrayscale1 += xError1 * 0.5 + yError1 * 0.5;
        finalGrayscale2 += xError2 * 0.5 + yError2 * 0.5;
        finalGrayscale3 += xError3 * 0.5 + yError3 * 0.5;
        float finalBit1 = finalGrayscale1 >= 0.5 ? 1.0 : 0.0;
        float finalBit2 = finalGrayscale2 >= 0.5 ? 1.0 : 0.0;
        float finalBit3 = finalGrayscale3 >= 0.5 ? 1.0 : 0.0;

        gl_FragColor = vec4(finalBit1, finalBit2, finalBit3, 1.0);

    }
    /*
     vec4 final = ditherTest(gl_FragCoord.xy, source, source2) * 1.0;
     gl_FragColor = final;
     */
}