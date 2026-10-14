from pathlib import Path
root=Path('examples/starpost-valley/src/main/java/starpost')
(root/'realvalley/TownTerrain.java').write_text('''package starpost.realvalley;

import java.util.List;
import java.util.stream.IntStream;
import com.openggf.level.objects.ObjectSpawn;
import starpost.realtown.TownContent;
import starpost.realtown.TownLayout;
import starpost.valley.Runner;
import starpost.valley.Valley;

/** The single mapping seam between town destinations and the real valley's geometry. */
public final class TownTerrain {
    private TownTerrain() {}

    /** Scene coordinates share the block columns; the act adds its empty sky rows. */
    public static TownLayout layout(Valley valley) {
        Runner.Ground ground = new Runner.Ground() {
            public int left() { return valley.left(); }
            public int right() { return RealValley.blocks().length * RealValley.S1_BLOCK; }
            public boolean solid(int x, int y) { return valley.solid(x, y - RealValley.terrainTop()); }
            public int floorBelow(int x, int fromY) {
                return valley.floorBelow(x, Math.max(0, fromY - RealValley.terrainTop())) + RealValley.terrainTop();
            }
        };
        return new TownLayout(ground,
            RealValley.columnOf(RealValley.SPRING_BLOCK) * RealValley.S1_BLOCK + 20,
            RealValley.columnOf(RealValley.LOOP_BLOCK) * RealValley.S1_BLOCK, valley.places);
    }

    /** Native camera-local admission must cover the gate and every menu-return position. */
    public static List<ObjectSpawn> admission(S1Terrain terrain) {
        return IntStream.range(0, RealValley.blocks().length).mapToObj(i -> {
            int x = RealValley.FARM_GATE_X + i * RealValley.S1_BLOCK;
            return TownContent.spawn(TownContent.CONTROLLER, i, x, ValleyLevel.floorAt(terrain, x));
        }).toList();
    }

    public static int entryX() { return RealValley.FARM_GATE_X + 40; }
    public static int entryY(TownLayout layout, String farmer) {
        // S3K standing radii: Tails is four pixels shorter than Sonic and Knuckles.
        return layout.ground.floorBelow(entryX(), 0) - (farmer.equals("tails") ? 15 : 19) - 1;
    }
}
''')
p=root/'realvalley/ValleyLevel.java'; s=p.read_text().replace('objects.addAll(loopSwappers(objects.size()));','objects.addAll(loopSwappers(objects.size()));\n        objects.addAll(TownTerrain.admission(terrain));'); p.write_text(s)
p=root/'realtown/TownBridge.java'; s=p.read_text().replace('TownLayout.from(play.valley().valley)','starpost.realvalley.TownTerrain.layout(play.valley().valley)'); p.write_text(s)
p=root/'scene/StarpostScene.java'; s=p.read_text().replace('private int returnX = 190, returnY = 173, healthRings;','private int returnX, returnY, healthRings;').replace('if (!returnToAct || actPlay != play) { returnX = 190; returnY = 173; healthRings = 0; }\n        prepareTownAct();','boolean fresh = !returnToAct || actPlay != play;\n        prepareTownAct();\n        if (fresh) {\n            returnX = starpost.realvalley.TownTerrain.entryX();\n            returnY = starpost.realvalley.TownTerrain.entryY(town.layout(), shell.game.farmer);\n            healthRings = 0;\n        }').replace('state.getOrDefault("town.returnX", "190")','state.getOrDefault("town.returnX", Integer.toString(returnX))').replace('state.getOrDefault("town.returnY", "173")','state.getOrDefault("town.returnY", Integer.toString(returnY))'); p.write_text(s)
p=root/'realtown/TownController.java'; s=p.read_text().replace('int width = town.layout().ground.right();','int width = town.layout().ground.right();').replace('TownContent.DECORATION,0,150,192','TownContent.DECORATION,0,spawn.x(),spawn.y()').replace('TownContent.DECORATION,1,150,192','TownContent.DECORATION,1,spawn.x(),spawn.y()').replace('town.layout().anchor("farm_gate"),192','town.layout().anchor("farm_gate"),town.layout().ground.floorBelow(town.layout().anchor("farm_gate"),0)').replace('i,door.x(),192','i,door.x(),town.layout().ground.floorBelow(door.x(),0)'); p.write_text(s)
p=root/'realtown/ActGround.java'; s=p.read_text().replace('var tile=level.getSolidTileForChunkDesc(desc,0x0C,false);','if (desc == null || !desc.getTopSolid()) return false;\n        var tile=level.getSolidTileForChunkDesc(desc,0x0C,false);'); p.write_text(s)
p=root/'valley/Pickups.java'; s=p.read_text().replace('int floor = ground.floorBelow(x, 0);\n            for (int i = 0; i < 5; i++) {\n                pickups.add(new Pickup(this, n++, x + i * 16, floor - 16, null));','for (int i = 0; i < 5; i++) {\n                pickups.add(new Pickup(this, n++, x + i * 16, ground.floorBelow(x + i * 16, 0) - 16, null));').replace('96 - 20 - (float) Math.sin(a) * 60','ground.floorBelow(springX, 0) - 116 - (float) Math.sin(a) * 60').replace('111 + (float) Math.cos(a) * 58','ground.floorBelow(loopX + 126, 0) - 81 + (float) Math.cos(a) * 58'); p.write_text(s)
# Existing regression now uses the layout rather than the removed placeholder's Y.
p=Path('src/test/java/com/openggf/TestModSceneActBridge.java'); s=p.read_text().replace('NativePositionOps.writeYPosResetSubpixel(player(),173);','NativePositionOps.writeYPosResetSubpixel(player(), townFloor(town, player().getCentreX()) - player().getYRadius() - 1);'); s=s.replace('    static Object field(Object object,String name)', '''    static int townFloor(Object town, int x) throws Exception {
        Object layout = call(town,"layout");
        return (int) call(field(layout,"ground"),"floorBelow",x,0);
    }
    static Object field(Object object,String name)'''); p.write_text(s)
