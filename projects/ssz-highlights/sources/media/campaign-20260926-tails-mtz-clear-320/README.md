# Tails SSZ capture — campaign-20260926-tails-mtz-clear-320

Runtime: develop ed828779df8f169802d53b1c4c5fee97d546dcb0 (before the newly
proposed preliminary widescreen projection correction). Native S3K,320px,
Tails alone, donor off, fresh SSZ1 entry. No position/ring/health/clock seeds.
Input: src/test/resources/routes/s3k/ssz1-tails-solo-cold-replicas-320.bk2 in the resumed campaign tree.

Reproduce with GameplayCaptureTool --game s3k --zone ssz --act 1 --main tails
--sidekick none --width 320 --rom <absolute S3K ROM> --input <above BK2>
--frames 9675 --capture-from 7680 --out-dir <new external directory>.
The tool supplies neutral input after the movie ends. Capture frames are
zero-based; the MP4 shows frames7680–9674,60fps.

All9675 author rows match19 recorded gameplay-state fields against this
fresh replay. No deaths or follower in all9675 capture rows. Full MP4 decode
passed; selected attack/defeat/arrival or exit stills were inspected. This is
engine route/presentation evidence, not native-emulator parity. Whole-registry
route tests are pending when this note is written; consult the committed act
matrix for their eventual result. The full route loads DEZ at input17,669.
