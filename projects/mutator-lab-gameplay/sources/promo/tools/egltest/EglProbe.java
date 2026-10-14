import org.lwjgl.opengl.GL;
import static org.lwjgl.glfw.GLFW.*;
import static org.lwjgl.opengl.GL11.*;
public class EglProbe {
  public static void main(String[] a){
    org.lwjgl.glfw.GLFWErrorCallback.createPrint(System.out).set(); glfwInitHint(GLFW_PLATFORM, GLFW_PLATFORM_NULL);
    System.out.println("init="+glfwInit()+" platform="+glfwGetPlatform());
    glfwDefaultWindowHints(); glfwWindowHint(GLFW_VISIBLE,GLFW_FALSE);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR,4); glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR,1);
    glfwWindowHint(GLFW_OPENGL_PROFILE,GLFW_OPENGL_CORE_PROFILE); glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT,GLFW_TRUE);
    glfwWindowHint(GLFW_CONTEXT_CREATION_API,GLFW_EGL_CONTEXT_API); if(a.length>0){glfwWindowHint(GLFW_DEPTH_BITS,0);glfwWindowHint(GLFW_STENCIL_BITS,0);} if(a.length>1){glfwWindowHint(GLFW_ALPHA_BITS,0);glfwWindowHint(GLFW_DOUBLEBUFFER,GLFW_FALSE);}
    long w=glfwCreateWindow(320,224,"probe",0,0); System.out.println("window="+w);
    if(w!=0){glfwMakeContextCurrent(w);GL.createCapabilities();System.out.println(glGetString(GL_RENDERER)+" | "+glGetString(GL_VERSION));}
    glfwTerminate();
  }
}
