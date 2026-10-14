package promoaudio;
import com.openggf.mods.code.GgfMod;
import com.openggf.mods.code.ModContext;
/** Borrowed Slay/Flappy soundboard registration; no gameplay mutators. */
public final class AudioMod implements GgfMod {
    @Override public void register(ModContext context) {
        context.registerStartupScene(SoundboardScene::new);
    }
}
