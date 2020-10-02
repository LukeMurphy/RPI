class Dither {

    int levels = 1;
    int x0 = 1;
    int x1 = 1;
    int y0 = 1;
    int y1 = 1;

void Dither() {

}

PImage dither(PImage source) {
    float lNorm = 255./levels;

    // FS Kernal
    float d1 = 7. / 16.;
    float d2 = 3. / 16.;
    float d3 = 5. / 16.;
    float d4 = 1. / 16.;

    int c, nc, lc, rc;
    float r, g, b;
    float nr, ng, nb;
    float er, eg, eb;
    float lr, lg, lb;
    int x = 0, y = 0;

    // Ordered Dithering Implementation
    for (y = y0; y < y1; y++) {
        for (x = x0; x <= x1; x++) {
            // Retrieve current RGB value
            c = source.get(x, y);
            r = (c >> 16) & 0xFF;
            g = (c >> 8) & 0xFF;
            b = c & 0xFF;

            // Normalize and scale to number of levels
            // basically a cheap but crappy form of color quantization
            nr = round((r/255) * levels) * lNorm;
            ng = round((g/255) * levels) * lNorm;
            nb = round((b/255) * levels) * lNorm;

            // Set the current pixel
            nc = color(nr, ng, nb);
            source.set(x, y, nc);

            // Quantization Error
            er = r-nr;
            eg = g-ng;
            eb = b-nb;

            // Apply the kernel
            // +1, 0
            lc = source.get(x + 1, y);
            lr = (lc >> 16 & 0xFF) + d1 * er;
            lg = (lc >> 8 & 0xFF) + d1 * eg;
            lb = (lc & 0xFF) + d1 * eb;
            source.set(x + 1, y, color(lr, lg, lb));

            // -1, +1
            lc = source.get(x - 1, y + 1);
            lr = (lc >> 16 & 0xFF) + (d2*er);
            lg = (lc >> 8 & 0xFF) + (d2*eg);
            lb = (lc & 0xFF) + (d2*eb);
            source.set(x - 1, y + 1, color(lr, lg, lb));

            // 0, +1
            lc = source.get(x, y + 1);
            lr = (lc >> 16 & 0xFF) + (d3*er);
            lg = (lc >> 8 & 0xFF) + (d3*eg);
            lb = (lc & 0xFF) + (d3*eb);
            source.set(x, y + 1, color(lr, lg, lb));

            // +1, +1
            lc = source.get(x+1, y+1);
            lr = (lc >> 16 & 0xFF) + (d4*er);
            lg = (lc >> 8 & 0xFF) + (d4*eg);
            lb = (lc & 0xFF) + (d4*eb);
            source.set(x+1, y+1, color(lr, lg, lb));
        }
    }
     return source;
}
}
