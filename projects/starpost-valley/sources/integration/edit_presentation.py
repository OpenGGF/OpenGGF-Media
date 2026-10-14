from pathlib import Path
root=Path('examples/starpost-valley/src/main/java/starpost')
p=root/'StarpostValleyMod.java'; s=p.read_text().replace('starpost.realtown.TownContent.registerInput(context, destination, town);','starpost.realtown.TownContent.registerInput(context, destination, town);\n        // S1 ROM-art TIME/day clock and wallet RINGS are drawn by the town HUD.\n        context.registerHudProfile(new com.openggf.mods.code.ModHudProfileContribution(destination,\n            new com.openggf.level.objects.HudProfile(java.util.List.of())));'); p.write_text(s)
p=root/'scene/PlayScreen.java'; s=p.read_text().replace('void chooseMusic(Shell shell)','public void chooseMusic(Shell shell)'); p.write_text(s)
p=root/'realtown/TownBridge.java'; s=p.read_text().replace('new TownPresentation(shell.art,FestivalSystem.forPlay(play),play)','new TownPresentation(shell.art,FestivalSystem.forPlay(play),play,shell)').replace('if (result==null) return;','if (result==null) return;\n        shell.music.parkForAct();').replace('case "farm_gate" -> play.returnToFarm();','case "farm_gate" -> { play.returnToFarm(); play.chooseMusic(shell); shell.music.update(); }'); p.write_text(s)
p=root/'realtown/TownPresentation.java'; s=p.read_text().replace('private final starpost.scene.PlayScreen play;','private final starpost.scene.PlayScreen play;\n    private final starpost.scene.Shell shell;').replace('this.art=art; peopleArt=new PeopleArt(art); this.festivals=festivals; this.play=play;','this(art,festivals,play,null);\n    }\n    public TownPresentation(Art art,FestivalSystem festivals,starpost.scene.PlayScreen play,starpost.scene.Shell shell) {\n        this.art=art; peopleArt=new PeopleArt(art); this.festivals=festivals; this.play=play; this.shell=shell;').replace('    private SceneCanvas canvas(ObjectServices services)', '''    /** The retained context uses the same scoped donor route as the farm's soundtrack. */
    public void updateMusic(int x) {
        if (shell == null || play == null) return;
        play.placeInValley(x);
        play.chooseMusic(shell);
        shell.music.update();
    }
    private SceneCanvas canvas(ObjectServices services)''').replace('''        canvas.fill(0,0,canvas.width(),17,0xE0101848);
        String hud=town.game().calendar.clock()+"   RINGS "+town.game().rings+"   MOMENTUM "+town.game().momentum;
        canvas.text(hud,6,5,Text.YELLOW);''','''        var calendar=town.game().calendar;
        boolean flash=town.ticks()/8%2==0;
        art.hud.timeRow(canvas,calendar.minutes()>=24*60&&flash,
            calendar.minutes()/60%24,calendar.minutes()%60,8);
        art.hud.ringsRow(canvas,town.game().rings==0&&flash,town.game().rings,24);
        String date=starpost.core.Calendar.seasonName(calendar.season())+" "+calendar.day()+" "+
            starpost.core.Calendar.weekdayName(calendar.weekday());
        Text.right(canvas,date,canvas.width()-8,6,Text.WHITE);''').replace('canvas.fill(6,21,','canvas.fill(6,43,').replace('canvas.text(town.notice(),10,24,','canvas.text(town.notice(),10,46,'); p.write_text(s)
p=root/'realtown/TownController.java'; s=p.read_text().replace('town.tick(x,y,!entity.getAir());','town.tick(x,y,!entity.getAir());\n        if (town.presentation()!=null) town.presentation().updateMusic(x);'); p.write_text(s)
