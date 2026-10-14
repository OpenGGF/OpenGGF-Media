import org.lwjgl.egl.*;
import org.lwjgl.opengl.*;
import org.lwjgl.system.MemoryStack;
import java.nio.*;
import static org.lwjgl.egl.EGL10.*;
import static org.lwjgl.egl.EGL12.*;
import static org.lwjgl.egl.EGL14.*;
import static org.lwjgl.egl.EGL15.*;
import static org.lwjgl.opengl.GL11.*;
public class EglDirect {
  public static void main(String[] a){
    long dpy = EXTPlatformBase.eglGetPlatformDisplayEXT(MESAPlatformSurfaceless.EGL_PLATFORM_SURFACELESS_MESA, EGL_DEFAULT_DISPLAY, (IntBuffer)null);
    System.out.println("dpy="+dpy);
    try (MemoryStack s = MemoryStack.stackPush()) {
      IntBuffer maj=s.mallocInt(1), min=s.mallocInt(1);
      System.out.println("init="+eglInitialize(dpy,maj,min)+" "+maj.get(0)+"."+min.get(0));
      EGLCapabilities caps = EGL.createDisplayCapabilities(dpy, maj.get(0), min.get(0));
      System.out.println("bind="+eglBindAPI(EGL_OPENGL_API));
      IntBuffer attrs = s.ints(EGL_SURFACE_TYPE, EGL_PBUFFER_BIT, EGL_RENDERABLE_TYPE, EGL_OPENGL_BIT,
          EGL_RED_SIZE,8,EGL_GREEN_SIZE,8,EGL_BLUE_SIZE,8,EGL_ALPHA_SIZE,8, EGL_NONE);
      PointerBuffer cfg = s.mallocPointer(1); IntBuffer n=s.mallocInt(1);
      System.out.println("choose="+eglChooseConfig(dpy, attrs, cfg, n)+" n="+n.get(0));
      long surf = eglCreatePbufferSurface(dpy, cfg.get(0), s.ints(EGL_WIDTH,320,EGL_HEIGHT,224,EGL_NONE));
      System.out.println("surf="+surf+" err="+Integer.toHexString(eglGetError()));
      long ctx = eglCreateContext(dpy, cfg.get(0), EGL_NO_CONTEXT, s.ints(EGL_CONTEXT_MAJOR_VERSION,4,EGL_CONTEXT_MINOR_VERSION,1,
          EGL_CONTEXT_OPENGL_PROFILE_MASK, EGL_CONTEXT_OPENGL_CORE_PROFILE_BIT, EGL_NONE));
      System.out.println("ctx="+ctx+" err="+Integer.toHexString(eglGetError()));
      System.out.println("make="+eglMakeCurrent(dpy,surf,surf,ctx));
      GL.createCapabilities();
      System.out.println(glGetString(GL_RENDERER)+" | "+glGetString(GL_VERSION));
      IntBuffer rb=s.mallocInt(1); eglQuerySurface(dpy,surf,EGL_RENDER_BUFFER,rb); System.out.println("renderbuf="+Integer.toHexString(rb.get(0)));
      glClearColor(1,0,0,1); glClear(GL_COLOR_BUFFER_BIT); glReadBuffer(GL_BACK);
      ByteBuffer px = org.lwjgl.BufferUtils.createByteBuffer(4); glReadPixels(5,5,1,1,GL_RGBA,GL_UNSIGNED_BYTE,px);
      System.out.println("px="+(px.get(0)&255)+","+(px.get(1)&255)+" glerr="+glGetError());
    }
  }
}
