import org.lwjgl.opengl.GL;
import org.lwjgl.system.*;
import org.lwjgl.PointerBuffer;
import java.nio.*;
import static org.lwjgl.system.JNI.*;
import static org.lwjgl.opengl.GL11.*;
public class EglJni {
  public static void main(String[] a) throws Exception {
    SharedLibrary egl = Library.loadNative(EglJni.class, "org.lwjgl.egl", "libEGL.so.1");
    long getPlatformDisplay = egl.getFunctionAddress("eglGetPlatformDisplay");
    long initialize = egl.getFunctionAddress("eglInitialize"), bindApi = egl.getFunctionAddress("eglBindAPI");
    long choose = egl.getFunctionAddress("eglChooseConfig"), pbuf = egl.getFunctionAddress("eglCreatePbufferSurface");
    long create = egl.getFunctionAddress("eglCreateContext"), make = egl.getFunctionAddress("eglMakeCurrent");
    long getError = egl.getFunctionAddress("eglGetError"), getProc = egl.getFunctionAddress("eglGetProcAddress");
    long dpy = invokePPP(0x31DD /*EGL_PLATFORM_SURFACELESS_MESA*/, 0L, 0L, getPlatformDisplay);
    System.out.println("dpy="+dpy);
    try (MemoryStack s = MemoryStack.stackPush()) {
      IntBuffer maj=s.mallocInt(1), min=s.mallocInt(1);
      System.out.println("init="+invokePPPI(dpy, MemoryUtil.memAddress(maj), MemoryUtil.memAddress(min), initialize)+" "+maj.get(0)+"."+min.get(0));
      System.out.println("bind="+invokeI(0x30A2 /*EGL_OPENGL_API*/, bindApi));
      IntBuffer attrs = s.ints(0x3033,0x0001 /*SURFACE_TYPE PBUFFER*/, 0x3040,0x0008 /*RENDERABLE OPENGL*/,
          0x3024,8,0x3023,8,0x3022,8,0x3021,8, 0x3038);
      PointerBuffer cfg = s.mallocPointer(1); IntBuffer n=s.mallocInt(1);
      System.out.println("choose="+invokePPPPI(dpy, MemoryUtil.memAddress(attrs), MemoryUtil.memAddress(cfg), 1, MemoryUtil.memAddress(n), choose)+" n="+n.get(0));
      long surf = invokePPPP(dpy, cfg.get(0), MemoryUtil.memAddress(s.ints(0x3057,960,0x3056,672,0x3038)), pbuf);
      System.out.println("surf="+surf+" err="+Integer.toHexString(invokeI(getError)));
      long ctx = invokePPPPP(dpy, cfg.get(0), 0L, MemoryUtil.memAddress(s.ints(0x3098,4,0x30FB,1,0x30FD,0x1,0x3038)), create);
      System.out.println("ctx="+ctx+" err="+Integer.toHexString(invokeI(getError)));
      System.out.println("make="+invokePPPPI(dpy,surf,surf,ctx,make));
      GL.createCapabilities();
      System.out.println(glGetString(GL_RENDERER)+" | "+glGetString(GL_VERSION));
      glClearColor(1,0,0,1); glClear(GL_COLOR_BUFFER_BIT); glReadBuffer(GL_BACK);
      ByteBuffer px = org.lwjgl.BufferUtils.createByteBuffer(4); glReadPixels(5,5,1,1,GL_RGBA,GL_UNSIGNED_BYTE,px);
      System.out.println("px="+(px.get(0)&255)+","+(px.get(1)&255)+" glerr="+glGetError());
    }
  }
}
