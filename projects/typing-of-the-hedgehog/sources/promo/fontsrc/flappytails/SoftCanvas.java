package flappytails;
import com.openggf.mods.scene.*;
import java.awt.image.BufferedImage;
/** Temporary software SceneCanvas for previewing frames without GL. */
public class SoftCanvas implements SceneCanvas {
    final int w, h; final int[] px; int cx0, cy0, cx1, cy1;
    public SoftCanvas(int w, int h) { this.w = w; this.h = h; px = new int[w*h]; unclip(); }
    public int width() { return w; } public int height() { return h; }
    public void clear(int rgb) { java.util.Arrays.fill(px, 0xFF000000 | rgb); }
    void blend(int x, int y, int argb) {
        if (x < cx0 || y < cy0 || x >= cx1 || y >= cy1) return;
        int a = argb >>> 24; if (a == 0) return;
        int d = px[y*w+x];
        if (a == 255) { px[y*w+x] = argb | 0xFF000000; return; }
        int r = ((argb>>16&255)*a + (d>>16&255)*(255-a))/255, g = ((argb>>8&255)*a + (d>>8&255)*(255-a))/255, b = ((argb&255)*a + (d&255)*(255-a))/255;
        px[y*w+x] = 0xFF000000 | r<<16 | g<<8 | b;
    }
    public void fill(int x, int y, int fw, int fh, int argb) { for (int j=y;j<y+fh;j++) for (int i=x;i<x+fw;i++) blend(i,j,argb); }
    public void draw(SceneImage image, float x, float y) { draw(image, x, y, SceneDraw.plain()); }
    public void draw(SceneImage image, float x, float y, SceneDraw st) { drawRegion(image, 0, 0, image.width(), image.height(), x, y, image.width()*st.scaleX(), image.height()*st.scaleY(), st); }
    public void draw(SceneSprite s, float x, float y, SceneDraw st) {
        float ox = st.flipX() ? (s.width() - s.originX()) : s.originX();
        float oy = st.flipY() ? (s.height() - s.originY()) : s.originY();
        drawRegion(s.image(), 0, 0, s.width(), s.height(), x - ox*st.scaleX(), y - oy*st.scaleY(), s.width()*st.scaleX(), s.height()*st.scaleY(), st);
    }
    public void drawRegion(SceneImage img, int sx, int sy, int sw, int sh, float dx, float dy, float dw, float dh, SceneDraw st) {
        int x0 = Math.round(dx), y0 = Math.round(dy), x1 = Math.round(dx+dw), y1 = Math.round(dy+dh);
        int tint = st.tint(), flash = st.flash();
        for (int j=y0;j<y1;j++) for (int i=x0;i<x1;i++) {
            int u = (int)((i - dx) * sw / dw), v = (int)((j - dy) * sh / dh);
            if (u<0||v<0||u>=sw||v>=sh) continue;
            if (st.flipX()) u = sw-1-u; if (st.flipY()) v = sh-1-v;
            int c = img.pixel(sx+u, sy+v); int a = c>>>24; if (a==0) continue;
            int r=c>>16&255,g=c>>8&255,b=c&255;
            r = r*(tint>>16&255)/255; g = g*(tint>>8&255)/255; b = b*(tint&255)/255; a = a*(tint>>>24)/255;
            int fa = flash>>>24; if (fa>0) { r = (r*(255-fa)+(flash>>16&255)*fa)/255; g=(g*(255-fa)+(flash>>8&255)*fa)/255; b=(b*(255-fa)+(flash&255)*fa)/255; }
            blend(i,j,a<<24|r<<16|g<<8|b);
        }
    }
    public void text(String t, int x, int y, int argb) { com.openggf.mods.ui.CompactFont.draw(new com.openggf.mods.ui.PixelCanvas(){public int width(){return w;}public int height(){return h;}public void fill(int a,int b,int c,int d,int e){SoftCanvas.this.fill(a,b,c,d,e);}}, t, x, y, 1, argb); }
    public int textWidth(String t) { return com.openggf.mods.ui.CompactFont.width(t, 1); }
    public void clip(int x, int y, int cw, int ch) { cx0=Math.max(0,x); cy0=Math.max(0,y); cx1=Math.min(w,x+cw); cy1=Math.min(h,y+ch); }
    public void unclip() { cx0=0; cy0=0; cx1=w; cy1=h; }
    public void save(String path) throws Exception { BufferedImage b = new BufferedImage(w,h,BufferedImage.TYPE_INT_ARGB); b.setRGB(0,0,w,h,px,0,w); javax.imageio.ImageIO.write(b,"png",new java.io.File(path)); }
}
