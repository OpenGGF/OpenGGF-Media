import com.openggf.mods.testing.CreatorTestLauncher;
import java.io.PrintWriter;
import java.net.URL;
import java.net.URLClassLoader;
import java.nio.file.Path;

/**
 * Throwaway: runs a compiled creator test directory through the engine's launcher.
 * From a worktree root (R = your scratch dir):
 *   CP="target/classes:$(cat target/test-classpath.txt)"
 *   javac --release 21 -nowarn -cp "$CP" -d $R/main $(find examples/starpost-valley/src/main/java -name '*.java')
 *   javac --release 21 -nowarn -cp "$R/main:$CP" -d $R/tests $(find examples/starpost-valley/src/test/java -name '*.java')
 *   javac -cp "$CP" -d $R/out RunCreatorTests.java
 *   java -cp "$R/out:$CP" RunCreatorTests $R/tests $R/main
 */
public class RunCreatorTests {
    public static void main(String[] a) throws Exception {
        Path tests = Path.of(a[0]), main = Path.of(a[1]);
        try (URLClassLoader loader = new URLClassLoader(new URL[] {tests.toUri().toURL(), main.toUri().toURL()},
                RunCreatorTests.class.getClassLoader())) {
            int code = CreatorTestLauncher.scan(loader, tests, new PrintWriter(System.out, true), new PrintWriter(System.err, true));
            System.exit(code);
        }
    }
}
