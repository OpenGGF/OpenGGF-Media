package board;
import com.openggf.mods.code.GgfMod;
import com.openggf.mods.code.ModContext;
public final class BoardMod implements GgfMod {
    @Override public void register(ModContext context) { context.registerStartupScene(Board::new); }
}
